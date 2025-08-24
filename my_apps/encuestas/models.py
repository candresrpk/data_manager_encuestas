from django.db import models
from django.db.models import Count
from django.contrib.auth.models import User
# Create your models here.



class Encuesta(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    creador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_encuestas')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    
    class Meta:
        verbose_name = 'Encuesta'
        verbose_name_plural = 'Encuestas'
        

class EncuestaPermiso(models.Model):
    
    class CargoChoices(models.TextChoices):
        ADMINISTRADOR = 'Administrador', 'Administrador'
        EDITOR = 'Editor', 'Editor'
        VISOR = 'Visor', 'Visor'
        COLABORADOR = 'Colaborador', 'Colaborador'
    
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_permisos')
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_permisos')
    puede_editar = models.BooleanField(default=False)
    puede_ver_resultados = models.BooleanField(default=False)
    cargo = models.CharField(max_length=100, blank=True, null=True, choices=CargoChoices.choices, default=CargoChoices.VISOR)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f"Permisos de {self.usuario.username} en {self.encuesta.nombre}"
    
    class Meta:
        verbose_name = 'Permiso de Encuesta'
        verbose_name_plural = 'Permisos de Encuestas'
        unique_together = ('encuesta', 'usuario')
    

class Distribucion(models.Model):
    
    class GeneroChoices(models.TextChoices):
        MASCULINO = 'Masculino', 'Masculino'
        FEMENINO = 'Femenino', 'Femenino'
        OTRO = 'Otro', 'Otro'
        PREFIERO_NO_DECIRLO = 'Prefiero no decirlo', 'Prefiero no decirlo'
    
    nombre = models.CharField(max_length=100)
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_distribucion')
    asignado_a = models.ForeignKey(User, on_delete=models.CASCADE, related_name='usuario_distribuciones')
    
    genero = models.CharField(max_length=50, blank=True, null=True, choices=GeneroChoices.choices, default=GeneroChoices.OTRO)
    edad = models.IntegerField(blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    zona = models.CharField(max_length=50, blank=True, null=True)
    
    
    
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'Distribución'
        verbose_name_plural = 'Distribuciones'
        
    @classmethod
    def contar_por_edad(cls):
        return cls.objects.values("edad").annotate(total=Count("edad")).order_by("edad")
    
    @classmethod
    def contar_por_genero(cls):
        return cls.objects.values("genero").annotate(total=Count("genero")).order_by("genero")

    @classmethod
    def contar_por_departamento(cls):
        return cls.objects.values("departamento").annotate(total=Count("departamento")).order_by("departamento")
    
    @classmethod
    def contar_por_municipio(cls):
        return cls.objects.values("municipio").annotate(total=Count("municipio")).order_by("municipio")
    
    @classmethod
    def contar_por_zona(cls):
        return cls.objects.values("zona").annotate(total=Count("zona")).order_by("zona")    
    
    @classmethod
    def contar_por_usuario(cls):
        return cls.objects.values("asignado_a__username").annotate(total=Count("asignado_a")).order_by("asignado_a__username")
    
    
    
class Pregunta(models.Model):
    class CategoriaChoices(models.TextChoices):
        MULTIPLE = 'Múltiple', 'Múltiple'
        UNICA = 'Única', 'Única'
        ABIERTA = 'Abierta', 'Abierta'
        
        
    encuesta = models.ForeignKey(Encuesta, on_delete=models.CASCADE, related_name='encuesta_preguntas')
    texto = models.TextField()
    categoria = models.CharField(max_length=50, blank=True, null=True, choices=CategoriaChoices.choices, default=CategoriaChoices.UNICA)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.texto[:50]  # Mostrar solo los primeros 50 caracteres
    
    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
    
    
class Opcion(models.Model):
    
    pregunta = models.ForeignKey(Pregunta, on_delete=models.CASCADE, related_name='pregunta_opciones')
    texto = models.CharField(max_length=200)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.texto
    
    class Meta:
        verbose_name = 'Opción'
        verbose_name_plural = 'Opciones'
        

class Respuesta(models.Model):
    
    class GeneroChoices(models.TextChoices):
        MASCULINO = 'Masculino', 'Masculino'
        FEMENINO = 'Femenino', 'Femenino'
        OTRO = 'Otro', 'Otro'
        PREFIERO_NO_DECIRLO = 'Prefiero no decirlo', 'Prefiero no decirlo'
        
        
    opcion = models.ForeignKey(Opcion, on_delete=models.CASCADE, related_name='opcion_respuestas')
    
    genero = models.CharField(max_length=50, blank=True, null=True, choices=GeneroChoices.choices)
    edad = models.IntegerField(blank=True, null=True)
    departamento = models.CharField(max_length=100, blank=True, null=True)
    municipio = models.CharField(max_length=100, blank=True, null=True)
    zona = models.CharField(max_length=50, blank=True, null=True)
    
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Respuesta a {self.opcion.pregunta.texto}"
    
    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        
    
    @classmethod
    def contar_por_edad(cls):
        return cls.objects.values("edad").annotate(total=Count("edad")).order_by("edad")
    
    @classmethod
    def contar_por_genero(cls):
        return cls.objects.values("genero").annotate(total=Count("genero")).order_by("genero") 
    
    @classmethod
    def contar_por_departamento(cls):
        return cls.objects.values("departamento").annotate(total=Count("departamento")).order_by("departamento")
    
    @classmethod
    def contar_por_municipio(cls):
        return cls.objects.values("municipio").annotate(total=Count("municipio")).order_by("municipio")
    
    @classmethod
    def contar_por_zona(cls):
        return cls.objects.values("zona").annotate(total=Count("zona")).order_by("zona")
    
    @classmethod
    def contar_por_opcion(cls):
        return cls.objects.values("opcion__texto").annotate(total=Count("opcion")).order_by("opcion__texto")
    
        
        
