# Generated by Django 2.0.13 on 2019-08-26 18:04

import uuid

import django_xworkflows.models
from django.db import migrations, models

import sme_terceirizadas.dados_comuns.behaviors


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AlteracaoCardapio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('data_inicial', models.DateField(verbose_name='Data inicial')),
                ('data_final', models.DateField(verbose_name='Data final')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', django_xworkflows.models.StateField(max_length=34, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_APROVADO', 'DRE_PEDE_ESCOLA_REVISAR', 'DRE_CANCELA_PEDIDO_ESCOLA', 'CODAE_APROVADO', 'CODAE_CANCELOU_PEDIDO', 'TERCEIRIZADA_TOMA_CIENCIA', 'ESCOLA_PEDE_CANCELAMENTO_48H_ANTES', 'CANCELAMENTO_AUTOMATICO']))),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Alteração de cardápio',
                'verbose_name_plural': 'Alterações de cardápio',
            },
            bases=(django_xworkflows.models.BaseWorkflowEnabled, models.Model, sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, sme_terceirizadas.dados_comuns.behaviors.Logs),
        ),
        migrations.CreateModel(
            name='Cardapio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, null=True, verbose_name='Descricao')),
                ('ativo', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('data', models.DateField(verbose_name='Data')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Cardápio',
                'verbose_name_plural': 'Cardápios',
            },
        ),
        migrations.CreateModel(
            name='GrupoSuspensaoAlimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', django_xworkflows.models.StateField(max_length=25, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='InformativoPartindoDaEscolaWorkflow', states=['RASCUNHO', 'INFORMADO', 'TERCEIRIZADA_TOMA_CIENCIA']))),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Grupo de suspensão de alimentação',
                'verbose_name_plural': 'Grupo de suspensão de alimentação',
            },
            bases=(sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, django_xworkflows.models.BaseWorkflowEnabled, models.Model),
        ),
        migrations.CreateModel(
            name='InversaoCardapio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('motivo', models.TextField(blank=True, null=True, verbose_name='Motivo')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('status', django_xworkflows.models.StateField(max_length=34, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_APROVADO', 'DRE_PEDE_ESCOLA_REVISAR', 'DRE_CANCELA_PEDIDO_ESCOLA', 'CODAE_APROVADO', 'CODAE_CANCELOU_PEDIDO', 'TERCEIRIZADA_TOMA_CIENCIA', 'ESCOLA_PEDE_CANCELAMENTO_48H_ANTES', 'CANCELAMENTO_AUTOMATICO']))),
                ('observacao', models.TextField(blank=True, null=True, verbose_name='Observação')),
            ],
            options={
                'verbose_name': 'Inversão de cardápio',
                'verbose_name_plural': 'Inversão de cardápios',
            },
            bases=(sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, django_xworkflows.models.BaseWorkflowEnabled, models.Model, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade, sme_terceirizadas.dados_comuns.behaviors.Logs),
        ),
        migrations.CreateModel(
            name='MotivoAlteracaoCardapio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Motivo de alteração de cardápio',
                'verbose_name_plural': 'Motivos de alteração de cardápio',
            },
        ),
        migrations.CreateModel(
            name='MotivoSuspensao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Motivo de suspensão de alimentação',
                'verbose_name_plural': 'Motivo de suspensão de alimentação',
            },
        ),
        migrations.CreateModel(
            name='QuantidadePorPeriodoSuspensaoAlimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('numero_alunos', models.SmallIntegerField()),
            ],
            options={
                'verbose_name': 'Quantidade por período de suspensão de alimentação',
                'verbose_name_plural': 'Quantidade por período de suspensão de alimentação',
            },
        ),
        migrations.CreateModel(
            name='SubstituicoesAlimentacaoNoPeriodoEscolar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('qtd_alunos', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Substituições de alimentação no período',
                'verbose_name_plural': 'Substituições de alimentação no período',
            },
        ),
        migrations.CreateModel(
            name='SuspensaoAlimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data', models.DateField(verbose_name='Data')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('prioritario', models.BooleanField(default=False)),
                ('outro_motivo', models.CharField(blank=True, max_length=50, null=True, verbose_name='Outro motivo')),
            ],
            options={
                'verbose_name': 'Suspensão de alimentação',
                'verbose_name_plural': 'Suspensões de alimentação',
            },
        ),
        migrations.CreateModel(
            name='SuspensaoAlimentacaoNoPeriodoEscolar',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('qtd_alunos', models.PositiveSmallIntegerField(default=0)),
            ],
            options={
                'verbose_name': 'Suspensão de alimentação no período',
                'verbose_name_plural': 'Suspensões de alimentação no período',
            },
        ),
        migrations.CreateModel(
            name='TipoAlimentacao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
            ],
            options={
                'verbose_name': 'Tipo de alimentação',
                'verbose_name_plural': 'Tipos de alimentação',
            },
        ),
    ]
