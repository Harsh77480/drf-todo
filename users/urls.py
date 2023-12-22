from django.urls import path
from . import views

urlpatterns = [
    path('sign_in', views.Sign_In.as_view()),
    path('sign_up', views.Sign_Up.as_view()),
]