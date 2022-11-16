from django.shortcuts import render
from django.views.generic import *
from datetime import datetime
from ProyectoApp.models import *
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from random import randint
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin

# Create your views here.

class InicioView(LoginRequiredMixin, TemplateView):
    template_name = 'index/home.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        request.user.get_group_session()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'grafico_ventas':
                data = {
                    'name': 'Porcentaje de Venta',
                    'showInLegend': False,
                    'colorByPoint': True,
                    'data': self.grafico_ventas()
                }
            elif action == 'grafico_productos':
                data = {
                    'name': 'Vendido',
                    'colorByPoint': True,
                    'data': self.grafico_productos(),
                }  
            elif action == 'grafico_online':
                data = {'y': randint(1, 100)}
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def grafico_ventas(self):
        data = []
        try:
            year = datetime.now().year
            for m in range(1, 12):
                total = Ventas.objects.filter(f_registro__year=year, f_registro__month=m).aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                data.append(float(total))
        except:
            pass
        return data

    def grafico_productos(self):
        data = []
        year = datetime.now().year
        month = datetime.now().month
        try:
            for p in Producto.objects.all():
                total = Det_Ventas.objects.filter(venta__f_registro__year=year, venta__f_registro__month=month, prod_id=p.id).aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                if total > 0:
                    data.append({
                        'name': p.nombre,
                        'y': float(total)
                    })

        except:
            pass
        return data

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Venta'
        context['grafico_ventas'] = self.grafico_ventas()
        return context