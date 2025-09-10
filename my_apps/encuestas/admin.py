from django.contrib import admin
from .models import Encuesta, EncuestaPermiso, Distribucion, Pregunta, Opcion, Respuesta
# Register your models here.


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre', 'creador', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('nombre', 'creador__username')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    
    
@admin.register(EncuestaPermiso)
class EncuestaPermisoAdmin(admin.ModelAdmin):
    list_display = ('id', 'encuesta', 'usuario', 'puede_editar','puede_ver_resultados', 'cargo', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('encuesta__titulo', 'usuario__username')
    list_filter = ('puede_editar', 'fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    
@admin.register(Distribucion)
class DistribucionAdmin(admin.ModelAdmin):
    list_display = ('id', 'encuesta', 'genero', 'edad', 'asignado_a', 'estrato', 'barrio', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('encuesta__titulo', 'asignado_a__username')
    list_filter = ('genero', 'edad', 'fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('id', 'encuesta', 'texto', 'categoria', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('encuesta__titulo', 'texto')
    list_filter = ('categoria',  'fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    
@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('id', 'pregunta', 'texto', 'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('pregunta__texto', 'texto')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    
@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('id', 'encuestador', 'opcion__texto', 'opcion__pregunta__encuesta__nombre', 'opcion__pregunta__texto', 'genero', 'edad', 'departamento', 'municipio', 'zona',  'fecha_creacion', 'fecha_actualizacion')
    search_fields = ('pregunta__texto', 'usuario__username', 'texto_respuesta')
    list_filter = ('fecha_creacion', 'fecha_actualizacion')
    ordering = ('-fecha_creacion',)
    

