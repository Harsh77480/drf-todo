from django.urls import path,include
from . import views

urlpatterns = [
    path('groups', views.Groups.as_view()),

    #generic views 
    path('test_groups', views.TestGroupsList.as_view()),
    path('test_groups_create', views.TestGroupsCreate.as_view()),
    path('test_groups/<int:group_id>/test_todos', views.TestTodosList.as_view()),
    path('test_groups/<int:group_id>/test_todos_create', views.TestTodoCreate.as_view()),
    path('test_todos/<int:pk>', views.TestTodoDetails.as_view()),
    path('test_groups/<int:pk>', views.TestGroupDetails.as_view()),
    path('test_todos_assignee_update/<int:pk>', views.TestTodoAssigneeUpdate.as_view()),
    
    
    path('groups/<int:group_id>', views.Overdue.as_view()),
    path('groups/<int:group_id>/todos', views.Todo.as_view()),
    # path('groups/<int:group_id>/todos/', views.Todo.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>/assignees', views.TodoAssigne.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>/comments', views.TodoComments.as_view()),
    path('groups/<int:group_id>/todos/<int:todo_id>', views.TodoDetail.as_view()),
    path('download/<int:id>', views.get_file.as_view()),
    
]   


