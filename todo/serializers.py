from rest_framework import serializers
from .models import AddTodo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTodo
        fields = '__all__'