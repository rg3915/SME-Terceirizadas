# Generated by Django 2.2.6 on 2019-12-06 14:13

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('cardapio', '0003_auto_20191205_1815'),
    ]

    operations = [
        migrations.AlterField(
            model_name='alteracaocardapio',
            name='status',
            field=django_xworkflows.models.StateField(max_length=37, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_QUESTIONADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE'])),
        ),
        migrations.AlterField(
            model_name='inversaocardapio',
            name='status',
            field=django_xworkflows.models.StateField(max_length=37, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_QUESTIONADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE'])),
        ),
    ]
