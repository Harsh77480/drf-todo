from django.db import models
from users.models import CustomUser


# class DocumentTest(models.Model) :
#     name = models.CharField(max_length=50)


class Group(models.Model):
    name = models.CharField(max_length=200)
#     owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.name


class Todo(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=False)
    due_date = models.DateField(blank=False)
    completion_date  = models.DateField(blank=True,null=True)
    isCompleted = models.BooleanField(default = False)

    assignee = models.ManyToManyField(CustomUser,related_name='parents')
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    attached_file = models.FileField(upload_to='uploads/', null=True )
    
    def __str__(self):
        return self.name 


# class Comment(models.Model) :
#     message = models.TextField(blank=False)
#     todo = models.ForeignKey(Todo, on_delete=models.CASCADE)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)