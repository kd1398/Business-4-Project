import csv
import openpyxl
from openpyxl.utils.exceptions import InvalidFileException

import json

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET

from core.decorators import authenticate_user
from data.models import FileData, Category
from data.serializers import CategorySerializer, FileDataSerializer, FileDataIDSerializer


# Create your views here.
@csrf_exempt
@authenticate_user
def get_file_categories(request, user):
    try:
        if request.method == "GET":
            categories = Category.objects.all()
            serializer = CategorySerializer(categories, many=True)
            category_data = serializer.data
            return JsonResponse({"data": {"data": category_data}, "error": ""}, status=200)
        else:
            return JsonResponse({"data": "", "error": "Invalid request method. Only GET is supported."}, status=405)
    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "No file categories found."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_names(request, user):
    try:
        if request.method == "GET":
            file_data = FileData.objects.all()
            serializer = FileDataIDSerializer(file_data, many=True)
            data = serializer.data
            return JsonResponse({"data": {"data": data}, "error": ""}, status=200)
        else:
            return JsonResponse({"data": "", "error": "Invalid request method. Only GET is supported."}, status=405)
    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "No file names found."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
@authenticate_user
def upload_file(request, user):
    try:
        if request.method == "POST":
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

            category_id = file_related_data.get('file_category')
            try:
                category_obj = Category.objects.get(pk=category_id)
            except ObjectDoesNotExist:
                return JsonResponse({"data": "", "error": f"Category with ID {category_id} not found."}, status=404)

            file_data_object = FileData(title=file_title, category=category_obj, data=processed_data, uploaded_by=user)
            file_data_object.save()

            message = "File processed successfully."
            return JsonResponse({"data": {"message": message}, "error": ""}, status=200)
        else:
            return JsonResponse({"data": "", "error": "Invalid request method. Only POST is supported."}, status=405)

    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


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
        raise ValueError("Invalid file format. This is not a valid Excel file.")
    except Exception as e:
        raise ValueError(f"Error processing the Excel file: {str(e)}")


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
        raise ValueError("Invalid file encoding. The file should be in UTF-8 encoding.")
    except csv.Error as e:
        raise ValueError(f"CSV parsing error: {str(e)}")
    except Exception as e:
        raise ValueError(f"Error processing the CSV file: {str(e)}")


@csrf_exempt
@require_GET
@authenticate_user
def get_file_data(request, user):
    try:
        if request.method == "GET":
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
        else:
            return JsonResponse({"data": "", "error": "Invalid request method. Only GET is supported."}, status=405)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)