# Generated by Django 2.0.13 on 2019-09-13 13:37

from django.db import migrations
import django_xworkflows.models


class Migration(migrations.Migration):

    dependencies = [
        ('kit_lanche', '0007_auto_20190913_1021'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaokitlancheunificada',
            name='status',
            field=django_xworkflows.models.StateField(max_length=26, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaDiretoriaRegionalWorkflow', states=['RASCUNHO', 'CODAE_A_AUTORIZAR', 'DRE_PEDE_ESCOLA_REVISAR', 'CODAE_NEGOU_PEDIDO', 'CODAE_AUTORIZADO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'CANCELAMENTO_AUTOMATICO', 'DRE_CANCELOU'])),
        ),
    ]