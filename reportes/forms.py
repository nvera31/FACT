from django.forms import *

class ReporteForm(Form):
   
    date_ranger = CharField(widget=TextInput(attrs={
        'class': 'form-control',
        'autocomplete': 'off'
    }))
