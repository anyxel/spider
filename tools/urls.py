from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tools.index'),
    path('get-categories', views.categories, name='tools.categories'),
    path('get-tools', views.tools, name='tools.tools'),
    path('get-tool', views.getTool, name='tools.get-tool'),
]
