from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from rest_framework.parsers import JSONParser
# from django.contrib.auth import views as auth_views
# from django.urls import reverse_lazy
from core.decorators import authenticate_user
from core.serializers import UserSerializer


from microservice_apis.send_email import send_email

# from microservice_apis.send_email import send_password_reset_email

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
        return JsonResponse({"data": "", "error": str(e)}, status=500)


@csrf_exempt
@require_POST
@authenticate_user
def change_password(request, user):
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

            # Prepare email content
            subject = "Password Reset Code"
            # message = f"Your password reset code is: {code}"

            # Call send_email function
            if send_email(user_instance.email, subject, code, user_instance.username):
                message = "An email has been sent to you. Please enter the code to change your password."
                data = {"message": message, "username": user_instance.username, "code": code}
                return JsonResponse({"data": data, "error": ""}, status=200)
            else:
                return JsonResponse({"data": "", "error": "Failed to send email. Please try again later."},
                                    status=500)
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

# class CustomPasswordResetView(auth_views.PasswordResetView):
#     template_name = 'password_reset.html'  # Path to your custom template
#     email_template_name = 'password_reset_email.html'  # Path to your custom email template
#     subject_template_name = 'custom_password_reset_subject.txt'
#     success_url = reverse_lazy('password_reset_done')
