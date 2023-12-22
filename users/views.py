from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from users.models import CustomUser

class Sign_Up (APIView) :
    def post(self,request) : 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            serializer.save()
            return Response(serializer.data) 
        else :
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
            
    }

class Sign_In (APIView) :

    def post(self,request) : 
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email,password=password)
        print(email,password,user)
        if user :
            # Generate tokens for the user
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


    