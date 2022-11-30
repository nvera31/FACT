from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from ProyectoApp.models import *
from ProyectoApp.forms import ClientesForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ProyectoApp.mixin import ValidacionPermiso

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
#VISTA DE CLIENTES
class ClienteListView(LoginRequiredMixin, ValidacionPermiso, ListView):
    model = Clientes
    template_name = 'clientes/clientes.html'
    permission_required = 'view_clientes'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Clientes.objects.all():
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['create_url'] = reverse_lazy('agregar_cliente')
        context['list_url'] = reverse_lazy('listar_cliente')
        context['entity'] = 'Clientes'
        return context


class ClienteCreateView(LoginRequiredMixin, ValidacionPermiso, CreateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('listar_cliente')
    permission_required = 'add_clientes'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación un Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ClienteUpdateView(LoginRequiredMixin, ValidacionPermiso, UpdateView):
    model = Clientes
    form_class = ClientesForm
    template_name = 'clientes/create.html'
    success_url = reverse_lazy('listar_cliente')
    permission_required = 'change_clientes'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición un Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ClienteDeleteView(LoginRequiredMixin, ValidacionPermiso, DeleteView):
    model = Clientes
    template_name = 'clientes/delete.html'
    success_url = reverse_lazy('listar_cliente')
    #permission_required = 'erp.delete_client'
    url_redirect = success_url

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
        context['title'] = 'Eliminación de un Cliente'
        context['entity'] = 'Clientes'
        context['list_url'] = self.success_url
        return context
