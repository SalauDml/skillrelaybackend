from django.urls import path
from .views import (
    CourseListEndpoint,
    SpecificCourseEndpoint,
    SpecificQuizEndpoint,
    ModuleListEndpoint,
    LessonsEndpoint,
    ExamEndpoint,
    ProgressEndpoint,
)

urlpatterns = [
    path('courses/', CourseListEndpoint.as_view(), name='course-list'),
    path('courses/<int:id>/', SpecificCourseEndpoint.as_view(), name='course-detail'),
    path('modules/', ModuleListEndpoint.as_view(), name='module-list'),
    path('modules/<int:id>/quiz/', SpecificQuizEndpoint.as_view(), name='module-quiz'),
    path('modules/<int:id>/lessons/', LessonsEndpoint.as_view(), name='module-lessons'),
    path('courses/<int:id>/exam/', ExamEndpoint.as_view(), name='course-exam'),
    path('courses/<int:id>/progress/',ProgressEndpoint.as_view())

]

