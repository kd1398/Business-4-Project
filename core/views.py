from django.contrib.auth import get_user_model
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView

from core.serializers import UserSerializer

# Create your views here.

UserModel = get_user_model()


@csrf_exempt
def user_list(request):

    if request.method == "GET":
        users = UserModel.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
