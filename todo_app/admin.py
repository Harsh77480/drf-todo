from django.contrib import admin
from . import models
# Register your models here.

from datetime import date
admin.site.register(models.Group)
admin.site.register(models.Comment) 

@admin.register(models.Todo)
class TodoAdmin(admin.ModelAdmin):
    search_fields = ['name']
    list_display = ("name","description","overdue")
    list_filter = ['name']
    def overdue(self,obj) : 
        todo = models.Todo.objects.get(id=obj.id)
        if todo.due_date < date.today() :
            return True
        return False