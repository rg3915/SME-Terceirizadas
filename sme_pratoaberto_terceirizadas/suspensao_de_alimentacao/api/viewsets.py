from rest_framework import status
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from sme_pratoaberto_terceirizadas.suspensao_de_alimentacao.api.serializers import SuspensaoDeAlimentacaoSerializer, \
    DiaRazaoSuspensaoDeAlimentacaoSerializer, DescricaoSuspensaoDeAlimentacaoSerializer
from sme_pratoaberto_terceirizadas.suspensao_de_alimentacao.models import SuspensaoDeAlimentacao


class SuspensaoDeAlimentacaoViewSet(ModelViewSet):
    """
    Endpoint para Suspensão de Alimentação
    """

    """
    Exemplo de POST:
    {
      "status":"SALVO",
      "negado_pela_terceirizada":true,
      "razao_negacao":"nao vai dar nao",
      "obs":"observacao da solicitacao",
      "dias_razoes":[
        {
          "data_de":"20/06/2019",
          "data_ate":"21/06/2019",
          "dias_de_semana":[
            "1",
            "2",
            "3"
          ],
          "razao":"Dia da família"
        }
      ],
      "descricoes":[
        {
          "periodo":"first_period",
          "numero_de_alunos":"100",
          "tipo_de_refeicao":[
            "Lanche 4 Horas",
            "Lanche 5/6 Horas"
          ]
        }
      ]
    }
    """
    queryset = SuspensaoDeAlimentacao.objects.all()
    serializer_class = SuspensaoDeAlimentacaoSerializer
    object_class = SuspensaoDeAlimentacao
    permission_classes = ()
    lookup_field = 'uuid'

    @action(detail=False, methods=['post'])
    def salvar(self, request):
        try:
            data = request.data.copy()
            data['criado_por'] = request.user.uuid
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            for dia_razao in data.get('dias_razoes'):
                serializer_dias_razoes = DiaRazaoSuspensaoDeAlimentacaoSerializer(data=dia_razao)
                serializer_dias_razoes.is_valid(raise_exception=True)
            for descricao in data.get('descricoes'):
                serializer_descricoes = DescricaoSuspensaoDeAlimentacaoSerializer(data=descricao)
                serializer_descricoes.is_valid(raise_exception=True)
            SuspensaoDeAlimentacao.salvar_suspensao(data, request.user)
        except ValidationError as validation_error:
            return Response({'error': validation_error.get_full_details()}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'success': 'Solicitação salva com sucesso'}, status=status.HTTP_200_OK)
