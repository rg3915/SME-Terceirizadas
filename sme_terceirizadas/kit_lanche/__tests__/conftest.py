import datetime

import pytest
from faker import Faker
from model_mommy import mommy

from .. import models
from ...dados_comuns.fluxo_status import PedidoAPartirDaDiretoriaRegionalWorkflow, PedidoAPartirDaEscolaWorkflow
from ...dados_comuns.models import TemplateMensagem
from ...dados_comuns.models_abstract import TempoPasseio

fake = Faker('pt_BR')
fake.seed(420)


@pytest.fixture
def kit_lanche():
    itens = mommy.make(models.ItemKitLanche,
                       nome=fake.name(),
                       _quantity=3)
    return mommy.make(models.KitLanche, nome=fake.name(),
                      itens=itens)


@pytest.fixture
def item_kit_lanche():
    return mommy.make(models.ItemKitLanche,
                      nome=fake.name())


@pytest.fixture
def solicitacao_avulsa():
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.SOLICITACAO_KIT_LANCHE_AVULSA)
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche, kits=kits, data=datetime.datetime(2000, 1, 1))
    escola = mommy.make('escola.Escola')
    return mommy.make(models.SolicitacaoKitLancheAvulsa,
                      local=fake.text()[:160],
                      quantidade_alunos=999,
                      solicitacao_kit_lanche=solicitacao_kit_lanche,
                      escola=escola)


@pytest.fixture
def solicitacao_unificada_lista_igual():
    mommy.make(TemplateMensagem, tipo=TemplateMensagem.SOLICITACAO_KIT_LANCHE_UNIFICADA)
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional')
    return mommy.make(models.SolicitacaoKitLancheUnificada,
                      local=fake.text()[:160],
                      quantidade_max_alunos_por_escola=999,
                      lista_kit_lanche_igual=True,
                      solicitacao_kit_lanche=solicitacao_kit_lanche,
                      outro_motivo=fake.text(),
                      diretoria_regional=dre)


@pytest.fixture
def solicitacao_unificada_lotes_diferentes():
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional', nome=fake.name())
    solicitacao_unificada = mommy.make(models.SolicitacaoKitLancheUnificada,
                                       local=fake.text()[:160],
                                       quantidade_max_alunos_por_escola=999,
                                       lista_kit_lanche_igual=True,
                                       solicitacao_kit_lanche=solicitacao_kit_lanche,
                                       outro_motivo=fake.text(),
                                       diretoria_regional=dre)
    lote_um = mommy.make('escola.Lote')
    escola_um = mommy.make('escola.Escola', lote=lote_um)
    escola_dois = mommy.make('escola.Escola', lote=lote_um)
    escola_tres = mommy.make('escola.Escola', lote=lote_um)
    mommy.make(models.EscolaQuantidade,
               escola=escola_um,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_dois,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_tres,
               solicitacao_unificada=solicitacao_unificada)
    lote_dois = mommy.make('escola.Lote')
    escola_quatro = mommy.make('escola.Escola', lote=lote_dois)
    escola_cinco = mommy.make('escola.Escola', lote=lote_dois)
    mommy.make(models.EscolaQuantidade,
               escola=escola_quatro,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_cinco,
               solicitacao_unificada=solicitacao_unificada)
    return solicitacao_unificada


@pytest.fixture
def solicitacao_unificada_lotes_iguais():
    kits = mommy.make(models.KitLanche, _quantity=3)
    solicitacao_kit_lanche = mommy.make(models.SolicitacaoKitLanche,
                                        tempo_passeio=models.SolicitacaoKitLanche.OITO_OU_MAIS,
                                        kits=kits)
    dre = mommy.make('escola.DiretoriaRegional', nome=fake.name())
    solicitacao_unificada = mommy.make(models.SolicitacaoKitLancheUnificada,
                                       local=fake.text()[:160],
                                       quantidade_max_alunos_por_escola=999,
                                       lista_kit_lanche_igual=True,
                                       solicitacao_kit_lanche=solicitacao_kit_lanche,
                                       outro_motivo=fake.text(),
                                       diretoria_regional=dre)
    lote_um = mommy.make('escola.Lote')
    escola_um = mommy.make('escola.Escola', lote=lote_um)
    escola_dois = mommy.make('escola.Escola', lote=lote_um)
    escola_tres = mommy.make('escola.Escola', lote=lote_um)
    escola_quatro = mommy.make('escola.Escola', lote=lote_um)
    escola_cinco = mommy.make('escola.Escola', lote=lote_um)
    mommy.make(models.EscolaQuantidade,
               escola=escola_um,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_dois,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_tres,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_quatro,
               solicitacao_unificada=solicitacao_unificada)
    mommy.make(models.EscolaQuantidade,
               escola=escola_cinco,
               solicitacao_unificada=solicitacao_unificada)
    return solicitacao_unificada


