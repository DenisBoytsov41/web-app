from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.auth.models import User

class UserTheme(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=10, choices=[('light', 'Светлая'), ('dark', 'Темная')], default='light')
    def __str__(self):
        return self.user

    class Meta:
        verbose_name = 'Тема'
        verbose_name_plural = 'Темы'


User = get_user_model()
class UserToken(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    token = models.CharField(max_length=255)

    def __str__(self):
        return self.token

    class Meta:
        verbose_name = 'Токен'
        verbose_name_plural = 'Токены'