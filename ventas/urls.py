from django.urls import path
from ventas import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('listar/', views.VentasListView.as_view(), name="listar_venta"),
    path('agregar/', views.VentasCreateView.as_view(), name="agregar_venta"),
    path('actualizar/<int:pk>/', views.VentasUpdateView.as_view(), name="actualizar_venta"),
    path('eliminar/<int:pk>/', views.VentasDeleteView.as_view(), name="eliminar_venta"),
    path('factura/pdf/<int:pk>/', views.VentasFacturaPdfView.as_view(), name="pdf_venta"),
   
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)