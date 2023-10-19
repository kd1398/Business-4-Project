from rest_framework import serializers
from .models import Category, FileData


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class FileDataIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileData
        fields = ['id']


class FileDataSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = FileData
        fields = ['id', 'title', 'data', 'category_name', 'uploaded_by_username', 'uploaded_at', 'modified_at']
