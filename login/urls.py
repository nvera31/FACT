from django.urls import path
from login import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.LoginFormView.as_view(), name="login"),
    #path('logout/', views.LogoutView.as_view(), name="logout"),
    path('logout/', views.LogoutRedirectView.as_view(), name="logout"),
        
   
]

