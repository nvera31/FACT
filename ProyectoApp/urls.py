from django.urls import path
from ProyectoApp import views
from producto.views import *
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('listar/', views.CategoriaListView.as_view(), name="listar"),
    path('create/', views.CategoriaCreateView.as_view(), name="agregar"),
    path('edit/<int:pk>/', views.CategoriaUpdateView.as_view(), name="actualizar"),
    path('delete/<int:pk>/', views.CategoriaDeleteView.as_view(), name="eliminar"),
    path('form/', views.CategoriaFormView.as_view(), name="formulario"),
    
   #PRODUCTO
    path('producto/lista/', ProductoListView.as_view(), name='product_list'),
    path('producto/add/', ProductoCreateView.as_view(), name='product_create'),
    path('producto/update/<int:pk>/', ProductoUpdateView.as_view(), name='product_update'),
    path('producto/delete/<int:pk>/', ProductoDeleteView.as_view(), name='product_delete'),
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)