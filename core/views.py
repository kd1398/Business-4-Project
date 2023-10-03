from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from rest_framework_simplejwt.authentication import JWTAuthentication

from core.serializers import UserSerializer

# Create your views here.

UserModel = get_user_model()


@csrf_exempt
def user_list(request):
    tup = JWTAuthentication().authenticate(request)
    print(tup)
    return JsonResponse({"error": "Invalid JSON data."}, status=200)


    # if request.method == "GET":
    #     users = UserModel.objects.all()
    #     serializer = UserSerializer(users, many=True)
    #     return JsonResponse(serializer.data, safe=False)


@csrf_exempt
def create_user(request):
    if request.method == "POST":
        data = JSONParser().parse(request)
        print(data)

    return JsonResponse({"error": "Invalid JSON data."}, status=200)
