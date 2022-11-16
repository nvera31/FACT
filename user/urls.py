from django.urls import path
from user import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('listar/', views.UsuarioListView.as_view(), name="listar_usuarios"),
    path('agregar/', views.UsuarioCreateView.as_view(), name="crear_usuarios"),
    path('editar/<int:pk>/', views.UsuarioUpdateView.as_view(), name="editar_usuarios"),
    path('eliminar/<int:pk>/', views.UsuarioDeleteView.as_view(), name="eliminar_usuarios"),
    path('grupo/<int:pk>/', views.Perfil.as_view(), name="perfil_usuarios"),
    path('perfil/', views.UsuarioPerfilView.as_view(), name="perfil"),
    path('password/', views.UsuarioPasswordView.as_view(), name="password"),
    
    
]
