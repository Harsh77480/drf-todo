
from rest_framework import serializers
from .models import Todo

# class UploadedFileSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocumentTest
#         fields = ('name', 'file')

# class GroupSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = DocumentTest
#         fields = ('name', 'file')


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ('name', 'attached_file','description','due_date','assignee','group','owner') 

class TodoListSerializer(serializers.ModelSerializer):

    custom_field = serializers.SerializerMethodField()        

    class Meta:
        model = Todo
        fields = ('name', 'attached_file','description','due_date','assignee','group','owner') 

    def get_custom_field(self, obj):
        obj.assignee.values('username')