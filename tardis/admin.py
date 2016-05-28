from django.contrib import admin

# Register your models here.

from tardis import models

admin.site.register(models.Trip, admin.ModelAdmin)
