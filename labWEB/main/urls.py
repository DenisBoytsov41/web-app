from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('registration/', views.registration, name='registration'),
    path('authorization/', views.authorization, name='authorization'),
]
