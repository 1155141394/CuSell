from django.contrib import admin
from .models import *


# Register your models here.

class UserManager(admin.ModelAdmin):
    list_display = ['sid', 'name', 'email', 'password', 'introduction', 'creation_date']


admin.site.register(User, UserManager)
