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
        exclude = ['user_actualizo', 'user_creador']


    # def clean(self):
    #     cleaned = super().clean()
    #     if len(cleaned['nombre']) <= 50:
    #         #self.add_error('nombre', 'Te faltan caracteres')
    #         raise forms.ValidationError('Validacion xxx')
    #     return cleaned
       

class ProductoForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Producto
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese un nombre',
                }
            ),
        }


#CODIGO DE GUARDAR EN FORMULARIO
    # def save(self, commit=True):
    #     data = {}
    #     form = super()
    #     try:
    #         if form.is_valid():
    #             form.save()
    #         else:
    #             data['error'] = form.errors
    #     except Exception as e:
    #         data['error'] = str(e)
    #     return data


class TestForm(Form):
    categorias = ModelChoiceField(queryset=Categoria.objects.all(), widget=Select(attrs={
        'class': 'form-control select2',
        'style': 'width: 100%'
    }))

    productos = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control select2'
    }))