from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
# router.register(r'files', views.UploadedFileViewSet)

urlpatterns = [
    path('file', include(router.urls)),
    path('groups/<int:group_id>/todos', views.Todo.as_view()),
    path('download/<int:id>', views.get_file.as_view()),
]


