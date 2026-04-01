from django.shortcuts import render
from .models import AddTodo
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from rest_framework import status
import traceback
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


# Create your views here.
@swagger_auto_schema(
    method='post',
    request_body=TodoSerializer
)
@swagger_auto_schema(
    method='get',
    responses={200: TodoSerializer(many=True)}
)
@api_view(['GET', 'POST'])
def get_todos(request):
    try:
        if request.method == 'GET':
            todos = AddTodo.objects.all()
            serializer = TodoSerializer(todos, many=True)

            return Response({
                "success": True,
                "data": serializer.data
            })

        elif request.method == 'POST':
            serializer = TodoSerializer(data=request.data)

            if serializer.is_valid():
                serializer.save()

                return Response({
                    "success": True,
                    "message": "Todo created successfully",
                    "data": serializer.data
                }, status=status.HTTP_201_CREATED)

            return Response({
                "success": False,
                "errors": serializer.errors
            }, status=status.HTTP_400_BAD_REQUEST)

    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()

        return Response({
            "error": str(e)
        }, status=500)

    if request.method == 'GET':
        todos = AddTodo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        })

    elif request.method == 'POST':
        serializer = TodoSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response({
                "success": True,
                "message": "Todo created successfully",
                "data": serializer.data
            }, status=status.HTTP_201_CREATED)

        return Response({
            "success": False,
            "message": "Invalid data",
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
   