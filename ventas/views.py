from django.shortcuts import render
from ProyectoApp.mixin import ValidacionPermiso
from django.views.generic import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from ProyectoApp.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ProyectoApp.forms import VentasForm
from django.urls import reverse_lazy,reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
# Create your views here.

class VentasCreateView(LoginRequiredMixin, ValidacionPermiso, CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('Home')
    #permission_required = 'erp.add_sale'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_productos':
                data = []
                prods = Producto.objects.filter(nombre__icontains=request.POST['term'][0:10])
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.nombre
                    data.append(item)

            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context