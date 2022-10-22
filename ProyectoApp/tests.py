from Proyecto.wsgi import *
from ProyectoApp.models import *
import random

# # select * from tabla
# query = Type.objects.all()
# print(query)

# # insercion
# #t = Type(nombre='Ing')
# #t.nombre = 'Abogado'
# #t.save()

# # edicion
# t= Type.objects.get(id=3)
# t.nombre = 'Messi'
# t.save()

# #eliminar
# t = Type.objects.get(pk=2)
# t.delete()


#palabras que tengas un e, empiezen con M, ver la consulta sql
# obj = Type.objects.filter(nombre__contains='e')
# obj = Type.objects.filter(nombre__startswith='M')
# obj = Type.objects.filter(nombre__startswith='M').query
# print(obj)

print(Categoria.objects.all())


data = ['Leche y derivados', 'Carnes, pescados y huevos', 'Patatas, legumbres, frutos secos',
        'Verduras y Hortalizas', 'Frutas', 'Cereales y derivados, azucar y dulces',
        'Grasas, aceite y mantequill']

# for i in data:
#     cat = Categoria(nombre=i)
#     cat.save()
#     print('Guardado n{}'.format(cat.id))


letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']

for i in range(1, 6000):
    name = ''.join(random.choices(letters, k=5))
    while Categoria.objects.filter(nombre=name).exists():
        name = ''.join(random.choices(letters, k=5))
    Categoria(nombre=name).save()
    print('Guardado registro {}'.format(i))