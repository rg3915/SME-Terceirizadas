# Generated by Django 2.0.13 on 2019-07-17 13:11

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('escola', '0008_auto_20190716_1656'),
    ]

    operations = [
        migrations.AddField(
            model_name='diretoriaregional',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='escola',
            name='usuarios',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
    ]
