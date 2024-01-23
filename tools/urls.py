from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='tools.index'),
]
