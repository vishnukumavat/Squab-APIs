from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from authentication import views as authentication_views

urlpatterns = [
    path(
        r"user/signup",
        authentication_views.RegisterUserView.as_view(),
        name="RegisterUser",
    ),
    path(
        r"user/verify/email",
        authentication_views.VerifyEmailVerificationOTPView.as_view(),
        name="VerifyEmailVerificationOTP",
    ),
    path(
        r"user/resend/otp",
        authentication_views.ResendOTPView.as_view(),
        name="ResendOTP",
    ),
    path(
        r"user/social/login",
        authentication_views.UserSocialLoginView.as_view(),
        name="UserLogin",
    ),
    path(
        r"user/password/login",
        authentication_views.UserEmailPasswordLoginView.as_view(),
        name="UserEmailPasswordLogin",
    ),
    path(
        r"user/logout",
        authentication_views.UserLogoutView.as_view(),
        name="UserLogout",
    ),
    path(
        r"user/forgot/password/otp",
        authentication_views.CreateForgotPasswordOTPView.as_view(),
        name="CreateForgotPasswordOTP",
    ),
    path(
        r"user/forgot/password/otp/verify",
        authentication_views.VerifyForgotPasswordOTPView.as_view(),
        name="VerifyForgotPasswordOTP",
    ),
    path(
        r"user/update/password",
        authentication_views.UserPasswordSetResetView.as_view(),
        name="UserPasswordSetReset",
    ),
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)
