# Generated by Django 2.0.13 on 2019-05-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Address',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('street_name', models.CharField(max_length=256, verbose_name='Street name')),
                ('complement', models.CharField(max_length=30, verbose_name='Complement')),
                ('district', models.CharField(max_length=60, verbose_name='District')),
                ('number', models.CharField(max_length=20, verbose_name='Number')),
                ('postal_code', models.CharField(max_length=9, verbose_name='Postal code')),
                ('lat', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
                ('lon', models.DecimalField(decimal_places=6, max_digits=9, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='CityLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city', models.CharField(default='São Paulo', max_length=80, verbose_name='City')),
                ('state', models.CharField(default='SP', max_length=2, verbose_name='UF')),
            ],
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('name', models.CharField(max_length=80, verbose_name='Name')),
                ('phone', models.CharField(max_length=11, null=True, verbose_name='Phone')),
                ('mobile_phone', models.CharField(max_length=11, null=True, verbose_name='Mobile phone')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='LogEventData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Name')),
                ('description', models.TextField(blank=True, max_length=256, null=True, verbose_name='Description')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
