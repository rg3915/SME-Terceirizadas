# Generated by Django 2.2.6 on 2019-10-22 17:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0005_usuario_vinculo_funcional'),
    ]

    operations = [
        migrations.AddField(
            model_name='usuario',
            name='cpf',
            field=models.CharField(default='', max_length=11, verbose_name='CPF'),
        ),
    ]
