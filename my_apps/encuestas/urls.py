from django.urls import path
from . import views

app_name = 'encuestas'


urlpatterns = [
    path('', views.index, name='home'),
    path('encuestas/', views.list_view, name='encuesta_list'),
    path('encuestas/create/', views.create_view, name='encuesta_create'),
    path('encuestas/<int:encuesta_id>/', views.detail_view, name='encuesta_detail'),
    path('encuestas/cuotas/<int:encuesta_id>/', views.capturar_cuotas, name='cuotas_encuesta'),
    path('encuesta/iniciar/<int:encuesta_id>/', views.iniciar_encuesta, name='iniciar_encuesta'),
    path('not-found/', views.not_found_view, name='not_found'),
]