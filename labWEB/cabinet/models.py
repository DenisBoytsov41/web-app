from django.db import models
from django.contrib.auth.models import User

class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Темная')], default='light')
