import csv
import openpyxl
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
    if 'update_value' in request.POST:
        # Handle the request to update a specific value in the file data
        file_data_id = request.POST.get('file_data_id')
        row_number = int(request.POST.get('row_number'))
        column_name = request.POST.get('column_name')
        new_value = request.POST.get('new_value')

        try:
            file_data = FileData.objects.get(pk=file_data_id)
        except FileData.DoesNotExist:
            return JsonResponse({"data": "", "error": "File data not found."}, status=404)

        # Update the specific value in the data
        file_data.data[str(row_number)][column_name] = new_value
        file_data.save()

        return JsonResponse({"data": {"message": "File data updated successfully."}, "error": ""}, status=200)
    else:
        file_related_data = json.loads(request.POST.get('data'))
        file_title = file_related_data.get('file_name')
        file_type = file_related_data.get('file_type')
        uploaded_file = request.FILES.get('uploaded_file')
        if file_type == "csv":
            processed_data = process_file(uploaded_file)
        elif file_type == "xlsx":
            processed_data = process_xlsx_file(uploaded_file)
        else:
            return JsonResponse({"data": "", "error": "File type is not supported."}, status=415)

        category_obj = Category.objects.get(pk=file_related_data.get('file_category'))

        file_data_object = FileData(title=file_title, category=category_obj, data=processed_data, uploaded_by=user)
        file_data_object.save()

        message = "File processed successfully."
        return JsonResponse({"data": {"message": message}, "error": ""}, status=200)


def process_xlsx_file(uploaded_file):
    wb = openpyxl.load_workbook(uploaded_file, data_only=True)
    sheet = wb.active
    cols = []
    file_data_json = {}
    for col in sheet.iter_cols(min_row=3, max_row=3, min_col=1, max_col=6):
        for cell in col:
            cols.append(cell.value)
    count = 1
    for row in sheet.iter_rows(min_row=4, min_col=1, max_col=6):
        row_values = [cell.value for cell in row]
        cur_row = {}
        for i in range(0, len(cols)):
            cur_row[str(cols[i])] = row_values[i]
        file_data_json[str(count)] = cur_row
        count += 1
    return file_data_json


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
    print(request)
    file_id = request.GET.get('id', None)
    # data = JSONParser().parse(request)
    # print(data)
    # file_id = data.get('id')
    file_data = FileData.objects.get(pk=file_id)
    serializer = FileDataSerializer(file_data, many=False)
    data = serializer.data
    return JsonResponse({"data": {"data": data}, "error": ""}, status=200)

@csrf_exempt
def update_records(request):
    updated_file_data = json.loads(request.POST.get('data'))
    file_title = file_related_data.get('file_name')
    file_type = file_related_data.get('file_type')
    updated_file = request.FILES.get('uploaded_file')
    if file_type == "csv":
        processed_data = process_file(uploaded_file)
    elif file_type == "xlsx":
        processed_data = process_xlsx_file(uploaded_file)
    else:
        return JsonResponse({"data": "", "error": "File type is not supported."}, status=415)

