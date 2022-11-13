from django.urls import path
from index import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('index/', views.InicioView.as_view(), name="Home"),
    
    
   
]

#urlpatterns+=static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)