import smtplib
from Proyecto.wsgi import *
from Proyecto import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from user.models import User
from django.template.loader import render_to_string

def send_email():
    try:
        mailServer = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
        print(mailServer.ehlo())
        mailServer.starttls()
        print(mailServer.ehlo())
        mailServer.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
        print('conectado.....')

        email_to = "nverayepez05@gmail.com"
        #ENVIO DE MENSAJE
        mensaje = MIMEMultipart()
        mensaje['From'] = settings.EMAIL_HOST_USER
        mensaje['To'] = email_to
        mensaje['Subject'] = "Ganastes UN Viaje"

        content = render_to_string('ProyectoApp/correo.html', {'user': User.objects.get(pk=1)})
        #ENVIA EL CUERPO DEL EMAIL
        mensaje.attach(MIMEText(content, 'html'))

        mailServer.sendmail(settings.EMAIL_HOST_USER,
                            email_to,
                            mensaje.as_string())

        print('Correo Enviado')

    except Exception as e:
        print(e)       
        

send_email()