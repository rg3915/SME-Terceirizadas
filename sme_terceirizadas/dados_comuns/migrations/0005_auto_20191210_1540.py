# Generated by Django 2.2.6 on 2019-12-10 18:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dados_comuns', '0004_logsolicitacoesusuario_resposta_sim_nao'),
    ]

    operations = [
        migrations.AlterField(
            model_name='logsolicitacoesusuario',
            name='status_evento',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Solicitação Realizada'), (1, 'CODAE autorizou'), (2, 'Terceirizada tomou ciência'), (3, 'Terceirizada recusou'), (4, 'CODAE negou'), (5, 'CODAE pediu revisão'), (6, 'DRE revisou'), (7, 'DRE validou'), (8, 'DRE pediu revisão'), (9, 'DRE não validou'), (10, 'Escola revisou'), (13, 'Escola cancelou'), (14, 'DRE cancelou'), (11, 'Questionamento pela CODAE'), (12, 'Terceirizada respondeu questionamento')]),
        ),
    ]