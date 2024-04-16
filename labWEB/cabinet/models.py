from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User
from main.models import Register

class UserTheme(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE,primary_key=True)
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Темная')], default='light')
    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


User = get_user_model()
class UserToken(models.Model):
    user = models.OneToOneField(Register, on_delete=models.CASCADE,primary_key=True)
    token = models.CharField(max_length=255, null=True)

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'