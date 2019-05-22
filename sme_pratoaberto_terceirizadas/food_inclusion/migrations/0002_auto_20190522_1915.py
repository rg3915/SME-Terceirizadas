# Generated by Django 2.0.13 on 2019-05-22 22:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('food_inclusion', '0001_initial'),
        ('school', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='foodinclusiondescription',
            name='period',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='school.SchoolPeriod'),
        ),
        migrations.AddField(
            model_name='foodinclusiondayreason',
            name='food_inclusion',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='food_inclusion.FoodInclusion'),
        ),
        migrations.AddField(
            model_name='foodinclusiondayreason',
            name='reason',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='food_inclusion.FoodInclusionReason'),
        ),
    ]
