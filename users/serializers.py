from rest_framework import serializers 
from .models import CustomUser
from django.contrib.auth.hashers import make_password

class UserSerializer(serializers.ModelSerializer) : 
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data['password'])
        return super().create(validated_data)

    class Meta : 
        model = CustomUser
        fields = ['id' , 'username' , 'email' , 'password']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }

        