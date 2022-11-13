import os
from django.shortcuts import render
from ProyectoApp.mixin import ValidacionPermiso
from django.views.generic import CreateView, DeleteView, ListView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from ProyectoApp.models import *
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ProyectoApp.forms import VentasForm
from django.urls import reverse_lazy,reverse
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
from ProyectoApp.mixin import ValidacionPermiso

from django.conf import settings
from django.template import Context
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders

import json
# Create your views here.

class VentasListView(LoginRequiredMixin, ValidacionPermiso, ListView):
    model = Ventas
    template_name = 'ventas/ventas.html'
    #permission_required = 'erp.view_sale'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Ventas.objects.all():
                    data.append(i.toJSON())

            elif action == 'search_details':
                data = []
                for i in Det_Ventas.objects.filter(venta_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Ventas'
        context['create_url'] = reverse_lazy('agregar_venta')
        context['list_url'] = reverse_lazy('listar_venta')
        context['entity'] = 'Ventas'
        return context


class VentasCreateView(LoginRequiredMixin, ValidacionPermiso, CreateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('listar_venta')
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
                    #item['value'] = i.nombre
                    item['text'] = i.nombre
                    data.append(item)
            elif action == 'add':
                #PROCESO ALMACENADO
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])

                    sale = Ventas()
                    sale.f_registro = ventas['f_registro']
                    sale.cliente_id = ventas['cliente']
                    sale.subtotal = float(ventas['subtotal'])
                    sale.iva = float(ventas['iva'])
                    sale.total = float(ventas['total'])
                    sale.save()

                    for i in ventas['productos']:
                        det = Det_Ventas()
                        det.venta_id = sale.id
                        det.prod_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save();
                    data = {'id': sale.id}
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
        context['det'] = []
        return context


class VentasUpdateView(LoginRequiredMixin, ValidacionPermiso, UpdateView):
    model = Ventas
    form_class = VentasForm
    template_name = 'ventas/create.html'
    success_url = reverse_lazy('listar_venta')
    #permission_required = 'erp.change_sale'
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
            elif action == 'edit':
                #PROCESO ALMACENADO
                with transaction.atomic():
                    ventas = json.loads(request.POST['ventas'])

                    sale = self.get_object()
                    sale.f_registro = ventas['f_registro']
                    sale.cliente_id = ventas['cliente']
                    sale.subtotal = float(ventas['subtotal'])
                    sale.iva = float(ventas['iva'])
                    sale.total = float(ventas['total'])
                    sale.save()
                    sale.det_ventas_set.all().delete()
                    for i in ventas['productos']:
                        det = Det_Ventas()
                        det.venta_id = sale.id
                        det.prod_id = i['id']
                        det.cantidad = int(i['cantidad'])
                        det.precio = float(i['pvp'])
                        det.subtotal = float(i['subtotal'])
                        det.save();
                    data = {'id': sale.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    
    def get_detalle_productos(self):
        data = []
        try:
            for i in Det_Ventas.objects.filter(venta_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cantidad'] = i.cantidad
                data.append(item)

        except:
            pass
        return data
            
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edicion de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_detalle_productos())
        return context

class VentasDeleteView(LoginRequiredMixin, ValidacionPermiso, DeleteView):
    model = Ventas
    template_name = 'ventas/delete.html'
    success_url = reverse_lazy('listar_venta')
    #permission_required = 'erp.delete_sale'
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
        context['title'] = 'Eliminación de una Venta'
        context['entity'] = 'Ventas'
        context['list_url'] = self.success_url
        return context


class VentasFacturaPdfView(View):
    def link_callback(self, uri, rel):
        sUrl = settings.STATIC_URL        # Typically /static/
        sRoot = settings.STATIC_ROOT      # Typically /home/userX/project_static/
        mUrl = settings.MEDIA_URL         # Typically /media/
        mRoot = settings.MEDIA_ROOT       # Typically /home/userX/project_static/media/

        if uri.startswith(mUrl):
           path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
           path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
           return uri

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path




    def get(self, request, *args, **kwargs):
        try:
            template = get_template('ventas/factura.html')
            context = {
                'venta': Ventas.objects.get(pk=self.kwargs['pk']),
                'comp' : {'nombre': 'ALMACENES MEMO S.A', 'ruc': '1234567890123', 'direccion': 'Paris Chiquito, Ecuador'},
                'icon' : '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            #response['Content-Disposition'] = 'attachment; filename="report.pdf"'
            pisa_status = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
                
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('listar_venta'))