from django.forms import *
from ProyectoApp.models import *

class CategoriaForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.visible_fields():
            form.field.widget.attrs['class'] = 'form-control'
            form.field.widget.attrs['autocomplete'] = 'off'
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Categoria
        fields = '__all__'        
        widgets = {
            'nombre': TextInput(
                attrs={
                    
                    'placeholder': 'Ingrese',
                    
                }
            ),
            'desc': Textarea(
                attrs={
                    
                    'placeholder': 'Ingrese',
                    
                    'rows': 3,
                    'cols': 3
                }
            ),

        }


    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['nombre']) <= 50:
    #         #self.add_error('nombre', 'Te faltan caracteres')
    #         raise forms.ValidationError('Validacion xxx')
    #     return cleaned
       