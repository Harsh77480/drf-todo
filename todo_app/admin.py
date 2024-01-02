from django.contrib import admin
from . import models
# Register your models here.



admin.site.register(models.Todo)
admin.site.register(models.Group)
admin.site.register(models.Comment) 
class TodoAdmin(admin.ModelAdmin):
    search_fields = ['name']