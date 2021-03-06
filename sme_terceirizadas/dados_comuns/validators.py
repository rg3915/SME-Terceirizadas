import datetime

from django.db import models
from rest_framework import serializers
from workalendar.america import BrazilSaoPauloCity

from .constants import obter_dias_uteis_apos_hoje
from .utils import eh_dia_util

calendario = BrazilSaoPauloCity()


def nao_pode_ser_no_passado(data: datetime.date):
    if data < datetime.date.today():
        raise serializers.ValidationError('Não pode ser no passado')
    return True


def deve_ser_no_passado(data: datetime.date):
    if data > datetime.date.today():
        raise serializers.ValidationError('Deve ser data anterior a hoje')
    return True


def deve_pedir_com_antecedencia(dia: datetime.date, dias: int = 2):
    prox_dia_util = obter_dias_uteis_apos_hoje(quantidade_dias=dias)
    if dia < prox_dia_util:
        raise serializers.ValidationError(f'Deve pedir com pelo menos {dias} dias úteis de antecedência')
    return True


def deve_existir_cardapio(escola, data: datetime.date):
    if not escola.get_cardapio(data):
        raise serializers.ValidationError(f'Escola não possui cardápio para esse dia: {data.strftime("%d-%m-%Y")}')
    return True


def dia_util(data: datetime.date):
    if not eh_dia_util(data):
        raise serializers.ValidationError('Não é dia útil em São Paulo')
    return True


def verificar_se_existe(obj_model, **kwargs) -> bool:
    try:
        if not issubclass(obj_model, models.Model):
            raise TypeError('obj_model deve ser um "django models class"')
    except TypeError:
        raise TypeError('obj_model deve ser um "django models class"')
    existe = obj_model.objects.filter(**kwargs).exists()
    return existe


def objeto_nao_deve_ter_duplicidade(obj_model, mensagem='Objeto já existe', **kwargs, ):
    qtd = obj_model.objects.filter(**kwargs).count()
    if qtd:
        raise serializers.ValidationError(mensagem)


def nao_pode_ser_feriado(data: datetime.date, mensagem='Não pode ser no feriado'):
    if calendario.is_holiday(data):
        raise serializers.ValidationError(mensagem)


def campo_nao_pode_ser_nulo(valor, mensagem='Não pode ser nulo'):
    if not valor:
        raise serializers.ValidationError(mensagem)


def campo_deve_ser_deste_tipo(valor, tipo=str, mensagem='Deve ser do tipo texto'):
    if type(valor) is not tipo:
        raise serializers.ValidationError(mensagem)


def deve_ser_no_mesmo_ano_corrente(data_inversao: datetime.date):
    ano_corrente = datetime.date.today().year
    if ano_corrente != data_inversao.year:
        raise serializers.ValidationError(
            'Inversão de dia de cardapio deve ser solicitada no ano corrente'
        )
    return True


def deve_ter_extensao_valida(nome: str):
    if nome.split('.')[len(nome.split('.')) - 1].lower() not in ['doc', 'docx', 'pdf', 'png', 'jpg', 'jpeg']:
        raise serializers.ValidationError('Extensão inválida')
    return nome
