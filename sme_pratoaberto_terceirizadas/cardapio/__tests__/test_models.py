import pytest
from model_mommy import mommy
from xworkflows.base import InvalidTransitionError

from ...cardapio.models import Cardapio
from ...dados_comuns.fluxo_status import PedidoAPartirDaEscolaWorkflow
from ...escola.models import Escola

pytestmark = pytest.mark.django_db


def test_motivo_alteracao_cardapio(motivo_alteracao_cardapio):
    assert motivo_alteracao_cardapio.nome is not None


def test_alteracao_cardapio(alteracao_cardapio):
    assert alteracao_cardapio.data_inicial is not None
    assert alteracao_cardapio.data_final is not None
    assert alteracao_cardapio.observacao == 'teste'
    assert alteracao_cardapio.status is not None


def test_substituicoes_alimentacao_periodo(substituicoes_alimentacao_periodo):
    assert substituicoes_alimentacao_periodo.qtd_alunos is not None
    assert substituicoes_alimentacao_periodo.alteracao_cardapio is not None
    assert substituicoes_alimentacao_periodo.alteracao_cardapio.substituicoes is not None


def test_inversao_dia_cardapio(inversao_dia_cardapio):
    assert isinstance(inversao_dia_cardapio.escola, Escola)
    assert isinstance(inversao_dia_cardapio.cardapio_de, Cardapio)
    assert isinstance(inversao_dia_cardapio.cardapio_para, Cardapio)
    assunto, template_html = inversao_dia_cardapio.template_mensagem
    assert assunto == 'TESTE INVERSAO CARDAPIO'
    assert '98DC7' in template_html
    assert 'RASCUNHO' in template_html


def test_inversao_dia_cardapio_fluxo(inversao_dia_cardapio):
    fake_user = mommy.make('perfil.Usuario')
    inversao_dia_cardapio.inicia_fluxo(user=fake_user)
    assert str(inversao_dia_cardapio.status) == PedidoAPartirDaEscolaWorkflow.DRE_A_VALIDAR
    inversao_dia_cardapio.dre_aprovou(user=fake_user)
    assert str(inversao_dia_cardapio.status) == PedidoAPartirDaEscolaWorkflow.DRE_VALIDADO


def test_inclusao_alimentacao_continua_fluxo_erro(inversao_dia_cardapio):
    # TODO: pedir incremento do fluxo para testá-lo por completo
    with pytest.raises(InvalidTransitionError,
                       match="Transition 'dre_pediu_revisao' isn't available from state 'RASCUNHO'."):
        inversao_dia_cardapio.dre_pediu_revisao()
