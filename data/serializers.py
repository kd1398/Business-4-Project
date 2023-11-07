from rest_framework import serializers
from .models import Category, FileData, Module, FileDataHistory


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ['id', 'name']


class FileDataIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = FileData
        fields = ['id', 'title']


class FileDataSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)

    class Meta:
        model = FileData
        fields = ['id', 'title', 'data', 'category_name', 'uploaded_by_username', 'uploaded_at', 'modified_at']


class FileDataHistorySerializer(serializers.ModelSerializer):
    # parent_file_id = serializers.CharField(source='FileDataHistory.original_file', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    class Meta:
        model = FileDataHistory
        fields = ['id', 'title', 'data', 'original_file', 'category_name', 'uploaded_by_username', 'uploaded_at', 'modified_at']

class FileDataHistoryIDSerializer(serializers.ModelSerializer):

    class Meta:
        model = FileDataHistory
        fields = ['id', 'title']