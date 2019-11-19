# Generated by Django 2.0.13 on 2019-08-26 18:04

import uuid

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models

import sme_terceirizadas.dados_comuns.behaviors


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('dados_comuns', '0001_initial'),
        ('escola', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Contrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('numero', models.CharField(max_length=100, verbose_name='No do contrato')),
                ('processo', models.CharField(help_text='Processo administrativo do contrato', max_length=100, verbose_name='Processo Administrativo')),
                ('data_proposta', models.DateField(verbose_name='Data da proposta')),
                ('diretorias_regionais', models.ManyToManyField(related_name='contratos_da_diretoria_regional', to='escola.DiretoriaRegional')),
            ],
            options={
                'verbose_name': 'Contrato',
                'verbose_name_plural': 'Contratos',
            },
        ),
        migrations.CreateModel(
            name='Edital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('numero', models.CharField(help_text='Número do Edital', max_length=100, unique=True, verbose_name='Edital No')),
                ('tipo_contratacao', models.CharField(max_length=100, verbose_name='Tipo de contratação')),
                ('processo', models.CharField(help_text='Processo administrativo do edital', max_length=100, verbose_name='Processo Administrativo')),
                ('objeto', models.TextField(verbose_name='objeto resumido')),
            ],
            options={
                'verbose_name': 'Edital',
                'verbose_name_plural': 'Editais',
            },
        ),
        migrations.CreateModel(
            name='Nutricionista',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(blank=True, max_length=50, null=True, verbose_name='Nome')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('crn_numero', models.CharField(blank=True, max_length=160, null=True, verbose_name='Nutricionista crn')),
            ],
            options={
                'verbose_name': 'Nutricionista',
                'verbose_name_plural': 'Nutricionistas',
            },
        ),
        migrations.CreateModel(
            name='Terceirizada',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ativo', models.BooleanField(default=True, verbose_name='Está ativo?')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('nome_fantasia', models.CharField(blank=True, max_length=160, null=True, verbose_name='Nome fantasia')),
                ('razao_social', models.CharField(blank=True, max_length=160, null=True, verbose_name='Razao social')),
                ('cnpj', models.CharField(max_length=14, validators=[django.core.validators.MinLengthValidator(14)], verbose_name='CNPJ')),
                ('representante_legal', models.CharField(blank=True, max_length=160, null=True, verbose_name='Representante legal')),
                ('representante_contato', models.CharField(blank=True, max_length=160, null=True, verbose_name='Representante contato (email/tel)')),
                ('contatos', models.ManyToManyField(blank=True, to='dados_comuns.Contato')),
                ('endereco', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dados_comuns.Endereco')),
                ('usuarios', models.ManyToManyField(blank=True, related_name='terceirizadas', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Terceirizada',
                'verbose_name_plural': 'Terceirizadas',
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel),
        ),
        migrations.CreateModel(
            name='VigenciaContrato',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_inicial', models.DateField(verbose_name='Data inicial')),
                ('data_final', models.DateField(verbose_name='Data final')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('contrato', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='vigencias', to='terceirizada.Contrato')),
            ],
            options={
                'verbose_name': 'Vigência de contrato',
                'verbose_name_plural': 'Vigências de contrato',
            },
        ),
        migrations.AddField(
            model_name='nutricionista',
            name='terceirizada',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='nutricionistas', to='terceirizada.Terceirizada'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='edital',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='contratos', to='terceirizada.Edital'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='lotes',
            field=models.ManyToManyField(related_name='contratos_do_lote', to='escola.Lote'),
        ),
        migrations.AddField(
            model_name='contrato',
            name='terceirizadas',
            field=models.ManyToManyField(related_name='contratos_da_terceirizada', to='terceirizada.Terceirizada'),
        ),
    ]
