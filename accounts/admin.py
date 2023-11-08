from django.contrib import admin
from . models import Profile
from django.utils.html import format_html

class ProfileAdmin(admin.ModelAdmin):

    def thumbnail(self,object):
        return format_html('<img src="{}" width="30" style="border-radius:50%;">'.format(object.image.url))
    thumbnail.short_description = "Profile Picture"

    list_display = ('thumbnail','user','full_name','address')

admin.site.register(Profile,ProfileAdmin)