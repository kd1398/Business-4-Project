import csv

import pandas as pd
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST
from rest_framework.parsers import JSONParser

from core.decorators import authenticate_user
from data.models import Category, Module, FileData, FileDataHistory
from data.serializers import FileDataSerializer, FileDataIDSerializer


@csrf_exempt
@require_POST
@authenticate_user
def update_file_data(request, user, permissions):
    message = ''
    error = ''
    status = 200
    if not permissions.get('can_modify_files'):
        status = 401
        error = "You are not authorized to perform this action."
        return JsonResponse({"data": "", "error": error}, status=status)

    try:
        data = JSONParser().parse(request)
        file_id = data.get('file_id')
        row_num = data.get('row_num')
        row_data = data.get('row_data')

        file_obj = FileData.objects.get(pk=file_id)
        file_history_obj = FileDataHistory.objects.create(title=file_obj.title, data=file_obj.data,
                                                          original_file=file_obj,
                                                          uploaded_by=user)
        data = file_obj.data
        data[row_num] = row_data
        file_obj.save()

        message = 'Data updated successfully.'
    except Exception as e:
        message = ''
        error = str(e)
        status = 400
    return JsonResponse({"data": {"message": message}, "error": error}, status=status)


@csrf_exempt
@require_GET
@authenticate_user
def get_file_names(request, user, **kwargs):
    try:
        file_data = FileData.objects.filter().order_by('-modified_at')
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
def upload_file(request, user, permissions):
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
                processed_data = process_xlsx_file_new(uploaded_file)
            else:
                return JsonResponse({"data": "", "error": "File type is not supported."}, status=415)
            category_id = request.POST.get('file_category')
            module_id = request.POST.get('file_module')
            try:
                category_obj = Category.objects.get(pk=category_id)
                module_obj = Module.objects.get(pk=module_id)
            except ObjectDoesNotExist:
                return JsonResponse({"data": "", "error": "Module or Category ID not found."}, status=404)

            file_data_object = FileData.objects.create(title=file_title, category=category_obj, data=processed_data,
                                                       uploaded_by=user,
                                                       module=module_obj)

            message = "File processed successfully."
            return JsonResponse({"data": {"message": message}, "error": ""}, status=200)
        except Exception as e:
            return JsonResponse({"data": "", "error": {str(e)}}, status=500)


def process_xlsx_file_new(uploaded_file):
    error = ""
    try:
        df = pd.read_excel(uploaded_file)
        data = df.to_dict(orient='records')
        count = 1
        json_data = {}
        for row in data:
            json_data[count] = row
            count += 1
        return json_data
    except Exception as e:
        error = f"Error processing the XLSX file: {str(e)}"
    return JsonResponse({"data": "", "error": error}, status=500)


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
def get_file_data(request, user, **kwargs):
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

    # TODO: Create new method for filtering
    # input:
    # moduleid
    # categoryid

    # data = FileData.objects.filter(module=Module.objects.get(pk=module_id), category=Category.objects.get(pk=category_id))
    # handle if either of them is empty. If anyone of the ids is empty .get will generate error. Handle that!
    # FileDataSerializer(data, many=True)


@csrf_exempt
@require_GET
@authenticate_user
def filter_file_data(request, user, **kwargs):
    module_id = request.GET.get('module_id')
    category_id = request.GET.get('category_id')

    print("Module ID:", module_id)
    print("Category ID:", category_id)

    if not module_id and not category_id:
        return JsonResponse({"data": "", "error": "No filtering parameters provided."}, status=400)

    file_qs = FileData.objects.all()

    if module_id:
        module_obj = get_object_or_404(Module, pk=module_id)
        file_qs = file_qs.filter(module=module_obj)
        print("After Module Filter:", file_qs)

    if category_id:
        category_obj = get_object_or_404(Category, pk=category_id)
        file_qs = file_qs.filter(category=category_obj)
        print("After Category Filter:", file_qs)

    data = FileDataSerializer(file_qs, many=True).data
    return JsonResponse({"data": data, "error": ""}, status=200)
