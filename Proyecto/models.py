from django.db import models
from django.conf import settings

class BaseModel(models.Model):
    user_creador = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_creador',null=True, blank=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    user_actualizo = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user_actualizo',null=True, blank=True)
    fecha_actualizo = models.DateTimeField(auto_now=True, null=True, blank=True)

    class Meta:
        abstract = True