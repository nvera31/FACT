from multiprocessing import AuthenticationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from django.urls import reverse_lazy
from django.views.generic import FormView, RedirectView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
import Proyecto.settings as setting
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from login.forms import *
import uuid
import smtplib
from Proyecto.wsgi import *
from Proyecto import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from user.models import User
from django.template.loader import render_to_string

# Create your views here.

class LoginFormView(LoginView):
    template_name = "login/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(setting.LOGIN_REDIRECT_URL)
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesion'
        return context


class LoginFormView2(FormView):
    form_class = AuthenticationForm
    template_name = "login/login.html"
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(self.success_url)
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        login(self.request, form.get_user())
        return HttpResponseRedirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Iniciar sesion'
        return context


class LogoutRedirectView(RedirectView):
    pattern_name = 'login'

    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return super().dispatch(request, *args, **kwargs)

#RESETEO DE CONTRASEÑA
class ReseteoPasswordView(FormView):
    form_class = ReseteoPasswordForm
    template_name = "login/reseteo.html"
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


    def correo_reset_pwd(self, user):
        data = {}
        try:
            URL= settings.DOMAIN if not settings.DEBUG else self.request.META['HTTP_HOST']
            user.token = uuid.uuid4()
            user.save()

            mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            print(mailServer.ehlo())
            mailServer.starttls()
            print(mailServer.ehlo())
            mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
            print('conectado.....')

            email_to = user.email
            #ENVIO DE MENSAJE
            mensaje = MIMEMultipart()
            mensaje['From'] = settings.EMAIL_HOST_USER
            mensaje['To'] = email_to
            mensaje['Subject'] = "Reseteo Clave"

            content = render_to_string('login/send_email.html', {
                'user': user,
                'link_resetpwd': 'http://{}/login/cambio/contraseña/{}/'.format(URL, str(user.token)),
                'link_home': 'http://{}/index/'.format(URL)
            })
            #ENVIA EL CUERPO DEL EMAIL
            mensaje.attach(MIMEText(content, 'html'))

            mailServer.sendmail(settings.EMAIL_HOST_USER,
                                email_to,
                                mensaje.as_string())

            print('Correo Enviado')

        except Exception as e:
            data['error'] = str(e)    
        return data 
        

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form =  ReseteoPasswordForm(request.POST)
            if form.is_valid():
                user = form.get_user()
                #print(self.request.META['HTTP_HOST'])
                data = self.correo_reset_pwd(user)
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context


class CambioPasswordView(FormView):
    form_class = CambioPasswordForm
    template_name = "login/cambiopwd.html"
    success_url = reverse_lazy(setting.LOGIN_REDIRECT_URL)

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        token = self.kwargs['token']
        if User.objects.filter(token=token).exists():
            # print(self.kwargs['token'])
            return super().get(request, *args, **kwargs)
        return HttpResponseRedirect('/')


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            form = CambioPasswordForm(request.POST)
            if form.is_valid():
                user = User.objects.get(token= self.kwargs['token'])
                user.set_password(request.POST['password'])
                user.token = uuid.uuid4()
                user.save()
            else:
                data['error'] =  form.errors
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reseteo de Contraseña'
        return context
