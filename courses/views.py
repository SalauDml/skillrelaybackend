from django.shortcuts import render
from rest_framework import permissions
from .serializers import CourseListSerializer,CourseSerializer,QuizSerializer,ModuleListSerializer,UserProgressSerializer,UserCourseProgress
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

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <JWT token>",
    type=openapi.TYPE_STRING,
    required=False
)

# Create your views here.
class CourseListEndpoint (APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all courses.",
        manual_parameters=[token_param],
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
            token_param,
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
        try:
            course = Course.objects.get(id = id)
            serializer = CourseSerializer(course)
            return Response(serializer.data,status=status.HTTP_200_OK)
        except Course.DoesNotExist:
            return Response("Course with that Id does not exist", status=status.HTTP_400_BAD_REQUEST)
       

class ModuleListEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Get a list of all modules.",
        manual_parameters=[token_param],
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
            token_param,
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
            token_param,
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
            token_param,
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
    
class ProgressEndpoint(APIView):
    @swagger_auto_schema(
        operation_description="Create user progress. Requires Bearer token.",
        manual_parameters=[token_param],
        request_body=UserProgressSerializer,
        responses={
            201: openapi.Response('Accepted', examples={"application/json": "Accepted Request"}),
            400: openapi.Response('Validation error', examples={"application/json": {"error": "Validation failed"}})
        },
        tags=["Progress"]
    )
    def post(self,request):
        serializer = UserProgressSerializer(data=request.data,context= {"request":request.user})
        if serializer.is_valid():
            serializer.save()
            return Response("Accepted Request",status=status.HTTP_201_CREATED)
        return Response(f"{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Update user progress. Requires Bearer token.",
        manual_parameters=[
            token_param,
            openapi.Parameter('id', openapi.IN_PATH, description="Progress ID", type=openapi.TYPE_INTEGER)
        ],
        request_body=UserProgressSerializer,
        responses={
            202: openapi.Response('Updated', examples={"application/json": "Updated Successfully"}),
            400: openapi.Response('Validation error', examples={"application/json": {"error": "Validation failed"}})
        },
        tags=["Progress"]
    )
    def patch(self,request,id):
        object = UserCourseProgress.objects.filter(id = id)
        serializer = UserProgressSerializer(object, request.data, partial = True)
        if serializer.is_valid():
            serializer.save()
            return Response ("Updated Succesfully", status=status.HTTP_202_ACCEPTED)
        return Response(f"{serializer.errors}", status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        operation_description="Delete user progress. Requires Bearer token.",
        manual_parameters=[
            token_param,
            openapi.Parameter('id', openapi.IN_PATH, description="Progress ID", type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: openapi.Response('Deleted', examples={"application/json": "Deleted Successfully"}),
            404: openapi.Response('Not found', examples={"application/json": "Object does not exist"})
        },
        tags=["Progress"]
    )
    def delete(self, request, id):
        try: 
            object = UserCourseProgress.objects.filter(id = id)
        except UserCourseProgress.DoesNotExist:
            return Response("Object does not exist", status=status.HTTP_404_NOT_FOUND)
        object.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

