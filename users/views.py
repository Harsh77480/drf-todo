from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response 
from .serializers import UserSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth import authenticate
from django.db import transaction
from django.contrib.auth.hashers import make_password
from .models import EmailVerification,CustomUser
from django.conf import settings
from django.core.mail import send_mail
from django.http import HttpResponse

def email_test(user_email,hash) : 
    subject = "Email Verification"
    message = f" Click on below link to verify your email \n http://127.0.0.1:8000/api/users/verify/{hash} "
    email_from = settings.EMAIL_HOST_USER 
    recipient_list = [user_email]
    send_mail(subject,message,email_from,recipient_list)
    return Response({"email" : "sent"})

def verify_email(request,hash) :
        verifier=EmailVerification.objects.get(hash=hash)
        if verifier : 
            email = verifier.email 
            user = CustomUser.objects.get(email = email)
            if user :
                user.is_verified = True 
                user.save()
                return HttpResponse("Your mail has been verified!")
        return HttpResponse("Unable to verify your mail!")
    

class Sign_Up (APIView) :
    def post(self,request) : 
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True) :
            with transaction.atomic() :
                serializer.save()
                email=serializer.data['email']
                verifier=EmailVerification.objects.create(email=email)
                email_test(email,verifier.hash)
                return Response(serializer.data) 
        else :
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'id' : user.id ,
        'name' : user.username
    }

class Sign_In (APIView) :

    def post(self,request) : 
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(request,email=email,password=password)
        # print(email,password,user.id)
        if user :
            tokens = get_tokens_for_user(user)
            return Response(tokens, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        


    