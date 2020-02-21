# Generated by Django 2.2.8 on 2020-02-19 14:09

import uuid

import django.core.validators
import django.db.models.deletion
import django_xworkflows.models
from django.conf import settings
from django.db import migrations, models

import sme_terceirizadas.dados_comuns.behaviors


class Migration(migrations.Migration):

    dependencies = [
        ('terceirizada', '0003_auto_20191213_1339'),
        ('escola', '0012_faixaetaria_mudancafaixasetarias'),
        ('cardapio', '0013_remove_tipoalimentacao_substituicoes'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('inclusao_alimentacao', '0006_auto_20200129_1503'),
    ]

    operations = [
        migrations.CreateModel(
            name='InclusaoAlimentacaoDaCEI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descricao', models.TextField(blank=True, verbose_name='Descricao')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('data', models.DateField(verbose_name='Data')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('foi_solicitado_fora_do_prazo', models.BooleanField(default=False, verbose_name='Solicitação foi criada em cima da hora (5 dias úteis ou menos)?')),
                ('status', django_xworkflows.models.StateField(max_length=37, workflow=django_xworkflows.models._SerializedWorkflow(initial_state='RASCUNHO', name='PedidoAPartirDaEscolaWorkflow', states=['RASCUNHO', 'DRE_A_VALIDAR', 'DRE_VALIDADO', 'DRE_PEDIU_ESCOLA_REVISAR', 'DRE_NAO_VALIDOU_PEDIDO_ESCOLA', 'CODAE_AUTORIZADO', 'CODAE_QUESTIONADO', 'CODAE_NEGOU_PEDIDO', 'TERCEIRIZADA_RESPONDEU_QUESTIONAMENTO', 'TERCEIRIZADA_TOMOU_CIENCIA', 'ESCOLA_CANCELOU', 'CANCELADO_AUTOMATICAMENTE']))),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('escola', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='grupos_inclusoes_por_cei', to='escola.Escola')),
                ('motivo', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inclusao_alimentacao.MotivoInclusaoNormal')),
                ('periodo_escolar', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='escola.PeriodoEscolar')),
                ('rastro_dre', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inclusao_alimentacao_inclusaoalimentacaodacei_rastro_dre', to='escola.DiretoriaRegional')),
                ('rastro_escola', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inclusao_alimentacao_inclusaoalimentacaodacei_rastro_escola', to='escola.Escola')),
                ('rastro_lote', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inclusao_alimentacao_inclusaoalimentacaodacei_rastro_lote', to='escola.Lote')),
                ('rastro_terceirizada', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='inclusao_alimentacao_inclusaoalimentacaodacei_rastro_terceirizada', to='terceirizada.Terceirizada')),
                ('tipos_alimentacao', models.ManyToManyField(to='cardapio.ComboDoVinculoTipoAlimentacaoPeriodoTipoUE')),
            ],
            options={
                'verbose_name': 'Inclusão de alimentação da CEI',
                'verbose_name_plural': 'Inclusões de alimentação da CEI',
            },
            bases=(django_xworkflows.models.BaseWorkflowEnabled, models.Model, sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel, sme_terceirizadas.dados_comuns.behaviors.Logs, sme_terceirizadas.dados_comuns.behaviors.TemPrioridade),
        ),
        migrations.CreateModel(
            name='QuantidadeDeAlunosPorFaixaEtariaDaInclusaoDeAlimentacaoDaCEI',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('quantidade_alunos', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1)])),
                ('faixa_etaria', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='escola.FaixaEtaria')),
                ('inclusao_alimentacao_da_cei', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='inclusao_alimentacao.InclusaoAlimentacaoDaCEI')),
            ],
            options={
                'verbose_name': 'Quantidade de alunos por faixa etária da inclusao de alimentação',
                'verbose_name_plural': 'Quantidade de alunos por faixa etária da inclusao de alimentação',
            },
        ),
    ]
