from rest_framework import serializers
from drf_base64.serializers import ModelSerializer

from .validators import deve_ter_extensao_valida
from ...dados_comuns.validators import deve_ser_no_passado
from ..models import Anexo, SolicitacaoDietaEspecial


class AnexoSerializer(ModelSerializer):
    nome = serializers.CharField()

    def validate_nome(self, nome):
        deve_ter_extensao_valida(nome)
        return nome

    class Meta:
        model = Anexo
        fields = ('arquivo', 'nome')


class SolicitacaoDietaEspecialSerializer(serializers.ModelSerializer):
    anexos = serializers.ListField(
        child=AnexoSerializer(), required=True
    )

    def validate_anexos(self, anexos):
        if not anexos:
            raise serializers.ValidationError('Anexos não pode ser vazio')
        return anexos

    def validate_data_nascimento_aluno(self, data_nascimento_aluno):
        deve_ser_no_passado(data_nascimento_aluno)
        return data_nascimento_aluno

    def create(self, validated_data):
        validated_data['criado_por'] = self.context['request'].user
        anexos = validated_data.pop('anexos', [])
        solicitacao = SolicitacaoDietaEspecial.objects.create(**validated_data)

        for anexo in anexos:
            anexo.pop('nome')
            Anexo.objects.create(
                solicitacao_dieta_especial=solicitacao, arquivo=anexo.get('arquivo')
            )

        return solicitacao

    class Meta:
        model = SolicitacaoDietaEspecial
        fields = (
            'uuid',
            'codigo_eol_aluno',
            'nome_completo_aluno',
            'nome_completo_pescritor',
            'registro_funcional_pescritor',
            'data_nascimento_aluno',
            'observacoes',
            'criado_em',
            'anexos'
        )