# Generated by Django 2.0.13 on 2019-07-31 17:04

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0004_delete_diasemana'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConfiguracaoMensagem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('tipo', models.PositiveSmallIntegerField(choices=[(0, 'Alteração de cardápio'), (1, 'Inclusão de alimentação'), (2, 'Inclusão de alimentação contínua'), (3, 'Suspensão de alimentação'), (4, 'Solicitação de kit lanche avulsa'), (5, 'Solicitação de kit lanche unificada'), (6, 'Inversão de cardápio')], unique=True)),
                ('assunto', models.CharField(blank=True, max_length=256, null=True, verbose_name='Assunto')),
                ('template_html', models.TextField(blank=True, null=True, verbose_name='Corpo')),
            ],
            options={
                'verbose_name': 'Configuração de mensagem',
                'verbose_name_plural': 'Configurações de mensagem',
            },
        ),
    ]
