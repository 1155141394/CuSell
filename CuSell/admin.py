from django.contrib import admin
from .models import *


# Register your models here.

# define the format of user in admin
class UserManager(admin.ModelAdmin):
    # the attributes that the list would show
    list_display = ['sid', 'name', 'email', 'password', 'introduction', 'creation_date',
                    'portrait', 'is_active']
    # click sid to go to the information change interface
    list_display_links = ['sid']
    # fuzzy query user according to sid
    search_fields = ['sid']
    # add attribute which could directly changed in list
    list_editable = ['is_active']


# define the format of merchandise in admin
class MerchandiseManager(admin.ModelAdmin):
    # show the attributes in the list
    list_display = ['mid', 'sid', 'name', 'price', 'contact', 'description', 'pub_date',
                    'update_date', 'image_1', 'image_2', 'image_3', 'image_4']
    # filter according to key_word
    list_filter = ['sid']
    # click mid to go to the information change interface
    list_display_links = ['mid']
    # fuzzy query merchandise according to bid, sid, name, key_word
    search_fields = ['mid', 'sid', 'name', 'contact']
    # add attribute which could directly changed in list

admin.site.register(User, UserManager)
admin.site.register(Merchandise, MerchandiseManager)
