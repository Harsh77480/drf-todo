from rest_framework import viewsets
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

class Groups(APIView) : 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request) : 
        return Response({"name" : "harsh"})
    # def post(self, request, format=None):
    #     serializer = SnippetSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) def post(self,request) : 
        
from rest_framework.parsers import JSONParser
class Todo(APIView) : 
    def post(self,request,group_id) :
        group = get_object_or_404(models.Group,id=group_id)
        try : 
            data = json.loads(request.data['jsonData'])
            data['assignee'].append(request.user.id)
            data['owner'] = request.user.id
            data['group'] = group_id
            if 'attached_file' in request.data : 
                data['attached_file'] = request.data['attached_file']
            print(data)

            serializer = TodoSerializer(data=data)
            # print(serializer.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        except Exception as error : 
            return JsonResponse({"Error" : str(error)}, status=500)

    def get(self,request,group_id) :
        serializer = TodoSerializer(models.Todo.objects.all(),many=True)
        x = models.Todo.objects.get(id=33)
        data = x.assignee.values('username')
        # data = [e['username'] for e in list(x.assignee.values('username')) ]
        print(data)
        return JsonResponse(serializer.data,safe=False) 
    

# edit assignees 
# comments 
# download image      
           
# Todo : id name desc due date assigness isCompleted 
# assignees 
# attached file 
# comments 

        


# class UploadedFileViewSet(viewsets.ModelViewSet):
#     queryset = DocumentTest.objects.all()
#     serializer_class = UploadedFileSerializer
from django.core.serializers import serialize

class get_file(APIView):

    def get(self,request,id):
        uploaded_file = get_object_or_404(models.Todo, id=id)   
        # x = [e.id for e in uploaded_file.assignee.all()] 
        # print(request.user)    
        # print( list(uploaded_file.assignee.all().values() ) )
        if not request.user in uploaded_file.assignee.all() :
            return JsonResponse({"Error" : "user is not one of todo assignees "}, status=401)
        
        if not uploaded_file.attached_file :
            return JsonResponse({"Error" : "No attached file"}, status=500)
        file_content = uploaded_file.attached_file.file.read()

        content_type = 'application/octet-stream'  # Set the appropriate content type
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.attached_file.file.name}"'
        #for setting the file name and extension when its downloaded    
        return response
    
    #Assuming the file is stored in the 'file' field of the model
    #This content type indicates that the data is binary and doesn’t belong to any particular application
   




