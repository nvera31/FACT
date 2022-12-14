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
            'categoria': Select(
                attrs={
                    'class': 'select2',
                    'style': 'width: 100%'
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

    # search = CharField(widget=TextInput(attrs={
    #     'class': 'form-control',
    #     'placeholder': 'Ingrese Descripcion'
    # }))

    search = ModelChoiceField(queryset=Producto.objects.none(), widget=Select(attrs={
        'class': 'form-control'
    }))


#FORMULARIO CLIENTES
class ClientesForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs['autofocus'] = True

    class Meta:
        model = Clientes
        fields = '__all__'
        widgets = {
            'nombre': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus nombres',
                }
            ),
            'apellido': TextInput(
                attrs={
                    'placeholder': 'Ingrese sus apellidos',
                }
            ),
            'dni': TextInput(
                attrs={
                    'placeholder': 'Ingrese su dni',
                }
            ),
            'f_nacimiento': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                }
            ),
            'direccion': TextInput(
                attrs={
                    'placeholder': 'Ingrese su direcci??n',
                }
            ),
            'sexo': Select()
        }
        #exclude = ['user_updated', 'user_creation']

    def save(self, commit=True):
        data = {}
        form = super()
        try:
            if form.is_valid():
                instance = form.save()
                data = instance.toJSON()
            else:
                data['error'] = form.errors
        except Exception as e:
            data['error'] = str(e)
        return data


#FORMULARIO Ventas
class VentasForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cliente'].queryset = Clientes.objects.none()
        
        # self.fields['cliente'].widget.attrs = {
        #     'autofocus': True,
        #     'class': 'form-control select2'
        # }


    class Meta:
        model = Ventas
        fields = '__all__'
        widgets = {
            'cliente': Select(
                attrs={
                    'class': 'form-select select2',
                    # 'style': 'width: 100%'
                }
            ),
            'f_registro': DateInput(format='%Y-%m-%d',
                attrs={
                    'value': datetime.now().strftime('%Y-%m-%d'),
                    'autocomplete': 'off',
                    'class': 'form-control datetimepicker-input',
                    'id': 'f_registro',
                    'data-target': '#f_registro',
                    'data-toggle': 'datetimepicker'
                }
            ),
            'iva': TextInput(attrs={
                'class': 'form-control',
            }),
            'subtotal': TextInput(attrs={
                'disabled': True,
                'class': 'form-control'
            }),
            'total': TextInput(attrs={
                'disabled': True,
                'class': 'form-control'
            })
        }
        #exclude = ['user_updated', 'user_creation']

    