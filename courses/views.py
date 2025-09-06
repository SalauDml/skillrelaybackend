from django.shortcuts import render
from rest_framework import permissions
from .serializers import CourseListSerializer,CourseSerializer,QuizSerializer,ModuleListSerializer
from .serializers import LessonSerializer,ExamSerializer
from django.contrib.auth.models import User 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken,AccessToken
from .models import Course,Module
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Create your views here.
class CourseListEndpoint (APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all courses.",
        responses={
            200: openapi.Response(
                description="List of courses",
                schema=CourseListSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "title": "Python Basics",
                            "description": "Learn Python from scratch.",
                            "difficulty": "beginner",
                            "learners": 120
                        }
                    ]
                }
            )
        },
        tags=["Courses"]
    )
    def get(self,request):
        courses = Course.objects.all()
        serializer = CourseListSerializer(courses,many= True)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
class SpecificCourseEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get details of a specific course.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Course ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Course details",
                schema=CourseSerializer(),
                examples={
                    "application/json": {
                        "id": 1,
                        "title": "Python Basics",
                        "description": "Learn Python from scratch.",
                        "difficulty": "beginner",
                        "learners": 120,
                        "modules": [],
                        "exam": None
                    }
                }
            )
        },
        tags=["Courses"]
    )
    def get(self,request,id):
        course = Course.objects.filter(id=id).first()
        serializer = CourseSerializer(course)
        return Response(serializer.data,status=status.HTTP_200_OK)

class ModuleListEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all modules.",
        responses={
            200: openapi.Response(
                description="List of modules",
                schema=ModuleListSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "title": "Introduction",
                            "description": "Getting started",
                            "course": 1
                        }
                    ]
                }
            )
        },
        tags=["Modules"]
    )
    def get(self, request):
        modules = Module.objects.all()
        serializer = ModuleListSerializer(modules, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class SpecificQuizEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get the quiz for a specific module.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Module ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Quiz for module",
                schema=QuizSerializer(),
                examples={
                    "application/json": {
                        "id": 1,
                        "module": 1,
                        "questions": [
                            {
                                "id": 1,
                                "text": "What is Python?",
                                "options": [
                                    {"id": 1, "text": "A snake", "correct": False},
                                    {"id": 2, "text": "A programming language", "correct": True}
                                ]
                            }
                        ]
                    }
                }
            )
        },
        tags=["Quizzes"]
    )
    def get(self, request, id):
        module = Module.objects.filter(id=id).first()
        quiz = getattr(module, 'quiz', None)
        serializer = QuizSerializer(quiz)
        return Response(serializer.data, status=status.HTTP_200_OK)

class LessonsEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get all lessons for a specific module.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Module ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Lessons for module",
                schema=LessonSerializer(many=True),
                examples={
                    "application/json": [
                        {
                            "id": 1,
                            "module": 1,
                            "title": "Lesson 1",
                            "content": "Lesson content...",
                            "media": "url/to/media",
                            "completed": False
                        }
                    ]
                }
            )
        },
        tags=["Lessons"]
    )
    def get(self, request, id):
        module = Module.objects.filter(id=id).first()
        lessons = module.lessons.all() if module else []
        serializer = LessonSerializer(lessons, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get the exam for a specific course.",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="Course ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: openapi.Response(
                description="Exam for course",
                schema=ExamSerializer(),
                examples={
                    "application/json": {
                        "id": 1,
                        "course": 1,
                        "title": "Final Exam",
                        "pass_mark": 80,
                        "questions": [
                            {
                                "id": 1,
                                "text": "What is Python?",
                                "choices": [
                                    {"id": 1, "text": "A snake", "is_correct": False},
                                    {"id": 2, "text": "A programming language", "is_correct": True}
                                ]
                            }
                        ]
                    }
                }
            )
        },
        tags=["Exams"]
    )
    def get(self, request, id):
        course = Course.objects.filter(id=id).first()
        exam = getattr(course, 'exam', None)
        serializer = ExamSerializer(exam)
        return Response(serializer.data, status=status.HTTP_200_OK)