@pytest.fixture
def solicitacao():
    kits = mommy.make(models.KitLanche, nome=fake.name(), _quantity=3)
    return mommy.make(models.SolicitacaoKitLanche,
                      descricao=fake.text(),
                      motivo=fake.text(),
                      tempo_passeio=TempoPasseio.CINCO_A_SETE,
                      kits=kits)


@pytest.fixture(params=[
    (0, True),
    (1, True),
    (2, True),
])
def horarios_passeio(request):
    return request.param


erro_esperado_passeio = 'tempo de passeio deve ser qualquer uma das opções:'


@pytest.fixture(params=[
    ('0', erro_esperado_passeio),
    ('TESTE', erro_esperado_passeio),
    (3, erro_esperado_passeio),
])
def horarios_passeio_invalido(request):
    return request.param


@pytest.fixture(params=[
    # tempo passeio, qtd kits
    (0, 1),
    (1, 2),
    (2, 3),
])
def tempo_kits(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 2/10/19
    # data do evento, tag
    ((2019, 9, 30), 'VENCIDO'),
    ((2019, 10, 1), 'VENCIDO'),
    ((2019, 10, 2), 'PRIORITARIO'),
    ((2019, 10, 3), 'PRIORITARIO'),
    ((2019, 10, 4), 'PRIORITARIO'),
    ((2019, 10, 5), 'PRIORITARIO'),
    ((2019, 10, 6), 'PRIORITARIO'),
    ((2019, 10, 7), 'LIMITE'),
    ((2019, 10, 8), 'LIMITE'),
    ((2019, 10, 9), 'LIMITE'),
    ((2019, 10, 10), 'REGULAR'),
    ((2019, 10, 11), 'REGULAR'),
    ((2019, 10, 12), 'REGULAR'),
    ((2019, 10, 13), 'REGULAR'),
])
def kits_avulsos_parametros(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 20/12/19
    # data do evento, tag
    ((2019, 12, 18), 'VENCIDO'),
    ((2019, 12, 19), 'VENCIDO'),
    ((2019, 12, 20), 'PRIORITARIO'),
    ((2019, 12, 21), 'PRIORITARIO'),
    ((2019, 12, 22), 'PRIORITARIO'),
    ((2019, 12, 23), 'PRIORITARIO'),
    ((2019, 12, 24), 'PRIORITARIO'),
    ((2019, 12, 25), 'PRIORITARIO'),
    ((2019, 12, 26), 'LIMITE'),
    ((2019, 12, 27), 'LIMITE'),
    ((2019, 12, 28), 'LIMITE'),
    ((2019, 12, 29), 'LIMITE'),
    ((2019, 12, 30), 'LIMITE'),
    ((2019, 12, 31), 'REGULAR'),
    ((2020, 1, 1), 'REGULAR')
])
def kits_avulsos_parametros2(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 3/10/19
    # data do evento, status
    ((2019, 10, 2), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 10, 1), PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO),
    ((2019, 9, 30), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
    ((2019, 9, 29), PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO),
    ((2019, 9, 28), PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO),
    ((2019, 9, 27), PedidoAPartirDaEscolaWorkflow.RASCUNHO),
    ((2019, 9, 26), PedidoAPartirDaEscolaWorkflow.DRE_PEDIU_ESCOLA_REVISAR),
])
def kits_avulsos_datas_passado_parametros(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 3/10/19
    ((2019, 10, 3)),
    ((2019, 10, 4)),
    ((2019, 10, 5)),
    ((2019, 10, 6)),
    ((2019, 10, 7)),
    ((2019, 10, 8)),
    ((2019, 10, 9)),
    ((2019, 10, 10)),
])
def kits_avulsos_datas_semana(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 3/10/19
    ((2019, 10, 3)),
    ((2019, 10, 8)),
    ((2019, 10, 10)),
    ((2019, 10, 15)),
    ((2019, 10, 20)),
    ((2019, 11, 3)),
])
def kits_avulsos_datas_mes(request):
    return request.param


@pytest.fixture(params=[
    # para testar no dia 3/10/19
    # data do evento, status
    ((2019, 10, 2), PedidoAPartirDaDiretoriaRegionalWorkflow.RASCUNHO),
    ((2019, 10, 1), PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_A_AUTORIZAR),
    ((2019, 9, 30), PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_PEDIU_DRE_REVISAR),
    ((2019, 9, 29), PedidoAPartirDaDiretoriaRegionalWorkflow.RASCUNHO),
    ((2019, 9, 28), PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_PEDIU_DRE_REVISAR),
    ((2019, 9, 27), PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_A_AUTORIZAR),
    ((2019, 9, 26), PedidoAPartirDaDiretoriaRegionalWorkflow.CODAE_PEDIU_DRE_REVISAR),
])
def kits_unificados_datas_passado_parametros(request):
    return request.param