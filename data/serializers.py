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
    class Meta:
        model = FileData
        fields = ['id', 'title', 'data', 'category', 'uploaded_by', 'uploaded_at', 'modified_at']
