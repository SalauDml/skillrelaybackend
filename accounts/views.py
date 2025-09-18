from django.shortcuts import render
from rest_framework import permissions
from .serializers import UserSerializer, CertificationSerializer,CustomTokenObtainPairSerializer
from django.contrib.auth.models import User 
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from .models import CertificationList, AppUser
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework import parsers
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

token_param = openapi.Parameter(
    'Authorization',
    openapi.IN_HEADER,
    description="Bearer <JWT token>",
    type=openapi.TYPE_STRING,
    required=False
)

class CustomTokenObtainPairView(TokenObtainPairView):
    permission_classes = [permissions.AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="User email"),
                "password": openapi.Schema(type=openapi.TYPE_STRING, description="User password"),
            },
            required=["email", "password"],
        )
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(
        operation_description="Register a new user.",
        manual_parameters=[
            openapi.Parameter('email', openapi.IN_FORM, type=openapi.TYPE_STRING, description='User email', required=True),
            openapi.Parameter('password', openapi.IN_FORM, type=openapi.TYPE_STRING, description='User password', required=True),
            openapi.Parameter('full_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Full name', required=True),
            openapi.Parameter('phone_number', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Phone number', required=True),
            openapi.Parameter('location', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Location', required=True),
            openapi.Parameter('profile_picture', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Profile picture file', required=True),
            openapi.Parameter('tutor', openapi.IN_FORM, type=openapi.TYPE_BOOLEAN, description='Is tutor (optional)', required=False),
        ],
        consumes=['multipart/form-data'],
        responses={
            201: openapi.Response('User created', examples={"application/json": {"success": "user created successfully "}}),
            400: openapi.Response('Validation error', examples={"application/json": {"email": ["This field is required."]}})
        },
        tags=["Auth"]
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'success': "user created successfully "}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]

    @swagger_auto_schema(
        operation_description="Login a user and get JWT access token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['email', 'password'],
            properties={
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description='User email'),
                'password': openapi.Schema(type=openapi.TYPE_STRING, format='password', description='User password'),
            },
            example={
                "email": "user@example.com",
                "password": "password123"
            }
        ),
        responses={
            200: openapi.Response('Login success', examples={"application/json": {"access": "jwt-access-token"}}),
            401: openapi.Response('Invalid credentials', examples={"application/json": {"error": "Invalid Credentials"}})
        },
        tags=["Auth"]
    )
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = authenticate(email=email, password=password)

        if user is not None:
            access = AccessToken.for_user(user)
            return Response({'access': str(access)}, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Invalid Credentials"}, status=status.HTTP_401_UNAUTHORIZED)
        

class UserProfile(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(
            manual_parameters= [token_param]
    )

    def get(self,request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
            

    @swagger_auto_schema(
        operation_description="Update user profile (partial update). Requires Bearer token.",
        manual_parameters=[
            token_param,
            openapi.Parameter('full_name', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Full name', required=False),
            openapi.Parameter('phone_number', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Phone number', required=False),
            openapi.Parameter('location', openapi.IN_FORM, type=openapi.TYPE_STRING, description='Location', required=False),
            openapi.Parameter('profile_picture', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Profile picture file', required=False),
            openapi.Parameter('tutor', openapi.IN_FORM, type=openapi.TYPE_BOOLEAN, description='Is tutor', required=False),
        ],
        consumes=['multipart/form-data'],
        responses={
            202: openapi.Response('Profile updated', examples={"application/json": "Succesfully updated"}),
            400: openapi.Response('Validation error', examples={"application/json": {"phone_number": ["This field is required."]}})
        },
        tags=["Profile"]
    )
    def patch(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response("Succesfully updated", status=status.HTTP_202_ACCEPTED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CertificationList(APIView):
    parser_classes = [parsers.MultiPartParser, parsers.FormParser]

    @swagger_auto_schema(
        operation_description="Get all certifications for the authenticated user. Requires Bearer token.",
        manual_parameters=[token_param],
        responses={
            200: openapi.Response(
                'List of certifications',
                examples={"application/json": [
                    {"id": 1, "user": 2, "file": "/media/certificationfiles/cert1.pdf"},
                    {"id": 2, "user": 2, "file": "/media/certificationfiles/cert2.pdf"}
                ]}
            )
        },
        tags=["Certification"]
    )
    def get(self, request):
        certifications = request.user.files.all()
        serializer = CertificationSerializer(certifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        operation_description="Upload a new certification file. Requires Bearer token.",
        manual_parameters=[
            token_param,
            openapi.Parameter('file', openapi.IN_FORM, type=openapi.TYPE_FILE, description='Certification file', required=True)
        ],
        consumes=['multipart/form-data'],
        responses={
            200: openapi.Response('Created', examples={"application/json": "Created Successfully"}),
            400: openapi.Response('Validation error', examples={"application/json": {"file": ["This field is required."]}})
        },
        tags=["Certification"]
    )
    def post(self, request):
        serializer = CertificationSerializer(data=request.data,context = {"request": request})
        if serializer.is_valid():
            serializer.save()
            return Response("Created Successfully", status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)









