# Generated by Django 2.2.6 on 2019-10-24 14:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('perfil', '0012_auto_20191024_1127'),
    ]

    operations = [
        migrations.AlterField(
            model_name='vinculo',
            name='tipo_instituicao',
            field=models.ForeignKey(blank=True, limit_choices_to=models.Q(models.Q(('app_label', 'escola'), ('model', 'escola')), models.Q(('app_label', 'escola'), ('model', 'diretoriaregional')), models.Q(('app_label', 'escola'), ('model', 'codae')), models.Q(('app_label', 'terceirizada'), ('model', 'terceirizada')), _connector='OR'), null=True, on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType'),
        ),
    ]