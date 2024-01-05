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
import json 
from users.serializers import UserSerializer
from users.models import CustomUser
from . import serializers
from datetime import date 
from rest_framework.pagination import PageNumberPagination
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import generics
from .serializers import GroupSerializer
from .permissions import IsAssigneePermission , IsOwnerPermission
from . import models


#list groups 
class TestGroupsList(generics.ListAPIView) :

    """ API for Listing Groups where user is assigned one of the todos"""

    permission_classes = [IsAuthenticated]
    serializer_class = serializers.GroupSerializer #autodetects many = True acc. to queryset 

    def get_queryset(self):
        #get groups of all todos that are assigned to request.user 
        user_assigned_groups = models.Group.objects.filter(id__in=self.request.user.parents.values('group').distinct()) #user.parents = user.todos , all todos where user is assigned in ManyToManyKey , we are getting the group of those 

        #get all groups whose owner is request.user , this query is needed for when no todo is there in group  
        user_owned_groups = models.Group.objects.filter(owner=self.request.user.id)

        return user_assigned_groups.union(user_owned_groups)
    

#create groups 
class TestGroupsCreate(generics.CreateAPIView) :
    
    """ API for Creating a Group of Todos """

    permission_classes = [IsAuthenticated] 
    serializer_class = serializers.GroupSerializer

    def post(self, request, *args, **kwargs): #for setting 'owner' field 
        request.data['owner'] = request.user.id
        return self.create(request, *args, **kwargs)


class TestGroupDetails(generics.RetrieveAPIView) : 
    
    """ API for getting a Group instance"""

    permission_classes = [IsAuthenticated] 
    serializer_class = serializers.GroupSerializer
    queryset = models.Group.objects.all()


class TestTodoDetails(generics.RetrieveAPIView) : 
    
    """ API for getting a Todos instance"""

    permission_classes = [IsAuthenticated,IsAssigneePermission] #Custom permission only assignees can get the todo
    serializer_class = serializers.TodoListSerializer
    queryset = models.Todo.objects.all()


#get todos 
class TestTodosList(generics.ListAPIView) :

    """ API for getting a Todos instance"""

    serializer_class = serializers.TodoSerializer 
    permission_classes = [IsAuthenticated,IsAssigneePermission] #Custom permission only assignees can get the todo
    
    pagination_class = PageNumberPagination
    pagination_class.page_size = 5

    def get_queryset(self):
        
        #from all todos of user filter the one with given group
        user = CustomUser.objects.get(id=self.request.user.id) 
        todos = user.parents.filter(group = self.kwargs['group_id']).order_by('-due_date')

        name_query = self.request.query_params.get('name') #for searching 
        if name_query:
            todos = todos.filter(name__icontains=name_query)

        return todos





#create todos
class TestTodoCreate(generics.CreateAPIView) :

    """ API for Creating a Todos instance"""


    permission_classes = [IsAuthenticated,IsOwnerPermission] 
    serializer_class = serializers.TodoSerializer
    
    def create(self, request, *args, **kwargs):
        
        #jsonData is sent via form and in form of string , converting in json before passing to serializer 
        data = json.loads(request.data['jsonData'])
        data['assignee'].append(request.user.id)
        data['group'] = kwargs['group_id']
        data['attached_file'] = request.data.get('attached_file')

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers) 



class TestTodoAssigneeUpdate(generics.UpdateAPIView):
    
    """ API for Updating Todos assignees """

    permission_classes = [IsAuthenticated,IsOwnerPermission] 
    queryset = models.Todo.objects.all()
    serializer_class = serializers.TodoAssigneeSerializer
    serializer_class.partial = True  # Allow partial updates


class TestTodoCheck(generics.UpdateAPIView) : 
    
    """ API for Checkbox on todo """

    queryset = models.Todo.objects.all()
    permission_classes = [IsAuthenticated,IsAssigneePermission] 
    serializer_class = serializers.TodoCheckSerializer
    serializer_class.partial = True  # Allow partial updates





# current APIViews 

class Groups(APIView) : 

    #permissions
    permission_classes = [IsAuthenticated]

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
        


#Todo operations 
    
class Todo(APIView) :   
    def post(self,request,group_id) :
        group = get_object_or_404(models.Group,id=group_id)
        try : 
            data = json.loads(request.data['jsonData'])
            data['assignee'].append(request.user.id) #adding owner as one of the assignees of the todos 
            data['group'] = group_id #setting group foreign key 
            if 'attached_file' in request.data : 
                data['attached_file'] = request.data['attached_file']

            serializer = TodoSerializer(data=data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        except Exception as error : 
            return JsonResponse({"Error" : str(error)}, status=500)


    
    def get(self,request,group_id) :

        #pagination
        paginator = PageNumberPagination()
        paginator.page_size = 5
        group = get_object_or_404(models.Group,id=group_id)

        user = CustomUser.objects.get(id=request.user.id) 
        todos = user.parents.filter(group = group_id)

        #searching
        name_query = request.query_params.get('name') #for searching 
        if name_query:
            todos = todos.filter(name__icontains=name_query)

        paginated_queryset = paginator.paginate_queryset(todos, request)
        
        data = serializers.TodoListSerializer(paginated_queryset,many=True) 
        return paginator.get_paginated_response({"group" : group.name , "groupDesc" : group.description , "todos" : data.data })


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

class TodoDetail(APIView) : 
    def get(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)

        #only assignees can see details
        if len(user) < 1 : 
                return JsonResponse({"Error" : "Unauthorized"},status=401)
        return JsonResponse(serializers.TodoListSerializer(todo).data)
    

    def post(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)
        #only assignees can check todo 
        if len(user) < 1 : 
                return JsonResponse({"Error" : "Unauthorized"},status=401)
        todo.isCompleted = not todo.isCompleted
        todo.save()
        return JsonResponse(serializers.TodoListSerializer(todo).data)
    




class TodoComments(APIView) : 

    def get(self,request,group_id,todo_id) : 
        todo = get_object_or_404(models.Todo,id=todo_id)
        user = todo.assignee.filter(id = request.user.id)

        #only assignees can see and post comments 
        if len(user) < 1 : 
                return JsonResponse({"Error" : "You cant see comment "},status=401)
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
    


#download attached file with todo 
class get_file(APIView):
    @swagger_auto_schema(
            operation_summary="Download the attached file given todo id",
            operation_description="Only Assignees of todos can do get the file",
            responses={200: 'Success response'},
        )

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
    
   
#list overdue todos 
class Overdue(APIView) : 
    def get(self,request,group_id) :   
        uncompleted_todos = models.Todo.objects.filter(group=group_id , due_date__lt=date.today() , isCompleted = False ) 
        serializer = serializers.TodoListSerializer(uncompleted_todos,many=True)
        return JsonResponse(serializer.data,safe=False)


