from django.contrib import admin
from django.urls import path, include, re_path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('setup', views.setup, name='setup'),
    path('admin/', admin.site.urls),

    path('terminal', views.terminal, name='terminal'),
    path('run-command', views.runCommand, name='command.run'),

    path('tools/', include('tools.urls')),
]
