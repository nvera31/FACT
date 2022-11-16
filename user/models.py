from distutils.command.upload import upload
from django.db import models
from django.contrib.auth.models import AbstractUser
from Proyecto.settings import MEDIA_URL, STATIC_URL
from django.forms import model_to_dict
from crum import get_current_request

# Create your models here.
class User(AbstractUser):
    imagen = models.ImageField(upload_to='users/%Y/%m/%d', null=True, blank=True)

    def get_image(self):
        if self.imagen:
            return '{}{}'.format(MEDIA_URL, self.imagen)
        return '{}{}'.format(STATIC_URL, 'img/empty.png')

    def toJSON(self):
        item =  model_to_dict(self, exclude=['password','groups', 'user_permissions', 'last_login'])
        if self.last_login:
            item['last_login'] =  self.last_login.strftime('%Y-%m-%d')
        item['date_joined'] =  self.date_joined.strftime('%Y-%m-%d')
        item['imagen'] =  self.get_image()
        item['full_name'] =  self.get_full_name()
        item['groups'] =  [{'id': g.id, 'name': g.name} for g in self.groups.all()]
        return item

    def get_group_session(self):
        try:
            request = get_current_request()
            groups = self.groups.all()
            if groups.exists():
                if 'group' not in request.session:
                    request.session['group'] = groups[0]
        except:
            pass


    #ENCRIPTAR CLAVE
    # def save(self, *args, **kwargs):
    #     if self.pk is None:
    #         self.set_password(self.password)
    #     else:
    #         user = User.objects.get(pk=self.pk)
    #         if user.password != self.password:
    #             self.set_password(self.password)
    #     super().save(*args, **kwargs)
