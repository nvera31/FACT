from multiprocessing import context
from urllib import request
from django.urls import reverse_lazy,reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from re import template
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .models import *
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from .forms import CategoriaForm, TestForm
from ProyectoApp.mixin import IsSuperUserMixin, ValidacionPermiso

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
# Create your views here.



#ENLISTA LA TABLA CATEGORIA
class CategoriaListView(LoginRequiredMixin, ValidacionPermiso,ListView):
    permission_required = 'ProyectoApp.change_categoria'
    model = Categoria
    template_name = 'ProyectoApp/listar.html'

    @method_decorator(csrf_exempt)
    #@method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            #DATABLE CON AJAX
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Categoria.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
            
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #REDIRECCIONA A VISTA AGREGAR
        context['create_url'] = reverse_lazy('agregar')
        context['list_url'] = reverse_lazy('listar')
        context['title'] = 'Listado'
        return context

#GUARDA NUEVAS CATEGORIAS
class CategoriaCreateView(ValidacionPermiso,CreateView):
    permission_required = 'ProyectoApp.view_categoria'
    url_redirect = reverse_lazy('listar')
    model = Categoria
    form_class = CategoriaForm
    template_name = 'ProyectoApp/create.html'
    success_url = reverse_lazy('listar')

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'add':
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

    # def post(self, request, *args, **kwargs):
    #     form = CategoriaForm(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         return HttpResponseRedirect(self.success_url)
    #     self.object = None
    #     context = self.get_context_data(**kwargs)
    #     context['form'] = form
    #     return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crear Categoria'
        context['action'] = 'add'
        # REDIRECCIONA A LISTAR
        context['list_url'] = reverse_lazy('listar')
        return context


#ACTUALIZA LAS CATEGORIAS
class CategoriaUpdateView(UpdateView):
    model = Categoria
    form_class = CategoriaForm
    template_name = 'ProyectoApp/create.html'
    success_url = reverse_lazy('listar')

    @method_decorator(login_required)
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
        context['title'] = 'Editar Categoria'
        context['action'] = 'edit'
        # REDIRECCIONA A LISTAR
        context['list_url'] = reverse_lazy('listar')
        return context

#ELIMINAR CATEGORIAS
class CategoriaDeleteView(DeleteView):
    
    model = Categoria
    template_name = 'ProyectoApp/delete.html'
    success_url = reverse_lazy('listar')


    #@method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
        context['title'] = 'Eliminar Categoria'
        
        # REDIRECCIONA A LISTAR
        context['list_url'] = reverse_lazy('listar')
        return context


class CategoriaFormView(FormView):
    form_class = CategoriaForm
    template_name = 'ProyectoApp/create.html'
    success_url = reverse_lazy('listar')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Form | Categoria'
        context['action'] = 'edit'
        # REDIRECCIONA A LISTAR
        context['list_url'] = reverse_lazy('listar')
        return context



#TESTVIEWS SELECT2
class TestView(TemplateView):
    template_name = 'ProyectoApp/test.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs) :
        return super().dispatch(request, *args, **kwargs)
        
    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']

            if action == 'buscar':
               data = []
               for i in Producto.objects.filter(categoria_id=request.POST['id']):
                    data.append({'id': i.id, 'text': i.nombre, 'data': i.categoria.toJSON()})
            elif action == 'autocomplete':
                data = []
                for i in Categoria.objects.filter(nombre__icontains=request.POST['term']):
                    item = i.toJSON()
                    item['text'] = i.nombre
                    data.append(item)
            else:
                data['error'] = 'No ha Ingresado'
            
        except Exception as e:
             data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Selects | Django'
        context['form'] = TestForm()
        return context


