# Generated by Django 4.1.1 on 2022-11-20 22:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoApp', '0009_categoria_fecha_actualizo_categoria_fecha_creacion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='producto',
            name='stock',
            field=models.IntegerField(default=0, verbose_name='Stock'),
        ),
    ]
