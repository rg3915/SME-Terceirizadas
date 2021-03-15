# Generated by Django 2.2.13 on 2021-03-15 14:23

import django_xworkflows.models
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('logistica', '0020_auto_20210311_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solicitacaoremessa',
            name='status',
            field=django_xworkflows.models.StateField(max_length=31, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='AGUARDANDO_ENVIO', name='SolicitacaoRemessaWorkFlow', states=['AGUARDANDO_ENVIO', 'DILOG_ENVIA', 'CANCELADA', 'DISTRIBUIDOR_CONFIRMA', 'DISTRIBUIDOR_SOLICITA_ALTERACAO', 'DILOG_ACEITA_ALTERACAO'])),
        ),
    ]
