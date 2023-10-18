from django.contrib.auth import get_user_model
from django.db.models import Q
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
    if not user.is_staff:
        return JsonResponse({"data": "", "error": "You are not authorized to view this."}, status=403)

    users = UserModel.objects.all()
    serializer = UserSerializer(users, many=True)
    user_list_data = serializer.data
    return JsonResponse({"data": {"user_list": user_list_data}, "error": ""}, status=200)


@csrf_exempt
@authenticate_user
def change_password(request, user):
    if request.method == "POST":
        data = JSONParser().parse(request)
        user.set_password(data['password'])
        if data.get('fromForgetPassword'):
            user.is_password_reset = True
        user.save()
    return JsonResponse({"data": "", "error": ""}, status=200)


@csrf_exempt
def forget_password(request):
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
            return JsonResponse(
                {"data": "", "error": "Please check your username or email."},
                status=204)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data)

    return JsonResponse({"error": "Invalid JSON data."}, status=200)
