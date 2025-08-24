from django.forms import ModelForm
from .models import Encuesta, Pregunta, Opcion, Respuesta


class EncuestaForm(ModelForm):
    class Meta:
        model = Encuesta
        fields = ['nombre', 'descripcion']