from django import forms
from .models import Cita, Mascota, Dueno, Veterinario, Tratamiento


class CitaCompletaForm(forms.Form):
    # Datos del dueño
    cedula = forms.CharField(label="Cédula del dueño", max_length=20)
    nombre_dueno = forms.CharField(max_length=100, label="Nombre del dueño")
    apellido_dueno = forms.CharField(max_length=100, label="Apellido")
    correo = forms.EmailField(label="Correo")
    telefono = forms.CharField(max_length=20, label="Teléfono")

    # Datos de la mascota
    nombre_mascota = forms.CharField(max_length=100, label="Nombre de la mascota")
    especie = forms.ChoiceField(choices=[
        ('Perro', 'Perro'),
        ('Gato', 'Gato'),
        ('Ave', 'Ave'),
        ('Otro', 'Otro'),
    ], label="Especie")
    edad = forms.IntegerField(label="Edad")
    especialidad = forms.ChoiceField(choices=[
        ('General', 'General'),
        ('Cirugía', 'Cirugía'),
        ('Dermatología', 'Dermatología'),
        ('Odontología', 'Odontología'),
    ], label="Especialidad")

    fecha = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    hora = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))

    # Datos de la cita
    veterinario = forms.ModelChoiceField(queryset=Cita._meta.get_field('veterinario').remote_field.model.objects.all())

class VeterinarioForm(forms.ModelForm):
    class Meta:
        model = Veterinario
        fields = ['cedula','nombre', 'especialidad', 'correo']
        widgets = {
            'cedula': forms.TextInput(attrs={'class': 'form-control'}),
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'especialidad': forms.TextInput(attrs={'class': 'form-control'}),
            'correo': forms.EmailInput(attrs={'class': 'form-control'}),
        }
class CedulaVeterinarioForm(forms.Form):
    cedula = forms.CharField(max_length=20, label="Cédula del Veterinario")


class TratamientoForm(forms.ModelForm):
            class Meta:
                model = Tratamiento
                fields = ['descripcion', 'medicamento']  # ← solo los campos que existen
                widgets = {
                    'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
                    'medicamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            }
                labels = {
                    'descripcion': 'Descripción del tratamiento',
                    'medicamento': 'Medicamento recetado',
            }
class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['fecha', 'hora', 'especialidad', 'veterinario']
        widgets = {
            'fecha': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'hora': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'especialidad': forms.Select(attrs={'class': 'form-select'}),
            'veterinario': forms.Select(attrs={'class': 'form-select'}),
        }




