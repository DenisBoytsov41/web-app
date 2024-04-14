from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),
    path('<str:token>/', views.personal_cabinet, name='personal_cabinet'),
]