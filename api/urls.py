from django.urls import path

from .views import SignUpAPIView, LoginAPIView, ForgetPasswordView, VerifyPinView, ResetPasswordView

app_name = 'api'
urlpatterns = [
    path('register/', SignUpAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name="login"),
    path('forgot-password/', ForgetPasswordView.as_view(), name="forget_password"),
    path('verify/', VerifyPinView.as_view(), name="verify_pin"),
    path('reset-password/', ResetPasswordView.as_view(), name="reset_password")
]
