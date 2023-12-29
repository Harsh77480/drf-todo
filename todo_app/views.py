from django.core.serializers import serialize
from rest_framework import viewsets,pagination
from .serializers import TodoSerializer
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import HttpResponse,JsonResponse
from rest_framework import status
from . import models
import json 
from users.serializers import UserSerializer
from users.models import CustomUser
from . import serializers
from datetime import date 
from rest_framework.pagination import PageNumberPagination


class CustomPagination(pagination.PageNumberPagination):
    page_size = 1  
    page_size_query_param = 'page_size'
    max_page_size = 100  

class Groups(APIView) : 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get(self,request) :
        user_groups = models.Group.objects.filter(id__in=request.user.parents.values('group').distinct())
        user_owned_groups = models.Group.objects.filter(owner=request.user.id)
        groups = serializers.GroupSerializer(user_groups.union(user_owned_groups),many=True)
        return JsonResponse(groups.data,safe=False)
    

    def post(self, request ):
        request.data['owner'] = request.user.id
        serializer = serializers.GroupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
        
from rest_framework.parsers import JSONParser
from users.serializers import UserSerializer
class Todo(APIView) : 

    def post(self,request,group_id) :

        group = get_object_or_404(models.Group,id=group_id)
        try : 
            data = json.loads(request.data['jsonData'])
            data['assignee'].append(request.user.id)
            data['group'] = group_id
            if 'attached_file' in request.data : 
                data['attached_file'] = request.data['attached_file']
            print(data)

            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        except Exception as error : 
            return JsonResponse({"Error" : str(error)}, status=500)

    def get(self,request,group_id) :

        paginator = PageNumberPagination()
        paginator.page_size = 10

        user = CustomUser.objects.get(id=request.user.id) 
        todos = user.parents.filter(group = group_id)

        name_query = request.query_params.get('name') #for searching 
        if name_query:
            todos = todos.filter(name__icontains=name_query)


        paginated_queryset = paginator.paginate_queryset(todos, request)
        
        data = serializers.TodoListSerializer(paginated_queryset,many=True) 
        return paginator.get_paginated_response(data.data)
        # return JsonResponse(data.data,safe=False) 
    

class TodoAssigne(APIView) : 
    def get(self,request,group_id,todo_id) :  
        todo = get_object_or_404(models.Todo,id=todo_id)
        try : 
            user = todo.assignee.filter(id = request.user.id)
            if len(user) < 1 : 
                return JsonResponse({"Error" : "Unauthorized"},status=401)
            serializer = serializers.Assignee(todo.assignee.all(),many=True)
            return JsonResponse(serializer.data,safe=False)
            
        except Exception as error: 
            return JsonResponse({"Error" :str(error)},status = 500)

    def patch(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        try : 
            if request.user.id is not todo.group.owner.id :
                return JsonResponse({"Error" : "You can't add/remove assignees "},status=401)
            assignees = request.data['assignee']
            if request.user.id not in assignees:
                assignees.append(request.user.id)
            users = CustomUser.objects.filter(id__in = assignees)
            todo.assignee.set(users)
            todo.save()
            serializer = serializers.TodoListSerializer(todo)
            return JsonResponse(serializer.data)
        except Exception as error: 
            return JsonResponse({"Error" :str(error)},status = 500)

class TodoCompletion(APIView) : 
    def post(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)
        if len(user) < 1 : 
                return JsonResponse({"Error" : "Unauthorized"},status=401)
        todo.isCompleted = not todo.isCompleted
        todo.save()
        return JsonResponse(serializers.TodoListSerializer(todo).data)
    
class Overdue(APIView) : 
    def get(self,request,group_id) :   
        uncompleted_todos = models.Todo.objects.filter(group=group_id , due_date__lt=date.today() , isCompleted = False ) 
        # print(uncompleted_todos)
        serializer = serializers.TodoListSerializer(uncompleted_todos,many=True)
        return JsonResponse(serializer.data,safe=False)


class TodoComments(APIView) : 

    def get(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)
        if len(user) < 1 : 
                return JsonResponse({"Error" : "You see comment "},status=401)
        comments = serializers.CommentSerializer(todo.comment_set.all(),many=True)
        return JsonResponse(comments.data,safe=False)
    
    def post(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)
        if len(user) < 1 : 
                return JsonResponse({"Error" : "You can't comment "},status=401)
        
        comments = todo.comment_set.all()
        print(comments)
        request.data['todo'] = todo.id
        new_comment = serializers.CommentSerializer(data = request.data)
        if new_comment.is_valid() :
            new_comment.save() 
            return JsonResponse(new_comment.data, status=201)
        return JsonResponse(new_comment.errors, status=400)
    


class get_file(APIView):

    def get(self,request,id):
        uploaded_file = get_object_or_404(models.Todo, id=id)   
        if not request.user in uploaded_file.assignee.all() :
            return JsonResponse({"Error" : "user is not one of todo assignees "}, status=401)
        
        if not uploaded_file.attached_file :
            return JsonResponse({"Error" : "No attached file"}, status=500)
        file_content = uploaded_file.attached_file.file.read()

        content_type = 'application/octet-stream'  # Set the appropriate content type
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.attached_file.file.name}"'
        return response
    
   




