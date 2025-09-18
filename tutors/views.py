from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import TutorSerializer
from rest_framework.response import Response
from rest_framework import status
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
class TutorEndpoint(APIView):

    @swagger_auto_schema(
        operation_description="Create a new tutor profile. Requires Bearer token.",
        manual_parameters=[token_param],
        request_body=TutorSerializer,
        responses={
            201: openapi.Response('Tutor created', examples={"application/json": "Tutor successfully created"}),
            400: openapi.Response('Bad request', examples={"application/json": {"error": "Bad request"}})
        },
        tags=["Tutors"]
    )
    def post(self, request):
        serializer = TutorSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response("Tutor successfully created", status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

