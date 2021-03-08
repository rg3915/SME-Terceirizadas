# Generated by Django 2.2.6 on 2021-02-04 16:20

import environ
from django.db import migrations

ROOT_DIR = environ.Path(__file__) - 2

sql_path = ROOT_DIR.path('sql', '0013_solicitacoes.sql')
with open(sql_path, 'r') as f:
    sql = f.read()


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ('paineis_consolidados', '0012_solicitacoes'),
    ]

    operations = [
        migrations.RunSQL(sql),
    ]