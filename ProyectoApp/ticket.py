from Proyecto.wsgi import *
from django.template.loader import get_template
from weasyprint import HTML, CSS
#from django.shortcuts import render
from Proyecto import settings

def ticket():
    template = get_template("ProyectoApp/ticket.html")
    context = {"nombre": "Noe Vera"}
    html_template = template.render(context)
    css_url = os.path.join(settings.BASE_DIR, 'ProyectoApp/static/vendor/bootstrap/css/bootstrap.min.css')
    HTML(string=html_template).write_pdf(target="ticket.pdf", stylesheets=[CSS(css_url)])

    
    #print(css_url)

ticket()