from rest_framework import serializers
from .models import Todo,Group,Comment
from users.models import CustomUser
from users.serializers import UserSerializer



class Assignee(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('username','id') 

class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('id','name', 'description' , 'owner','created_at')


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('message','todo') 


class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Todo
        fields = ( 'id' , 'name', 'description','due_date', 'assignee', 'isCompleted' , 'attached_file','group') 

 
class TodoAssigneeSerializer(serializers.ModelSerializer)  : 
    class Meta :
        model = Todo 
        fields = ['assignee']

class TodoCheckSerializer(serializers.ModelSerializer)  : 
    class Meta :
        model = Todo 
        fields = ['isCompleted']

class TodoListSerializer(serializers.ModelSerializer):
    assignee = Assignee(many=True,partial=True)
    class Meta:
        model = Todo
        fields = ('id','name','description','due_date','assignee' , 'isCompleted') 


