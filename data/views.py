import csv
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

import json

from django.db import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.parsers import JSONParser

from core.decorators import authenticate_user
from data.models import FileData, Category, Module
from data.serializers import CategorySerializer, FileDataSerializer, FileDataIDSerializer, ModuleSerializer


# Create your views here.
@csrf_exempt
@require_GET
@authenticate_user
def get_file_categories(request, user):
    try:
        categories = Category.objects.all()
        serializer = CategorySerializer(categories, many=True)
        category_data = serializer.data
        return JsonResponse({"data": {"data": category_data}, "error": ""}, status=200)
    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "No file categories found."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
@require_POST
@authenticate_user
def add_new_category(request, user):
    data = JSONParser().parse(request)
    status = 200
    error = ""
    try:
        cat_name = data.get('name')
        cat = Category.objects.create(name=cat_name)
        message = "Category successfully added."

    except Exception as e:
        error = str(e)
        message = ""
        status = 400
    return JsonResponse({"data": {"message": message}, "error": error}, status=status)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_names(request, user):
    try:
        file_data = FileData.objects.all()
        serializer = FileDataIDSerializer(file_data, many=True)
        data = serializer.data
        return JsonResponse({"data": {"data": data}, "error": ""}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "No file names found."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
@require_POST
@authenticate_user
def upload_file(request, user):
    if 'update_value' in request.POST:
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
        try:
            file_title = request.POST.get('file_name')
            file_type = request.POST.get('file_type')
            uploaded_file = request.FILES.get('uploaded_file')

            if file_type == "csv":
                processed_data = process_file(uploaded_file)
            elif file_type == "xlsx":
                processed_data = process_xlsx_file(uploaded_file)
            else:
                return JsonResponse({"data": "", "error": "File type is not supported."}, status=415)

            category_id = request.POST.get('file_category')
            module_id = request.POST.get('file_module')
            try:
                category_obj = Category.objects.get(pk=category_id)
                module_obj = Module.objects.get(pk=module_id)
            except ObjectDoesNotExist:
                return JsonResponse({"data": "", "error": "Module or Category ID not found."}, status=404)

            file_data_object = FileData(title=file_title, category=category_obj, data=processed_data, uploaded_by=user,
                                        module=module_obj)
            file_data_object.save()

            message = "File processed successfully."
            return JsonResponse({"data": {"message": message}, "error": ""}, status=200)
        except Exception as e:
            return JsonResponse({"data": "", "error": {str(e)}}, status=500)


def process_xlsx_file(uploaded_file):
    try:
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
    except InvalidFileException:
        return JsonResponse({"data": "", "error": "Invalid file format. This is not a valid Excel file."}, status=500)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Error processing the Excel file: {str(e)}"}, status=500)


def process_file(uploaded_file):
    try:
        content = uploaded_file.read().decode('utf-8')
        csv_reader = csv.DictReader(content.splitlines())

        count = 1
        json_data = {}
        for row in csv_reader:
            json_data[count] = row
            count += 1
        return json_data
    except UnicodeDecodeError:
        error = "Invalid file encoding. The file should be in UTF-8 encoding."
    except csv.Error as e:
        error = f"CSV parsing error: {str(e)}"
    except Exception as e:
        error = f"Error processing the CSV file: {str(e)}"
    return JsonResponse({"data": "", "error": error}, status=500)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_data(request, user):
    try:
        file_id = request.GET.get('id', None)

        if file_id is None:
            return JsonResponse({"data": "", "error": "Missing 'id' parameter in the request."}, status=400)

        try:
            file_data = FileData.objects.get(pk=file_id)
            serializer = FileDataSerializer(file_data, many=False)
            data = serializer.data
            return JsonResponse({"data": {"data": data}, "error": ""}, status=200)
        except ObjectDoesNotExist:
            return JsonResponse({"data": "", "error": f"File with ID {file_id} not found."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": str(e)}, status=500)

@csrf_exempt
def update_records(request):
    updated_file_data = json.loads(request.POST.get('data'))
    file_title = updated_file_data.get('file_name')
    file_type = updated_file_data.get('file_type')
    updated_file = request.FILES.get('uploaded_file')
    if file_type == "csv":
        processed_data = process_file(updated_file)
    elif file_type == "xlsx":
        processed_data = process_xlsx_file(updated_file)
    else:
        return JsonResponse({"data": "", "error": "File type is not supported."}, status=415)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_modules(request, user):
    module_list = Module.objects.all()
    status = 200
    data = ModuleSerializer(module_list, many=True).data
    return JsonResponse({"data": {"data": data}, "error": ""}, status=status)


@csrf_exempt
@require_POST
@authenticate_user
def add_file_module(request, user):
    message = "Module added successfully."
    request_data = JSONParser().parse(request)
    error = ""
    status = 200
    try:
        module_name = request_data.get('name')
        module_obj = Module.objects.create(name=module_name)
        data = ModuleSerializer(module_obj, many=False).data
    except (IntegrityError, ValueError) as e:
        if type(e) == IntegrityError:
            error = "Module name should be unique"
        else:
            error = str(e)
        data = ""
        status = 400
        message = ""
    return JsonResponse({"data": {"data": data, "message": message}, "error": error}, status=status)
