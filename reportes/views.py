from django.shortcuts import render
from django.views.generic import TemplateView
from django.urls import reverse_lazy,reverse
from reportes.forms import ReporteForm
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from ProyectoApp.models import *
from ProyectoApp.mixin import ValidacionPermiso
from django.db.models.functions import Coalesce
from django.db.models import Sum, DecimalField
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
class ReportesVentasView(LoginRequiredMixin, ValidacionPermiso,TemplateView):
    template_name = 'reportes/reportes.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
       return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                search = Ventas.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(f_registro__range=[start_date,end_date])
                for s in search:
                    data.append([
                        s.id,
                        s.cliente.nombre,
                        s.f_registro.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'), 0, output_field=DecimalField())).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'), 0, output_field=DecimalField())).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'), 0, output_field=DecimalField())).get('r')
                data.append([
                    '---',
                    '---',
                    '---',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),
                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs): 
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Venta'
        context['list_url'] = reverse_lazy('reportes')
        context['form'] = ReporteForm()
        return context


