from django.contrib.auth import get_user_model
from django.http import JsonResponse
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

UserModel = get_user_model()


def authenticate_user(view_function):
    def wrapper(request, *args, **kwargs):
        try:
            # Authenticate the request using your JWT authentication logic
            user = JWTAuthentication().authenticate(request)
            if user:
                # Pass the authenticated user instance to the view function
                kwargs['user'] = user[0]
            else:
                return JsonResponse({"data": "", "error": "Please login."}, status=401)
        except InvalidToken as e:
            return JsonResponse({"data": "", "error": "Token Expired. Please login again."}, status=401)

        # Call the view function with the updated arguments
        return view_function(request, *args, **kwargs)

    return wrapper
