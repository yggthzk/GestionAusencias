from rest_framework import serializers
from .models import SolicitudAusencia

class SolicitudAusenciaSerializer(serializers.ModelSerializer):
    class Meta:
        model = SolicitudAusencia
        fields = '__all__'
        read_only_fields = ('estado', 'fecha_creacion', 'fecha_actualizacion')