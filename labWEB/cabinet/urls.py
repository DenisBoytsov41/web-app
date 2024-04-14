from django.urls import path
from . import views

urlpatterns = [
    path('', views.PersonalCabinetView.as_view(), name='personal_cabinet'),
]