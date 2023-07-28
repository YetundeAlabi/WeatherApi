import random

from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    SignUpSerializer, LoginSerializer, ResetPasswordSerializer, ForgetPasswordSerializer, VerifyPinSerializer
                    )
from utils import Util


def generate_otp():
    otp = str(random.randint(1000, 9999)) #generate 4 digits random number as otp
    return otp

# Create your views here.
class SignUpAPIView(GenericAPIView):
    serializer_class = SignUpSerializer
    queryset = User.objects.all()

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"status": True, "message": "Account created successfullly.", "data":serializer.data}, status=status.HTTP_201_CREATED)
        return Response({"status": False, "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

class LoginAPIView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            token = RefreshToken.for_user(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            return Response({"status": True, "refresh": refresh_token, "access": access_token}, status=status.HTTP_200_OK)
        return Response({"status": False, "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class ForgetPasswordView(GenericAPIView):
    serializer_class = ForgetPasswordSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data.get('email')
            try:
                user = User.objects.filter(email=email).get()
            except User.DoesNotExist:
                return Response({"status": False,"error": "Invalid email address. Enter a correct email address"}, status=status.HTTP_400_BAD_REQUEST)

            user.verification_code = generate_otp()
            user.save(update_fields=["verification_code"])
            #send email
            subject = "Password Reset Verification Pin"
            body = f'Your verification pin is {generate_otp()}'
            data = {"email_body": body, "to_email": email,
                    "email_subject": subject}
            Util.send_email(data)
            return Response({'status': True,'message': 'Verification pin sent successfully'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyPinView(GenericAPIView):
    serializer_class = VerifyPinSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data["email"]
        verification_code = serializer.validated_data["verification_code"]
        try:
            user = User.objects.filter(email=email).get()
        except User.DoesNotExist: 
            return Response({"message": "Incorrect credential"}, status=status.HTTP_404_NOT_FOUND)
        print(user.verification_code)
        if user.verification_code != verification_code:
            return Response({"message": "Incorrect verification pin."}, status=status.HTTP_400_BAD_REQUEST)
        user.verification_code = ""
        user.save(update_fields=["verification_code"])
        return Response({"message": "verification successful"}, status=status.HTTP_200_OK)


class ResetPasswordView(GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            new_password = serializer.validated_data['new_password']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({"message": "Incorrect credential"}, status=status.HTTP_404_NOT_FOUND)
            user.set_password(new_password)
            user.save()
            return Response({"status": True, "message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response({"status": False, "errors":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    