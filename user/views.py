from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
import traceback
from .serializers import LoginSerializer

# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=RegisterSerializer,
    responses={201: RegisterSerializer, 400: "Bad Request"}
)
@api_view(['POST'])
def register(request):
   try:
       serializer = RegisterSerializer(data=request.data)

       if serializer.is_valid():
                serializer.save()
                return Response({
                        "success": True,
                        "message": "User registered successfully",
                        "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
            
       return Response({
                "success": False,
                "error": serializer.errors,
            }, status=400)
   
   except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
   
   

@swagger_auto_schema(
    method='post',
    request_body=LoginSerializer,
    responses={200: "Success", 400: "Bad Request"}
)
@api_view(['POST'])
def login_view(request):
    serializer = LoginSerializer(data=request.data)

    if serializer.is_valid():
        data = serializer.validated_data
        user = data['user']

        return Response({
            "success": True,
            "message": "Login successful",
            "data": {
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email": user.email,
                "access_token": data['access'],
                "refresh_token": data['refresh']
            }
        })

    return Response({
        "success": False,
        "errors": serializer.errors
    }, status=400)