# Generated by Django 4.1.1 on 2022-10-13 01:32

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ProyectoApp', '0004_type_empleado_tipo'),
    ]

    operations = [
        migrations.CreateModel(
            name='Categoria',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
            ],
            options={
                'verbose_name': 'Categoria',
                'verbose_name_plural': 'Categorias',
                'db_table': 'categoria',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Clientes',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, verbose_name='Nombre')),
                ('apellido', models.CharField(max_length=150, verbose_name='Apellidos')),
                ('dni', models.CharField(max_length=10, unique=True, verbose_name='Dni')),
                ('f_nacimiento', models.DateField(default=datetime.datetime.now, verbose_name='Fecha de nacimiento')),
                ('direccion', models.CharField(blank=True, max_length=150, null=True, verbose_name='Direccion')),
                ('sexo', models.CharField(choices=[('male', 'Masculino'), ('female', 'Femenino')], default='male', max_length=10, verbose_name='Sexo')),
            ],
            options={
                'verbose_name': 'Cliente',
                'verbose_name_plural': 'Clientes',
                'db_table': 'clientes',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Det_Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('precio', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cantidad', models.IntegerField(default=0)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
            ],
            options={
                'verbose_name': 'DVenta',
                'verbose_name_plural': 'DVentas',
                'db_table': 'dventas',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Producto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=150, unique=True, verbose_name='Nombre')),
                ('imagen', models.ImageField(blank=True, null=True, upload_to='producto/%Y,%m,%d')),
                ('pvp', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('categoria', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoApp.categoria')),
            ],
            options={
                'verbose_name': 'Producto',
                'verbose_name_plural': 'Productos',
                'db_table': 'productos',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Ventas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('f_registro', models.DateField(default=datetime.datetime.now)),
                ('subtotal', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('iva', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('total', models.DecimalField(decimal_places=2, default=0.0, max_digits=9)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoApp.clientes')),
            ],
            options={
                'verbose_name': 'Venta',
                'verbose_name_plural': 'Ventas',
                'db_table': 'ventas',
                'ordering': ['id'],
            },
        ),
        migrations.DeleteModel(
            name='Empleado',
        ),
        migrations.DeleteModel(
            name='Type',
        ),
        migrations.AddField(
            model_name='det_ventas',
            name='prod',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoApp.producto'),
        ),
        migrations.AddField(
            model_name='det_ventas',
            name='venta',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='ProyectoApp.ventas'),
        ),
    ]
