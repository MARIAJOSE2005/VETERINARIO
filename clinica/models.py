from django.db import models

class Dueno(models.Model):
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20)
    correo = models.EmailField(unique=True)
    cedula = models.CharField(max_length=20, unique=True)  # nuevo campo

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Mascota(models.Model):
    nombre = models.CharField(max_length=100)
    especie = models.CharField(max_length=50)  # Ej: perro, gato, ave
    edad = models.PositiveIntegerField()
    dueno = models.ForeignKey(Dueno, on_delete=models.CASCADE, related_name="mascotas")

    def __str__(self):
        return f"{self.nombre} ({self.especie})"


class Veterinario(models.Model):
    cedula = models.CharField(max_length=20, unique=True)
    nombre = models.CharField(max_length=100)
    especialidad = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)

    def __str__(self):
        return f"{self.nombre} ({self.cedula})"

class Cita(models.Model):
    dueno = models.ForeignKey(Dueno, on_delete=models.CASCADE)
    mascota = models.ForeignKey(Mascota, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()
    veterinario = models.ForeignKey(Veterinario, on_delete=models.CASCADE)
    especialidad = models.CharField(max_length=50)


def __str__(self):
        return f"Cita de {self.mascota.nombre} con {self.veterinario.nombre} el {self.fecha}"


class Tratamiento(models.Model):
    cita = models.ForeignKey(Cita, on_delete=models.CASCADE, related_name="tratamientos")
    descripcion = models.TextField()
    medicamento = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return f"Tratamiento para {self.cita.mascota.nombre} el {self.cita.fecha}"