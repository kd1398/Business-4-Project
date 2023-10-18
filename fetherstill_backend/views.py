from django.contrib.auth import get_user_model, authenticate
from django.utils import timezone
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

UserModel = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        username = request.data['username']
        password = request.data['password']
        user_instance = authenticate(username=username, password=password)

        if user_instance is not None and not user_instance.is_password_reset and user_instance.key_expiry < timezone.now():
            custom_response = {
                "data": "",
                'error': "Key expired"
            }
            return Response(custom_response, status=401)

        if user_instance is None:
            custom_response = {
                "data": "",
                "error": "Please check your credentials"
            }
            return Response(custom_response, status=401)
        response = super().post(request, *args, **kwargs)
        access_token = response.data.get('access')
        custom_response = {
            'data': {
                'access_token': access_token
            },
            'error': ''
        }
        return Response(custom_response)
