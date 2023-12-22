from django.db import models
from users.models import CustomUser


class DocumentTest(models.Model) :
    name = models.CharField(max_length=50)
    file = models.FileField(upload_to='uploads/',blank=False, null=False)


# class Group(models.Model):
#     name = models.CharField(max_length=200)
#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     # created at 
#     def __str__(self):
#         return self.name



# class Todo(models.Model):
#     name = models.CharField(max_length=200)
#     description = models.TextField(blank=False)
#     assignee = models.ManyToManyField(CustomUser)
#     group = models.ForeignKey(Group, on_delete=models.CASCADE)
#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
#     isCompleted = models.BooleanField(default = False)
#     due_date = models.DateField(blank=False)
#     completion_date  = models.DateField(blank=True)
#     # attached_file = 
    
#     def __str__(self):
#         return self.name


# class Comment(models.Model) :
#     message = models.TextField(blank=False)
#     todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)