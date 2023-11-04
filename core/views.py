from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser

from core.decorators import authenticate_user
from core.models import CustomUserRoles
from core.serializers import UserSerializer

# Create your views here.

UserModel = get_user_model()


@csrf_exempt
@authenticate_user
def user_list(request, user, **kwargs):
    try:
        if not user.is_staff:
            return JsonResponse({"data": "", "error": "You are not authorized to view this."}, status=403)

        try:
            users = UserModel.objects.all()
        except DatabaseError as db_error:
            return JsonResponse({"data": "", "error": f"Database error: {str(db_error)}"}, status=500)

        serializer = UserSerializer(users, many=True)
        user_list_data = serializer.data
        return JsonResponse({"data": {"user_list": user_list_data}, "error": ""}, status=200)

    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "User does not exist."}, status=404)

    except Exception as e:
        return JsonResponse({"data": "", "error": str(e)}, status=500)


@csrf_exempt
@require_POST
@authenticate_user
def change_password(request, user, **kwargs):
    message = ""
    try:
        data = JSONParser().parse(request)
        new_password = data.get('password')

        if new_password:
            user.set_password(new_password)

            if data.get('fromForgetPassword'):
                user.is_password_reset = True
            user.save()

            message = "Password changed successfully."
            error = ""
        else:
            error = "New password not provided."
    except ObjectDoesNotExist:
        return JsonResponse({"data": "", "error": "User does not exist."}, status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": str(e)}, status=500)

    return JsonResponse({"data": {"message": message}, "error": error}, status=200)


@csrf_exempt
@require_POST
def forget_password(request):
    try:
        data = JSONParser().parse(request)
        username_or_email = data.get('usernameOrEmail')
        user_query_data = UserModel.objects.filter(Q(username=username_or_email) | Q(email=username_or_email))
        if user_query_data.exists():
            user_instance = user_query_data[0]
            code = user_instance.generate_forget_password_key()
            user_instance.is_password_reset = False
            user_instance.save()
            # TODO: Send Email Function Call Goes Here
            message = "An email has been sent to you. Please enter the code to change your password."
            data = {"message": message,
                    "username": user_instance.username,
                    "code": code}
            return JsonResponse({"data": data, "error": ""}, status=200)
        else:
            return JsonResponse({"data": "", "error": "User not found. Please check your username or email."},
                                status=404)
    except Exception as e:
        return JsonResponse({"data": "", "error": str(e)}, status=500)


@csrf_exempt
@require_POST
def create_user(request):
    data = JSONParser().parse(request)
    print(data)

    return JsonResponse({"error": "Invalid JSON data."}, status=200)


@csrf_exempt
@require_POST
@authenticate_user
def add_new_user_role(request, user, permissions):
    message = ""
    error = ""
    status = 200
    if permissions.get("can_add_new_roles"):
        try:
            data = JSONParser().parse(request)
            title = data.get("title")
            can_modify_module = data.get("can_modify_module")
            can_modify_category = data.get("can_modify_category")
            can_modify_user = data.get("can_modify_user")
            can_add_new_user = data.get("can_add_new_user")
            can_add_new_roles = data.get("can_add_new_roles")
            custom_user_role_obj = CustomUserRoles.objects.create(title=title, can_modify_user=can_modify_user,
                                                                 can_modify_category=can_modify_category,
                                                                 can_modify_module=can_modify_module,
                                                                 can_add_new_user=can_add_new_user,
                                                                 can_add_new_roles=can_add_new_roles)
            message = "Role added successfully."
        except Exception as e:
            error = str(e)
            status = 400

        return JsonResponse({"data": {"message": message}, "error": error}, status=status)
    else:
        error = "You do not have the permission to add new roles."
        status = 403
        return JsonResponse({"data": {}, "error": error}, status=status)


@csrf_exempt
@require_POST
@authenticate_user
def add_new_user(request, user, permissions):
    message = ""
    error = ""
    status = 200
    if permissions.get("can_add_new_user"):
        try:
            data = JSONParser().parse(request)
            username = data.get("username")
            email = data.get("email")
            temp_password = data.get("temp_password")
            user_obj = UserModel.objects.create(username=username, email=email)
            user_obj.set_password(temp_password)
            user_obj.save()
            message = "User added successfully."
        except Exception as e:
            error = str(e)
            status = 400

        return JsonResponse({"data": {"message": message}, "error": error}, status=status)
    else:
        error = "You do not have the permission to add new users."
        status = 403
        return JsonResponse({"data": {}, "error": error}, status=status)
