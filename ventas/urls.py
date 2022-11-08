from django.urls import path
from ventas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('agregar/', views.VentasCreateView.as_view(), name="agregar_venta"),
   
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)