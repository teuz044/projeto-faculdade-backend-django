# Generated by Django 4.2.6 on 2023-11-22 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_remove_acidente_id_alter_acidente_data_hora_boletim_and_more'),
    ]

    operations = [

        migrations.AlterField(
            model_name='acidente',
            name='data_hora_boletim',
            field=models.CharField(db_column='data_hora_boletim', max_length=255),
        ),
        migrations.AlterField(
            model_name='acidente',
            name='nascimento',
            field=models.CharField(db_column='nascimento', max_length=255),
        ),
        migrations.AlterField(
            model_name='acidente',
            name='num_boletim',
            field=models.CharField(db_column='num_boletim', max_length=255, serialize=False, unique=True),
        ),
        migrations.AlterModelTable(
            name='acidente',
            table='acidente',
        ),
    ]
