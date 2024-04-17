from django.contrib import admin
from .models import Register,Login,UserRecord,UserProfile

# Register your models here.
admin.site.register(Register)
admin.site.register(Login)
admin.site.register(UserRecord)
admin.site.register(UserProfile)
