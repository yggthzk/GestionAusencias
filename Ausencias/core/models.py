from django.db import models
from django.contrib.auth.models import User

class SolicitudAusencia(models.Model):
    TIPOS = [
        ('vacaciones', 'Vacaciones'),
        ('medica', 'Licencia Medica'),
        ('personal', 'Dia Personal'),
    ]
    ESTADOS = [
        ('pendiente', 'Pendiente'),
        ('aprobada', 'Aprobada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    nombre_completo = models.CharField(max_length=200)
    codigo_empleado = models.CharField(max_length=50)
    correo_contacto = models.EmailField(max_length=254, verbose_name="Correo de Contacto", default="sin@correo.com")
    contacto_emergencia = models.CharField(max_length=200, verbose_name="Contacto de Emergencia", default="No especificado")
    contacto_emergencia = models.CharField(max_length=200, verbose_name="Contacto de Emergencia")
    tipo_ausencia = models.CharField(max_length=20, choices=TIPOS)
    fecha_inicio = models.DateField(null=True, blank=True)  #campos del formularioooo
    fecha_fin = models.DateField(null=True, blank=True)
    motivo_detallado = models.TextField()
    url_justificativo = models.URLField(max_length=500, blank=True, null=True)
    estado = models.CharField(max_length=20, choices=ESTADOS, default='pendiente')
    fecha_solicitud = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombre_completo} - {self.estado}"