from django.shortcuts import render
from django.shortcuts import get_object_or_404
from .models import AddTodo
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import TodoSerializer
from rest_framework import status
import traceback
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi


@swagger_auto_schema(
    method='get',
    responses={200: TodoSerializer(many=True)}
)
@api_view(['GET'])
def get_todos(request):
    """Get all todos"""
    try:
        todos = AddTodo.objects.all()
        serializer = TodoSerializer(todos, many=True)

        return Response({
            "success": True,
            "data": serializer.data
        })

    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


@swagger_auto_schema(
    method='post',
    request_body=TodoSerializer,
    responses={201: TodoSerializer(), 400: "Bad Request"}
)
@api_view(['POST'])
def create_todo(request):
    try:
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
            "success": False,
            "error": str(e)
        }, status=500)
    

@swagger_auto_schema(
    method='get',
    responses={200: TodoSerializer(), 404: "Not Found"}
)
@api_view(['GET'])
def get_todo_detail(request, pk):
    try:
        todo = get_object_or_404(AddTodo, pk=pk)
        serializer = TodoSerializer(todo)
        return Response({
            "success": True,
            "data": serializer.data
        })
    except Exception as e:
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
    

@swagger_auto_schema(
    method='patch',
    request_body=TodoSerializer,
    responses={200: TodoSerializer(), 400: "Bad Request", 404: "Not Found"}
)
@api_view(['PATCH'])
def update_todo(request, pk):
    """Partially update a todo (PATCH)"""
    try:
        todo = get_object_or_404(AddTodo, pk=pk)
        serializer = TodoSerializer(todo, data=request.data, partial=True)
        
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Todo updated successfully",
                "data": serializer.data
            })
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


@swagger_auto_schema(
    method='delete',
    responses={200: "Deleted", 404: "Not Found"}
)
@api_view(['DELETE'])
def delete_todo(request, pk):
    """Delete a todo"""
    try:
        todo = get_object_or_404(AddTodo, pk=pk)
        todo.delete()
        return Response({
            "success": True,
            "message": "Todo deleted successfully"
        }, status=status.HTTP_200_OK)
    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)
    

@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Mark as completed'),
        }
    ),
    responses={200: TodoSerializer(), 404: "Not Found"}
)
@api_view(['PATCH'])
def mark_todo_done(request, pk):
    try:
        todo = get_object_or_404(AddTodo, pk=pk)
        todo.completed = True
        todo.save()
        
        serializer = TodoSerializer(todo)
        return Response({
            "success": True,
            "message": "Todo marked as done",
            "data": serializer.data
        })
    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)


@swagger_auto_schema(
    method='patch',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN, description='Toggle completion status'),
        }
    ),
    responses={200: TodoSerializer(), 404: "Not Found"}
)
@api_view(['PATCH'])
def toggle_todo_status(request, pk):
    """Toggle todo completion status (using PATCH for partial update)"""
    try:
        todo = get_object_or_404(AddTodo, pk=pk)
        todo.completed = not todo.completed
        todo.save()
        
        status_message = "done" if todo.completed else "undone"
        
        serializer = TodoSerializer(todo)
        return Response({
            "success": True,
            "message": f"Todo marked as {status_message}",
            "data": serializer.data
        })
    except Exception as e:
        print("🔥 ERROR:", str(e))
        traceback.print_exc()
        return Response({
            "success": False,
            "error": str(e)
        }, status=500)