from django.contrib import admin
from .models import Dueno, Mascota, Veterinario, Cita, Tratamiento

admin.site.register(Dueno)
admin.site.register(Mascota)
admin.site.register(Veterinario)
admin.site.register(Cita)
admin.site.register(Tratamiento)