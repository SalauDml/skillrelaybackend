from django.urls import path,include,re_path
from .views import TutorEndpoint

urlpatterns = [
    path("tutor/",TutorEndpoint.as_view())
]