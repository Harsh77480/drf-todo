from django.urls import path,include
from . import views

urlpatterns = [
    path('groups', views.Groups.as_view()),
    path('groups/<int:group_id>', views.Overdue.as_view()),
    path('groups/<int:group_id>/todos', views.Todo.as_view()),
    # path('groups/<int:group_id>/todos/', views.Todo.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>/assignees', views.TodoAssigne.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>/comments', views.TodoComments.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>', views.TodoDetail.as_view()),
    path('download/<int:id>', views.get_file.as_view()),
]   


