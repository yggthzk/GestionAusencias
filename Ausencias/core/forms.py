from django import forms
from .models import SolicitudAusencia

class SolicitudForm(forms.ModelForm):
    class Meta:
        model = SolicitudAusencia
        fields = ['tipo', 'fecha_inicio', 'fecha_fin', 'justificativo', 'motivo']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        justificativo = cleaned_data.get('justificativo')

        if tipo == 'licencia_medica' and not justificativo:
            self.add_error('justificativo', 'Debe subir un justificativo para licencia medica')
        
        return cleaned_data