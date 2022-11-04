from email.policy import default
from enum import unique
from random import choices
from tabnanny import verbose
from unittest.util import _MAX_LENGTH
from django.db import models
from datetime import datetime
from crum import get_current_user
from django.forms.models import model_to_dict
from Proyecto.settings import MEDIA_URL, STATIC_URL
from ProyectoApp.choices import gender_choices
from Proyecto.models import BaseModel
# Create your models here.
#Primera Practica
# class Type(models.Model):
#     nombre = models.CharField(max_length=150, verbose_name='Nombre')

#     def __str__(self):
#         return self.nombre

#     class Meta:
#         verbose_name = 'Tipo'
#         verbose_name_plural = 'Tipos'
#         db_table = 'tipo'
#         ordering = ['id']

# class Empleado(models.Model):
#     tipo = models.ForeignKey(Type, on_delete=models.CASCADE)
#     nombres = models.CharField(max_length=150, verbose_name='Nombres')
#     dni = models.CharField(max_length=10,unique=True, verbose_name='Cedula')
#     fecha = models.DateField(default=datetime.now, verbose_name='Fecha de Registro')
#     f_creacion = models.DateTimeField(auto_now=True)
#     f_actualizada = models.DateTimeField(auto_now_add=True)
#     edad = models.PositiveIntegerField(default=0)
#     salario = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)
#     estado = models.BooleanField(default=True)
#    # sexo = models.CharField(max_length=15)
#     avatar = models.ImageField(upload_to='avatar/%Y/%m/%d', null=True, blank=True)
#     curriculo = models.FileField(upload_to='vitae/%Y/%m/%d', null=True, blank=True)

#     def __str__(self):
#         return self.nombres

#     class Meta:
#         verbose_name = 'Empleado'
#         verbose_name_plural = 'Empleados'
#         db_table = 'empleado'
#         ordering = ['id']

#Tablas Finales
class Categoria(BaseModel):
    nombre =models.CharField(max_length=150, verbose_name= 'Nombre', unique=True)
    desc = models.CharField(max_length=500, verbose_name= 'Descripcion', null=True, blank=True)

    def __str__(self):
        return self.nombre

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
       user = get_current_user()
       if user is not None:
          if not self.pk:
            self.user_creador = user
          else:
            self.user_actualizo = user
       super(Categoria, self).save()


    def toJSON(self):
        item = model_to_dict(self)        
        return item

    class Meta:
        verbose_name = 'Categoria'
        verbose_name_plural = 'Categorias'
        db_table = 'categoria'
        ordering = ['id']

class Producto(models.Model):
    nombre = models.CharField(max_length=150, verbose_name= 'Nombre', unique=True)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    imagen = models.ImageField(upload_to="producto", null=True, blank=True)
    pvp = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)

    def __str__(self):
        return self.nombre

#CONTENIDO NUEVO
    def toJSON(self):
        item = model_to_dict(self)
        item['categoria'] = self.categoria.toJSON()
        item['imagen'] = self.get_image()
        item['pvp'] = format(self.pvp, '.2f')
        return item


    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'
        db_table = 'productos'
        ordering = ['id']

class Clientes(models.Model):
    nombre = models.CharField(max_length=150, verbose_name= 'Nombre')
    apellido = models.CharField(max_length=150, verbose_name= 'Apellidos')
    dni = models.CharField(max_length=10, unique=True, verbose_name= 'Dni')
    f_nacimiento = models.DateField(default=datetime.now, verbose_name= 'Fecha de nacimiento')
    direccion = models.CharField(max_length=150, null=True, blank=True, verbose_name='Direccion')
    sexo = models.CharField(max_length=10, choices=gender_choices, default='male', verbose_name='Sexo')

    def __str__(self):
        return self.nombre
#RETORNA UN DICCIONARIO
    def toJSON(self):
        item = model_to_dict(self)
        item['sexo'] = {'id': self.sexo, 'nombre': self.get_sexo_display()}
        item['f_nacimiento'] = self.f_nacimiento.strftime('%Y-%m-%d')
        return item

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        db_table = 'clientes'
        ordering = ['id']

class Ventas(models.Model):
    cliente = models.ForeignKey(Clientes, on_delete=models.CASCADE)
    f_registro = models.DateField(default=datetime.now)
    subtotal = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    iva = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    total = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return self.cliente.nombre

    class Meta:
        verbose_name = 'Venta'
        verbose_name_plural = 'Ventas'
        db_table = 'ventas'
        ordering = ['id']

class Det_Ventas(models.Model):
    venta = models.ForeignKey(Ventas, on_delete=models.CASCADE)
    prod = models.ForeignKey(Producto, on_delete=models.CASCADE)
    precio = models.DecimalField(default=0.0, max_digits=9, decimal_places=2)
    cantidad = models.IntegerField(default=0)
    subtotal = models.DecimalField(default=0.00, max_digits=9, decimal_places=2)


    def __str__(self):
        return self.prod.nombre

    class Meta:
        verbose_name = 'DVenta'
        verbose_name_plural = 'DVentas'
        db_table = 'dventas'
        ordering = ['id']