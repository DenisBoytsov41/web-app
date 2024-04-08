from django.urls import path
from . import views

urlpatterns = [
    path('', views.personal_cabinet, name='personal_cabinet')
]
