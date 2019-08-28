"""
    Antes de rodar isso vc deve ter rodado as escolas e as fixtures
"""
import datetime
import random

from faker import Faker

from sme_pratoaberto_terceirizadas.cardapio.models import TipoAlimentacao
from sme_pratoaberto_terceirizadas.escola.models import Escola, DiretoriaRegional, PeriodoEscolar
from sme_pratoaberto_terceirizadas.inclusao_alimentacao.models import InclusaoAlimentacaoContinua, \
    MotivoInclusaoContinua, GrupoInclusaoAlimentacaoNormal, QuantidadePorPeriodo, InclusaoAlimentacaoNormal, \
    MotivoInclusaoNormal
from sme_pratoaberto_terceirizadas.perfil.models import Usuario

f = Faker('pt-br')
f.seed(420)
hoje = datetime.datetime.today()


def vincula_dre_escola_usuario():
    dres = DiretoriaRegional.objects.filter(id__lte=5)
    escolas = Escola.objects.filter(id__lte=5)
    for dre in dres:
        dre.escolas.set(escolas)
    usuario = Usuario.objects.first()
    usuario.diretorias_regionais.set(dres)
    usuario.escolas.set(escolas)


def _get_random_motivo_continuo():
    return MotivoInclusaoContinua.objects.order_by("?").first()


def _get_random_motivo_normal():
    return MotivoInclusaoNormal.objects.order_by("?").first()


def _get_random_escola():
    return Escola.objects.filter(id__lte=5).order_by("?").first()


def _get_random_dre():
    return DiretoriaRegional.objects.filter(id__lte=5).order_by("?").first()


def _get_random_periodo_escolar():
    return PeriodoEscolar.objects.order_by("?").first()


def _get_random_tipos_alimentacao():
    num_alimentacoes = random.randint(2, 5)
    alimentacoes = []
    for i in range(num_alimentacoes):
        alim = TipoAlimentacao.objects.order_by("?").first()
        alimentacoes.append(alim)
    return alimentacoes


def fluxo_escola_felix(obj, user):
    print(f'aplicando fluxo feliz em {obj}')
    obj.inicia_fluxo(user=user, notificar=True)
    if random.random() >= 0.1:
        obj.dre_aprovou(user=user, notificar=True)
        if random.random() >= 0.2:
            obj.codae_aprovou(user=user, notificar=True)
            if random.random() >= 0.3:
                obj.terceirizada_tomou_ciencia(user=user, notificar=True)


def fluxo_escola_loop(obj, user):
    print(f'aplicando fluxo loop revisao dre-escola em {obj}')
    obj.inicia_fluxo(user=user, notificar=True)
    obj.dre_pediu_revisao(user=user, notificar=True)
    obj.escola_revisou(user=user, notificar=True)
    obj.dre_aprovou(user=user, notificar=True)


def cria_inclusoes_continuas(qtd=50):
    user = Usuario.objects.first()
    for i in range(qtd):
        inclusao_continua = InclusaoAlimentacaoContinua.objects.create(
            motivo=_get_random_motivo_continuo(),
            escola=_get_random_escola(),
            outro_motivo=f.text()[:20],
            descricao=f.text()[:160], criado_por=user,
            dias_semana=[1, 4, 5],
            data_inicial=hoje + datetime.timedelta(
                days=random.randint(1, 30)),
            data_final=hoje + datetime.timedelta(
                days=random.randint(100, 200)))

        q = QuantidadePorPeriodo.objects.create(
            periodo_escolar=_get_random_periodo_escolar(),
            numero_alunos=random.randint(10, 200),
            inclusao_alimentacao_continua=inclusao_continua
        )
        q.tipos_alimentacao.set(_get_random_tipos_alimentacao())

        fluxo_escola_felix(inclusao_continua, user)


def cria_inclusoes_normais(qtd=50):
    user = Usuario.objects.first()
    for i in range(qtd):
        grupo_inclusao_normal = GrupoInclusaoAlimentacaoNormal.objects.create(
            descricao=f.text()[:160],
            criado_por=user,
            escola=_get_random_escola()
        )
        q = QuantidadePorPeriodo.objects.create(
            periodo_escolar=_get_random_periodo_escolar(),
            numero_alunos=random.randint(10, 200),
            grupo_inclusao_normal=grupo_inclusao_normal
        )
        q.tipos_alimentacao.set(_get_random_tipos_alimentacao())
        InclusaoAlimentacaoNormal.objects.create(
            motivo=_get_random_motivo_normal(),
            outro_motivo=f.text()[:40],
            grupo_inclusao=grupo_inclusao_normal,
            data=hoje + datetime.timedelta(days=random.randint(1, 30))
        )
        fluxo_escola_felix(grupo_inclusao_normal, user)


print('-> vinculando escola dre e usuarios')
vincula_dre_escola_usuario()
print('-> criando inclusoes continuas')
cria_inclusoes_continuas()
print('-> criando inclusoes normais')
cria_inclusoes_normais()
