from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.timezone import now
from django.utils import timezone
from django.shortcuts import render, redirect
from .models import Dueno, Mascota, Cita, Veterinario
from .forms import CitaCompletaForm



from .forms import CitaCompletaForm, VeterinarioForm, CedulaVeterinarioForm, TratamientoForm, CitaForm
from .models import Dueno, Mascota, Cita, Veterinario


def get_veterinarios(request):
    especialidad = request.GET.get('especialidad')
    veterinarios = Veterinario.objects.filter(especialidad=especialidad).values('id', 'nombre')
    return JsonResponse(list(veterinarios), safe=False)

def bienvenida(request):
    return render(request, 'clinica/bienvenida.html')
from django.shortcuts import render, get_object_or_404
from .models import Dueno, Cita

def mis_citas(request, dueno_id):
    dueno = get_object_or_404(Dueno, id=dueno_id)
    citas = Cita.objects.filter(dueno=dueno).order_by('fecha', 'hora')
    return render(request, 'clinica/mis_citas.html', {'dueno': dueno, 'citas': citas})

def agendar_cita(request):
    if request.method == 'POST':
        form = CitaCompletaForm(request.POST)
        if form.is_valid():
            # Buscar o crear dueño por cédula
            cedula = form.cleaned_data['cedula']
            dueno, creado = Dueno.objects.get_or_create(
                cedula=cedula,
                defaults={
                    'nombre': form.cleaned_data['nombre_dueno'],
                    'apellido': form.cleaned_data['apellido_dueno'],
                    'telefono': form.cleaned_data['telefono'],
                    'correo': form.cleaned_data['correo']
                }
            )

            # Crear mascota
            mascota = Mascota.objects.create(
                nombre=form.cleaned_data['nombre_mascota'],
                especie=form.cleaned_data['especie'],
                edad=form.cleaned_data['edad'],
                dueno=dueno
            )

            # Buscar veterinario por especialidad
            especialidad = form.cleaned_data['especialidad']
            veterinario = Veterinario.objects.filter(especialidad__iexact=especialidad).first()

            if not veterinario:
                messages.error(request, "No hay veterinarios disponibles en esa especialidad.")
                return redirect('agendar_cita')

            # Validar horario ocupado
            if Cita.objects.filter(
                fecha=form.cleaned_data['fecha'],
                hora=form.cleaned_data['hora'],
                veterinario=veterinario
            ).exists():
                messages.error(request, "Ese horario ya está ocupado.")
                return render(request, 'clinica/agendar.html', {'form': form})

            # Crear cita con instancia de veterinario
            Cita.objects.create(
                dueno=dueno,
                mascota=mascota,
                fecha=form.cleaned_data['fecha'],
                hora=form.cleaned_data['hora'],
                especialidad=form.cleaned_data['especialidad'],
                veterinario=veterinario   # ✅ instancia correcta
            )

            messages.success(request, "¡La cita fue reservada con éxito! 🐾")
            return redirect('mis_citas', dueno_id=dueno.id)
        else:
            print("Errores del formulario:", form.errors)
    else:
        form = CitaCompletaForm()

    return render(request, 'clinica/agendar.html', {'form': form})

def admin_portal(request):
    veterinarios = Veterinario.objects.all()

    if request.method == 'POST':
        form = VeterinarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_portal')
    else:
        form = VeterinarioForm()

    return render(request, 'clinica/admin_portal.html', {
        'form': form,
        'veterinarios': veterinarios
    })

def editar_veterinario(request, id):
    vet = get_object_or_404(Veterinario, id=id)
    if request.method == 'POST':
        form = VeterinarioForm(request.POST, instance=vet)
        if form.is_valid():
            form.save()
            return redirect('admin_portal')
    else:
        form = VeterinarioForm(instance=vet)
    return render(request, 'clinica/editar_veterinario.html', {'form': form})

def eliminar_veterinario(request, id):
    vet = get_object_or_404(Veterinario, id=id)
    vet.delete()
    return redirect('admin_portal')



# Vista veterinario
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from .models import Veterinario, Cita

def veterinario_portal(request):
    cedula = request.session.get('cedula')
    if not cedula:
        return redirect('veterinario_login')

    # Buscar el veterinario por cédula
    veterinario = get_object_or_404(Veterinario, cedula=cedula)

    # Definir la fecha de hoy
    hoy = timezone.now().date()

    # Filtrar citas desde hoy en adelante para ese veterinario
    citas = Cita.objects.filter(veterinario=veterinario).order_by('fecha', 'hora')

    return render(request, 'clinica/veterinario_portal.html', {
        'citas': citas,
        'veterinario': veterinario
    })


def admin_portal(request):
    if request.method == 'POST':
        form = VeterinarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('admin_portal')  # recarga la página después de guardar
    else:
        form = VeterinarioForm()

    veterinarios = Veterinario.objects.all()
    return render(request, 'clinica/admin_portal.html', {
        'form': form,
        'veterinarios': veterinarios
    })

from .models import Veterinario, Cita
from .forms import CedulaVeterinarioForm
from django.utils import timezone

def veterinario_login(request):
    if request.method == 'POST':
        form = CedulaVeterinarioForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            try:
                vet = Veterinario.objects.get(cedula=cedula)
                request.session['cedula'] = vet.cedula  # guardar sesión
                return redirect('veterinario_portal')
            except Veterinario.DoesNotExist:
                form.add_error('cedula', 'Cédula no registrada')
    else:
        form = CedulaVeterinarioForm()
    return render(request, 'clinica/veterinario_login.html', {'form': form})


def eliminar_cita(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)
    dueno_id = cita.dueno.id
    cita.delete()
    messages.success(request, "La cita fue eliminada correctamente 🐾")
    return redirect('mis_citas', dueno_id=dueno_id)

def registrar_tratamiento(request, cita_id):
    cita = get_object_or_404(Cita, id=cita_id)

    if request.method == 'POST':
        form = TratamientoForm(request.POST)
        if form.is_valid():
            tratamiento = form.save(commit=False)
            tratamiento.cita = cita
            tratamiento.save()
            return redirect('veterinario_portal')
    else:
        form = TratamientoForm()

    return render(request, 'clinica/registrar_tratamiento.html', {
        'form': form,
        'cita': cita
    })


def editar_cita(request, cita_id):
    cita = get_object_or_404(Cita, pk=cita_id)

    if request.method == "POST":
        form = CitaCompletaForm(request.POST)
        if form.is_valid():
            # Ver qué datos llegan
            print("Datos limpios:", form.cleaned_data)

            # Actualizar manualmente los campos
            cita.fecha = form.cleaned_data['fecha']
            cita.hora = form.cleaned_data['hora']
            cita.especialidad = form.cleaned_data['especialidad']
            cita.veterinario = form.cleaned_data['veterinario']  # instancia correcta

            cita.save()
            messages.success(request, "La cita fue actualizada correctamente 🐾")
            return redirect("mis_citas", dueno_id=cita.dueno.id)
    else:
        form = CitaCompletaForm(initial={
            'fecha': cita.fecha,
            'hora': cita.hora,
            'especialidad': cita.especialidad,
            'veterinario': cita.veterinario,
        })

    return render(request, "clinica/editar_cita.html", {"form": form, "cita": cita})






