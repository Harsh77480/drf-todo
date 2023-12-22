from django.urls import path,include
from . import views

from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'files', views.UploadedFileViewSet)

urlpatterns = [
    path('file', include(router.urls)),
    path('files/<int:file_id>/download', views.get_file, name='file-download'),

    # other URL patterns...
]