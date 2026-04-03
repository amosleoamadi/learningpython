from rest_framework import serializers
from .models import AddTodo

class TodoSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddTodo
        fields = '__all__'
        read_only_fields = ['id', 'created_at', 'updated_at']

    def validate(self, data):
        if not data.get("title"):
            raise serializers.ValidationError("Title is required")
        if not data.get("description"):
            raise serializers.ValidationError("Description is required")
        return data