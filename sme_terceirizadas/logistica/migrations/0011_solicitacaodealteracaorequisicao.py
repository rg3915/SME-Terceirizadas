# Generated by Django 2.2.13 on 2021-01-20 19:26

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import multiselectfield.db.fields
import sme_terceirizadas.dados_comuns.behaviors
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('logistica', '0010_auto_20210114_1715'),
    ]

    operations = [
        migrations.CreateModel(
            name='SolicitacaoDeAlteracaoRequisicao',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('alterado_em', models.DateTimeField(auto_now=True, verbose_name='Alterado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('motivo', multiselectfield.db.fields.MultiSelectField(choices=[('ALTERAR_DATA_ENTREGA', 'Alterar data de entrega'), ('ALTERAR_QTD_ALIMENTO', 'Alterar quantidade de alimento'), ('ALTERAR_ALIMENTO', 'Alterar alimento'), ('OUTROS', 'Outros')], max_length=65)),
                ('justificativa', models.TextField(verbose_name='Motivo')),
                ('data', models.DateField()),
                ('hora', models.TimeField()),
                ('requisicao', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solicitacoes_de_alteracao', to='logistica.SolicitacaoRemessa')),
                ('usuario_solicitante', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model, sme_terceirizadas.dados_comuns.behaviors.TemIdentificadorExternoAmigavel),
        ),
    ]
