from django.urls import path
from clientes import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('listar/', views.ClienteListView.as_view(), name="listar_cliente"),
    path('agregar/', views.ClienteCreateView.as_view(), name="agregar_cliente"),
    path('actualizar/<int:pk>/', views.ClienteUpdateView.as_view(), name="actualizar_cliente"),
    path('eliminar/<int:pk>/', views.ClienteDeleteView.as_view(), name="eliminar_cliente"),
    
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)