from django.urls import path
from ProyectoApp import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('listar/', views.CategoriaListView.as_view(), name="listar"),
    path('create/', views.CategoriaCreateView.as_view(), name="agregar"),
    path('edit/<int:pk>/', views.CategoriaUpdateView.as_view(), name="actualizar"),
    path('delete/<int:pk>/', views.CategoriaDeleteView.as_view(), name="eliminar"),
    path('form/', views.CategoriaFormView.as_view(), name="formulario"),
    
   
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)