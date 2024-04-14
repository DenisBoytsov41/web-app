from django.template.context_processors import static
from django.urls import path
from . import views
from django.conf import settings

urlpatterns = [
    path('', views.index),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
]
