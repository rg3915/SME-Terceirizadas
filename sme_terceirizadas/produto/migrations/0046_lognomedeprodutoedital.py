# Generated by Django 2.2.13 on 2020-12-29 17:43

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('produto', '0045_auto_20201229_1712'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogNomeDeProdutoEdital',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('criado_em', models.DateTimeField(auto_now_add=True, verbose_name='Criado em')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('acao', models.CharField(blank=True, choices=[('a', 'ativar'), ('i', 'inativar')], max_length=1, null=True, verbose_name='ação')),
                ('criado_por', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('nome_de_produto_edital', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='produto.NomeDeProdutoEdital')),
            ],
            options={
                'verbose_name': 'Log de Produto proveniente do Edital',
                'verbose_name_plural': 'Log de Produtos provenientes do Edital',
                'ordering': ('-criado_em',),
            },
        ),
    ]
