from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from ProyectoApp.mixin import IsSuperUserMixin, ValidacionPermiso
from ProyectoApp.models import Producto
from ProyectoApp.forms import ProductoForm

# Create your views here.

class ProductoListView(LoginRequiredMixin,ValidacionPermiso,ListView):
    model = Producto
    template_name = 'producto/productos.html'
    permission_required = 'view_producto'

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
                for i in Producto.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
            
        except Exception as e:
            data['error'] = str(e)
        
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Productos'
        context['create_url'] = reverse_lazy('product_create')
        context['list_url'] = reverse_lazy('product_list')
        context['entity'] = 'Productos'
        return context


class ProductoCreateView(LoginRequiredMixin,ValidacionPermiso,CreateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'add_producto'
    url_redirect =success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product_list')
        context['action'] = 'add'
        return context


class ProductoUpdateView(LoginRequiredMixin,ValidacionPermiso,UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = 'producto/create.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'change_producto'
    url_redirect =success_url

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
        context['title'] = 'Edición de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product_list')
        context['action'] = 'edit'
        return context


class ProductoDeleteView(LoginRequiredMixin,ValidacionPermiso,DeleteView):
    model = Producto
    template_name = 'producto/delete.html'
    success_url = reverse_lazy('product_list')
    permission_required = 'delete_producto'
    url_redirect =success_url

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
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
        context['title'] = 'Eliminación de un Producto'
        context['entity'] = 'Productos'
        context['list_url'] = reverse_lazy('product_list')
        return context
