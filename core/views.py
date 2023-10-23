from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser

from core.decorators import authenticate_user
from core.serializers import UserSerializer

# Create your views here.

UserModel = get_user_model()


@csrf_exempt
@authenticate_user
def user_list(request, user):
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
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
@authenticate_user
def change_password(request, user):
    error = ""
    message = ""
    if request.method == "POST":
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
            return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)
    else:
        error = "Invalid request method. Only POST is supported."

    return JsonResponse({"data": {"message": message}, "error": error}, status=200)


@csrf_exempt
def forget_password(request):
    try:
        if request.method == "POST":
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
        else:
            return JsonResponse({"data": "", "error": "Invalid request method. Only POST is supported."},
                                status=405)
    except Exception as e:
        return JsonResponse({"data": "", "error": f"Internal server error: {str(e)}"}, status=500)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data)

    return JsonResponse({"error": "Invalid JSON data."}, status=200)
