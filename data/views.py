import csv
import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET
from rest_framework.parsers import JSONParser

from core.decorators import authenticate_user
from data.models import FileData, Category
from data.serializers import CategorySerializer, FileDataSerializer, FileDataIDSerializer


# Create your views here.
@csrf_exempt
@authenticate_user
def get_file_categories(request, user):
    categories = Category.objects.all()
    serializer = CategorySerializer(categories, many=True)
    category_data = serializer.data
    return JsonResponse({"data": {"data": category_data}, "error": ""}, status=200)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_names(request, user):
    file_data = FileData.objects.all()
    serializer = FileDataIDSerializer(file_data, many=True)
    data = serializer.data
    return JsonResponse({"data": {"data": data}, "error": ""}, status=200)


@csrf_exempt
@authenticate_user
def upload_file(request, user):
    file_related_data = json.loads(request.POST.get('data'))
    file_title = file_related_data.get('file_name')
    category_obj = Category.objects.get(pk=file_related_data.get('file_category'))

    uploaded_file = request.FILES.get('uploaded_file')
    processed_data = process_file(uploaded_file)

    file_data_object = FileData(title=file_title, category=category_obj, data=processed_data, uploaded_by=user)
    file_data_object.save()

    message = "File processed successfully."
    return JsonResponse({"data": {"message": message}, "error": ""}, status=200)


def process_file(uploaded_file):
    content = uploaded_file.read().decode('utf-8')
    csv_reader = csv.DictReader(content.splitlines())

    count = 1
    json_data = {}
    for row in csv_reader:
        json_data[count] = row
        count += 1
    return json_data


@csrf_exempt
@require_GET
@authenticate_user
def get_file_data(request, user):
    data = JSONParser().parse(request)
    file_id = data.get('id')
    file_data = FileData.objects.get(pk=file_id)
    serializer = FileDataSerializer(file_data, many=False)
    data = serializer.data
    return JsonResponse({"data": {"data": data}, "error": ""}, status=200)