from django.urls import path
from . import views

app_name = 'encuestas'


urlpatterns = [
    path('', views.index, name='home'),
    path('encuestas/', views.list_view, name='encuesta_list'),
    path('encuestas/<int:pk>/', views.detail_view, name='encuesta_detail'),
    path('encuestas/create/', views.create_view, name='encuesta_create'),
    # path('encuestas/<int:pk>/update/', views.EncuestaUpdateView.as_view(), name='encuesta_update'),
    # path('encuestas/<int:pk>/delete/', views.EncuestaDeleteView.as_view(), name='encuesta_delete'),
]