from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

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
    return JsonResponse({"data": serializer.data, "error": ""}, status=200)

@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data)

    return JsonResponse({"error": "Invalid JSON data."}, status=200)
