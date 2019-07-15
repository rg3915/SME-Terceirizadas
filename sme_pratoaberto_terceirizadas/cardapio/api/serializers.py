from datetime import date

from rest_framework import serializers
from traitlets import Any

from sme_pratoaberto_terceirizadas.dados_comuns.validators import (nao_pode_ser_passado, nao_pode_ser_feriado, \
                                                                   objeto_nao_deve_ter_duplicidade)
from ..models import *


class TipoAlimentacaoSerializer(serializers.ModelSerializer):

    def validate_nome(self, nome: str) -> Any:
        objeto_nao_deve_ter_duplicidade(TipoAlimentacao, 'Já existe um tipo de alimento com este nome: {}'.format(nome),
                                        nome=nome)
        return nome

    class Meta:
        model = TipoAlimentacao
        fields = ['uuid', 'nome']


class CardapioSimplesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cardapio
        fields = ['uuid', 'data']


class CardapioSerializer(serializers.ModelSerializer):
    tipos_alimentacao = TipoAlimentacaoSerializer(many=True, read_only=True)

    def validate_data(self, data: date) -> Any:
        nao_pode_ser_passado(data)
        nao_pode_ser_feriado(data)
        objeto_nao_deve_ter_duplicidade(
            Cardapio,
            mensagem='Já existe um cardápio cadastrado com esta data',
            data=data
        )
        return data

    class Meta:
        model = Cardapio
        fields = ['uuid', 'data', 'ativo', 'criado_em', 'tipos_alimentacao']


class InversaoCardapioSerializer(serializers.ModelSerializer):
    cardapio_de = CardapioSimplesSerializer()
    cardapio_para = CardapioSimplesSerializer()
    escola = serializers.SlugRelatedField(
        slug_field='uuid',
        required=True,
        queryset=Escola.objects.all()
    )

    class Meta:
        model = InversaoCardapio
        fields = ['uuid', 'descricao', 'criado_em', 'cardapio_de', 'cardapio_para', 'escola']
