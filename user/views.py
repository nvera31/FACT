from multiprocessing import context
from urllib import request
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView, View
from re import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group

from ProyectoApp.mixin import IsSuperUserMixin, ValidacionPermiso
from user.forms import *
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.



#ENLISTA LA TABLA CATEGORIA
class UsuarioListView(LoginRequiredMixin, ValidacionPermiso,ListView):
    #permission_required = 'user.view_user'
    model = User
    template_name = 'user/user.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            #DATABLE CON AJAX
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in User.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
            
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #REDIRECCIONA A VISTA AGREGAR
        context['create_url'] = reverse_lazy('crear_usuarios')
        context['list_url'] = reverse_lazy('listar_usuarios')
        context['title'] = 'Listado de Usuarios'
        return context

class UsuarioCreateView(LoginRequiredMixin, ValidacionPermiso,CreateView):
    #permission_required = 'user.user_add'
    
    model = User
    form_class =  UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('listar_usuarios')
    url_redirect = success_url

    
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha Ingresado'
            
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Usuario'
        context['action'] = 'add'
        # REDIRECCIONA A LISTAR
        context['list_url'] = self.success_url
        return context

class UsuarioUpdateView(LoginRequiredMixin, ValidacionPermiso,UpdateView):
    #permission_required = 'user.change_add'
    
    model = User
    form_class =  UserForm
    template_name = 'user/create.html'
    success_url = reverse_lazy('listar_usuarios')
    url_redirect = success_url

    
    def dispatch(self, request, *args, **kwargs) :
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data ['error'] = form.errors
            else:
                data['error'] = 'No ha Ingresado'
            
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Editar Usuario'
        context['action'] = 'edit'
        # REDIRECCIONA A LISTAR
        context['list_url'] = self.success_url
        return context


class UsuarioDeleteView(LoginRequiredMixin, ValidacionPermiso, DeleteView):
    
    model = User
    template_name = 'user/delete.html'
    success_url = reverse_lazy('listar_usuarios')
    url_redirect = success_url


    #@method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs) :
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:      
            self.object.delete()
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminar Usuarios'
        
        # REDIRECCIONA A LISTAR
        context['list_url'] = self.success_url
        return context

class Perfil(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        try:
            request.session['group'] = Group.objects.get(pk=self.kwargs['pk']) 
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('Home'))


class UsuarioPerfilView(LoginRequiredMixin,UpdateView):
    #permission_required = 'user.change_add'
    
    model = User
    form_class =  UserProfileForm
    template_name = 'user/perfil.html'
    success_url = reverse_lazy('Home')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        return self.request.user
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'edit':
                form = self.get_form()
                if form.is_valid():
                    form.save()
                else:
                    data ['error'] = form.errors
            else:
                data['error'] = 'No ha Ingresado'
            
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion Perfil'
        context['action'] = 'edit'
        # REDIRECCIONA A LISTAR
        context['list_url'] = self.success_url
        return context


class UsuarioPasswordView(LoginRequiredMixin,FormView):
    
    model = User
    form_class =  PasswordChangeForm
    template_name = 'user/password.html'
    success_url = reverse_lazy('login')
    
    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)

    def get_form(self, form_class=None):
        form = PasswordChangeForm(user=self.request.user)
        form.fields['old_password'].widget.attrs['placeholder'] = 'Ingrese su contraseña actual'
        form.fields['new_password1'].widget.attrs['placeholder'] = 'Ingrese su nueva contraseña'
        form.fields['new_password2'].widget.attrs['placeholder'] = 'Repita su contraseña'
        return form


    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'edit':
                form = PasswordChangeForm(user=request.user, data=request.POST)
                if form.is_valid():
                    form.save()
                    update_session_auth_hash(request, form.user)
                else:
                    data['error'] = form.errors
            else:
                data['error'] = 'No ha Ingresado'
            
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion Contraseña'
        context['action'] = 'edit'
        # REDIRECCIONA A LISTAR
        context['list_url'] = self.success_url
        return context
