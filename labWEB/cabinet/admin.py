from django.contrib import admin
from .models import UserTheme,UserToken,Users

admin.site.register(UserTheme)
admin.site.register(UserToken)
admin.site.register(Users)
