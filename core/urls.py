
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include('my_apps.users.urls', namespace='users')),
    path('', include('my_apps.encuestas.urls', namespace='encuestas')),
]
