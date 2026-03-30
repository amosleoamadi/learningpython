from django.shortcuts import render
from .models import AddTodo
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from rest_framework import status


# Create your views here.
@api_view(['GET', 'POST'])
def get_todos(request):

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
   