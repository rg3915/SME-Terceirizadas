# Generated by Django 2.2.6 on 2019-10-23 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0009_auto_20191023_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinculo',
            name='data_final',
            field=models.DateField(blank=True, null=True, verbose_name='Data final'),
        ),
    ]