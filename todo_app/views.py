from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.shortcuts import get_object_or_404
from django.http import HttpResponse

class Groups(APIView) : 
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self,request) : 
        return Response({"name" : "sunny leone"})

from rest_framework import viewsets
from .models import DocumentTest

from .serializers import UploadedFileSerializer

class UploadedFileViewSet(viewsets.ModelViewSet):
    queryset = DocumentTest.objects.all()
    serializer_class = UploadedFileSerializer


def get_file(request, file_id):
    uploaded_file = get_object_or_404(DocumentTest, pk=file_id)

    #Assuming the file is stored in the 'file' field of the model
    file_content = uploaded_file.file.read()
    content_type = 'application/octet-stream'  # Set the appropriate content type
    #This content type indicates that the data is binary and doesn’t belong to any particular application

    response = HttpResponse(file_content, content_type=content_type)
    # response['Content-Disposition'] = f'attachment; filename="{uploaded_file.file.name}"'
    return response