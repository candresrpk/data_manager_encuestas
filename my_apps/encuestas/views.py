from django.shortcuts import render, redirect
from .models import Encuesta, Pregunta, Opcion, Respuesta, EncuestaPermiso, Distribucion
from .forms import EncuestaForm
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def index(request):
    return render(request, 'encuestas/home.html')


def list_view(request):
    
    user = request.user
    user_obj = User.objects.filter(username=user).first()
    encuestas = EncuestaPermiso.objects.filter(usuario=user_obj).select_related('encuesta')
    
    context = {
        'encuestas': encuestas,
    }
    
    
    return render(request, 'encuestas/list.html', context)


def detail_view(request, encuesta_id):
    
    user = request.user
    user_obj = User.objects.filter(username=user).first()
    encuesta_data = Encuesta.objects.filter(id=encuesta_id).first()
    
    encuesta = EncuestaPermiso.objects.filter(encuesta=encuesta_data, usuario=user_obj).first()
    
    
    if not encuesta:
        messages.error(request, "No tienes permiso para ver esta encuesta.")
        return redirect('encuestas:list')
    
    
    context = {
        'encuesta': encuesta,
    }
    
    return render(request, 'encuestas/detail.html', context)


def create_view(request):
    
    
    if request.method == 'POST':
        form = EncuestaForm(request.POST)
        if form.is_valid():
            encuesta = form.save(commit=False)
            encuesta.creador = request.user
            encuesta.save()
            
            encuesta_permiso = EncuestaPermiso(
                encuesta=encuesta,
                usuario=request.user,
                puede_editar=True,
                puede_ver_resultados=True,
                cargo=EncuestaPermiso.CargoChoices.ADMINISTRADOR
            )
            encuesta_permiso.save()
            
            messages.success(request, "Encuesta creada exitosamente.")
            return redirect('encuestas:encuesta_list')
        else:
            messages.error(request, "Error al crear la encuesta. Por favor, verifica los datos.")
    else:
        form = EncuestaForm()
        
        
    return render(request, 'encuestas/create.html', {'form': form})






def capturar_cuotas(request, encuesta_id):
    es_htmx = request.headers.get("HX-Request") == "true"
    edad = request.GET.get('edad')
    genero = request.GET.get('genero')
    barrio = request.GET.get('barrio')
    estrato = request.GET.get('estrato')
    
    
    usuario = request.user
    user_obj = User.objects.filter(username=usuario).first()
    encuesta_data = Encuesta.objects.filter(id=encuesta_id).first()

    
    try:
        encuesta = EncuestaPermiso.objects.get(encuesta=encuesta_data, usuario=user_obj).encuesta
    except EncuestaPermiso.DoesNotExist:
        encuesta = None
    except Exception as e:
        encuesta = None
        
    context = {
        'encuesta': encuesta,
    }
    
    # Si la encuesta no existe o el usuario no tiene permiso, redirigir o mostrar un error
    if not encuesta or encuesta == None:
        
        return redirect('encuestas:not_found')
    
    if not es_htmx:
        generos = Distribucion.objects.filter(encuesta=encuesta, asignado_a=request.user).values_list('genero', flat=True).distinct()
        context['generos'] = generos
        return render(request, 'encuestas/cuotas.html', context)
    
    # Caso 1: no eligió nada -> mostrar generos
    
    if not genero and not edad and not barrio and not estrato:
        generos = Distribucion.objects.filter(encuesta=encuesta, asignado_a=request.user).values_list('genero', flat=True).distinct()
        context['generos'] = generos
        return render(request, 'encuestas/partials/_generos.html', context)

    # Caso 2: eligió edad -> mostrar departamentos
    if genero and not edad:
        edades = Distribucion.objects.filter(encuesta=encuesta, asignado_a=request.user, genero=genero).values_list('edad', flat=True).distinct()
        context['genero'] = genero
        context['edades'] = edades
        return render(request, 'encuestas/partials/_edades.html', context)

    # Caso 3: eligió edad y género -> mostrar barrios
    if edad and genero and not barrio:
        barrios = Distribucion.objects.filter(encuesta=encuesta, asignado_a=request.user, edad=edad, genero=genero).values_list('barrio', flat=True).distinct()
        context['barrios'] = barrios
        context['edad'] = edad
        context['genero'] = genero
        return render(request, 'encuestas/partials/_barrios.html', context)

    # Caso 4: eligió edad y género y barrios -> mostrar estrato
    if edad and genero and barrio and not estrato:
        estratos = Distribucion.objects.filter(encuesta=encuesta, asignado_a=request.user, edad=edad, genero=genero, barrio=barrio).values_list('estrato', flat=True).distinct()
        print(estratos)
        context['estratos'] = estratos
        context['edad'] = edad
        context['genero'] = genero
        context['barrio'] = barrio
        
        return render(request, 'encuestas/partials/_estrato.html', context)
        
    # Caso 5: eligió todo -> mostrar resumen/final
    if edad and genero and barrio and estrato:
        context['estrato'] = estrato
        context['edad'] = edad
        context['genero'] = genero
        context['barrio'] = barrio
        
        return render(request, 'encuestas/partials/_resumen.html', context)
    
    
    

def iniciar_encuesta(request, encuesta_id):
    
    edad = request.GET.get('edad')
    genero = request.GET.get('genero')
    barrio = request.GET.get('barrio')
    estrato = request.GET.get('estrato')
    
    usuario = request.user
    user = User.objects.get(username=usuario)
    encuesta_data = Encuesta.objects.get(id=encuesta_id)
    try:
        encuesta = EncuestaPermiso.objects.get(encuesta=encuesta_data, usuario=user).encuesta
    except EncuestaPermiso.DoesNotExist:
        encuesta = None
    except Exception as e:
        encuesta = None
        
    if not encuesta or encuesta == None:
        return redirect('encuestas:not_found')
    
    
    preguntas = encuesta.encuesta_preguntas.all()
    context = {
        'preguntas': preguntas
    }
    
        
    
    return render(request, 'encuestas/preguntas.html', context)

    

def not_found_view(request):
    return render(request, 'encuestas/not_found.html')