from rest_framework import viewsets
# from .models import DocumentTest
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
        
        # print(request.user.id)
        # data = JSONParser.parse(request.data['assignee'])
        # assignees  = request.data['assignee'].split(',') [1:]
        # assignees.pop()
        # assignees.append(str(request.user.id))
        # print(assignees)
        # print(request.data['assignee']) 
        # print( '[1,2,3]' )
        try : 
            data = json.loads(request.data['jsonData'])
            data['assignee'].append(request.user.id)
            data['owner'] = request.user.id
            data['group'] = group_id
            # print(data)


            serializer = TodoSerializer(data=data)
            # print(serializer.data)
            if serializer.is_valid():
                serializer.save()
                return JsonResponse(serializer.data, status=201)
            return JsonResponse(serializer.errors, status=400)

        except Exception as error : 
            return JsonResponse({"Error" : str(error)}, status=500)


        # print(x)

        # # request.data['assignee'].insert(request.user.id)
        # request.data['assignee'] = request.user.id
        # print(dict(request.data))
        # serializer = TodoSerializer(data=request.data)
        # # print(serializer.data)
        # if serializer.is_valid():
        #     serializer.save()
        #     return JsonResponse(serializer.data, status=201)
        # return JsonResponse(serializer.errors, status=400)


    # def put(self,request) : 


# class UploadedFileViewSet(viewsets.ModelViewSet):
#     queryset = DocumentTest.objects.all()
#     serializer_class = UploadedFileSerializer


class get_file(APIView):

    def get(self,request,id):
        uploaded_file = get_object_or_404(models.Todo, id=id)
        file_content = uploaded_file.attached_file.file.read()
        content_type = 'application/octet-stream'  # Set the appropriate content type
        response = HttpResponse(file_content, content_type=content_type)
        response['Content-Disposition'] = f'attachment; filename="{uploaded_file.attached_file.file.name}"'
        #for setting the file name and extension when its downloaded    
        return response
    
    #Assuming the file is stored in the 'file' field of the model
    #This content type indicates that the data is binary and doesn’t belong to any particular application
   




