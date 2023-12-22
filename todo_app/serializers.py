
from rest_framework import serializers
from .models import DocumentTest

class UploadedFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentTest
        fields = ('name', 'file')

