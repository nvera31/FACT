from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView, TemplateView
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.contrib.auth.decorators import login_required
from ProyectoApp.models import *
from ProyectoApp.forms import ClientesForm
from django.urls import reverse_lazy,reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

# Create your views here.
#VISTA DE CLIENTES
class ClientesView(TemplateView):
    template_name = 'clientes/clientes.html'

    @method_decorator(csrf_exempt)
    @method_decorator(login_required)
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
            elif action == 'add':
                cli = Clientes()
                cli.nombre = request.POST['nombre']
                cli.apellido = request.POST['apellido']
                cli.dni = request.POST['dni']
                cli.f_nacimiento = request.POST['f_nacimiento']
                cli.direccion = request.POST['direccion']
                cli.sexo = request.POST['sexo']
                cli.save()
            elif action == 'edit':
                cli = Clientes.objects.get(pk=request.POST['id'])
                cli.nombre = request.POST['nombre']
                cli.apellido = request.POST['apellido']
                cli.dni = request.POST['dni']
                cli.f_nacimiento = request.POST['f_nacimiento']
                cli.direccion = request.POST['direccion']
                cli.sexo = request.POST['sexo']
                cli.save()
            elif action == 'delete':
                cli = Clientes.objects.get(pk=request.POST['id'])
                cli.delete()
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Clientes'
        context['list_url'] = reverse_lazy('erp:client')
        context['entity'] = 'Clientes'
        context['form'] = ClientesForm()
        return context
