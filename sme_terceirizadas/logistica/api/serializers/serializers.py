from rest_framework import serializers

from sme_terceirizadas.dados_comuns.api.serializers import LogSolicitacoesUsuarioSerializer
from sme_terceirizadas.dados_comuns.models import LogSolicitacoesUsuario
from sme_terceirizadas.logistica.models import Alimento, Guia, SolicitacaoRemessa


class AlimentoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimento
        exclude = ('id',)


class AlimentoLookUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alimento
        fields = ('uuid', 'nome_alimento', 'qtd_volume', 'embalagem')


class GuiaSerializer(serializers.ModelSerializer):
    alimentos = serializers.SerializerMethodField()

    def get_alimentos(self, obj):
        return AlimentoSerializer(
            Alimento.objects.filter(
                guia=obj.id
            ),
            many=True
        ).data

    class Meta:
        model = Guia
        exclude = ('id',)


class GuiaLookUpSerializer(serializers.ModelSerializer):
    alimentos = serializers.SerializerMethodField()

    def get_alimentos(self, obj):
        return AlimentoLookUpSerializer(
            Alimento.objects.filter(
                guia=obj.id
            ),
            many=True
        ).data

    class Meta:
        model = Guia
        fields = ('uuid', 'numero_guia', 'data_entrega', 'codigo_unidade', 'nome_unidade', 'alimentos')


class SolicitacaoRemessaSerializer(serializers.ModelSerializer):
    guias = serializers.SerializerMethodField()
    logs = serializers.SerializerMethodField()

    log_atual = serializers.SerializerMethodField()

    def get_log_atual(self, obj):
        return LogSolicitacoesUsuarioSerializer(
            LogSolicitacoesUsuario.objects.filter(uuid_original=obj.uuid).last()
        ).data

    def get_logs(self, obj):
        return LogSolicitacoesUsuarioSerializer(
            LogSolicitacoesUsuario.objects.filter(uuid_original=obj.uuid).order_by('criado_em'),
            many=True
        ).data

    def get_guias(self, obj):
        return GuiaSerializer(
            Guia.objects.filter(
                solicitacao=obj.id
            ),
            many=True
        ).data

    class Meta:
        model = SolicitacaoRemessa
        exclude = ('id',)


class SolicitacaoRemessaLookUpSerializer(serializers.ModelSerializer):
    status = serializers.SerializerMethodField()
    guias = serializers.SerializerMethodField()
    distribuidor_nome = serializers.SerializerMethodField()

    def get_guias(self, obj):
        return GuiaLookUpSerializer(
            Guia.objects.filter(
                solicitacao=obj.id
            ),
            many=True
        ).data

    def get_distribuidor_nome(self, obj):
        return obj.distribuidor.razao_social

    def get_status(self, obj):
        return obj.get_status_display()

    class Meta:
        model = SolicitacaoRemessa
        fields = ('uuid', 'numero_solicitacao', 'distribuidor_nome', 'status', 'guias')


class XmlAlimentoSerializer(serializers.Serializer):
    StrCodSup = serializers.CharField()
    StrCodPapa = serializers.CharField()
    StrNomAli = serializers.CharField()
    StrEmbala = serializers.CharField()
    IntQtdVol = serializers.CharField()


class XmlGuiaSerializer(serializers.Serializer):
    StrNumGui = serializers.CharField()
    DtEntrega = serializers.DateField()
    StrCodUni = serializers.CharField()
    StrNomUni = serializers.CharField()
    StrEndUni = serializers.CharField()
    StrNumUni = serializers.CharField()
    StrBaiUni = serializers.CharField()
    StrCepUni = serializers.CharField()
    StrCidUni = serializers.CharField()
    StrEstUni = serializers.CharField()
    StrConUni = serializers.CharField()
    StrTelUni = serializers.CharField()
    alimentos = XmlAlimentoSerializer(many=True)


class XmlParserSolicitacaoSerializer(serializers.Serializer):
    StrCnpj = serializers.CharField(max_length=14)
    StrNumSol = serializers.CharField(max_length=30)
    guias = XmlGuiaSerializer(many=True)
