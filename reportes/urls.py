from django.urls import path
from reportes import views

urlpatterns = [
    path('venta/', views.ReportesVentasView.as_view(), name='reportes'),
    
    
]