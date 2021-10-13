from rest_framework import serializers
from authentication import constants as authentication_constants
from authentication.services.v1 import (
    session_service,
    authentication_service,
    password_service,
    register_user,
)


class RegisterUserSerializer(serializers.Serializer):
    email_id = serializers.EmailField()

    def trigger_event(self):
        data = register_user.RegisterUser(**self.validated_data).perform_tasks()
        return data


class VerifyEmailVerificationOTPSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    otp = serializers.IntegerField()
    client_id = serializers.CharField()
    client_type = serializers.ChoiceField(
        choices=authentication_constants.CLIENT_CHOICES
    )
    client_description = serializers.CharField()
    ipv4_address = serializers.CharField()

    def verify_otp(self):
        data = register_user.VerifyEmailVerificationOTP(
            **self.validated_data
        ).perform_tasks()
        return data


class ResendOTPSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    otp_type = serializers.ChoiceField(
        choices=authentication_constants.RESEND_OTP_CHOICES
    )

    def trigger_event(self):
        data = password_service.ResendOTP(**self.validated_data).perform_tasks()
        return data


class UserSocialLoginSerializer(serializers.Serializer):
    platform = serializers.ChoiceField(
        choices=authentication_constants.PLATFORM_CHOICES
    )
    platform_token = serializers.CharField()
    client_id = serializers.CharField()
    client_type = serializers.ChoiceField(
        choices=authentication_constants.CLIENT_CHOICES
    )
    client_description = serializers.CharField()
    ipv4_address = serializers.CharField()

    def trigger_event(self):
        login_service_object = session_service.UserSocialLogin(self.validated_data)
        data = login_service_object.perform_tasks()
        return data


class UserEmailPasswordLoginSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    raw_password = serializers.IntegerField()
    client_id = serializers.CharField()
    client_type = serializers.ChoiceField(
        choices=authentication_constants.CLIENT_CHOICES
    )
    client_description = serializers.CharField()
    ipv4_address = serializers.CharField()

    def trigger_event(self):
        data = session_service.UserEmailPasswordLogin(
            **self.validated_data
        ).perform_tasks()
        return data


class UserLogoutSerializer(serializers.Serializer):
    session_token = serializers.CharField()
    user_id = serializers.IntegerField()

    def trigger_event(self):
        logout_service_obj = session_service.UserLogout(self.validated_data)
        data = logout_service_obj.perform_tasks()
        return data


class CreateForgotPasswordOTPSerializer(serializers.Serializer):
    email_id = serializers.EmailField()

    def trigger_event(self):
        data = password_service.CreateForgotPasswordOTP(
            **self.validated_data
        ).perform_tasks()
        return data


class VerifyForgotPasswordOTPSerializer(serializers.Serializer):
    email_id = serializers.EmailField()
    otp = serializers.IntegerField()
    client_id = serializers.CharField()
    client_type = serializers.ChoiceField(
        choices=authentication_constants.CLIENT_CHOICES
    )
    client_description = serializers.CharField()
    ipv4_address = serializers.CharField()

    def verify_otp(self):
        data = password_service.VerifyForgotPasswordOTP(
            **self.validated_data
        ).perform_tasks()
        return data


class UserPasswordSetResetSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    raw_password = serializers.CharField()
    confirm_raw_password = serializers.CharField()

    def trigger_event(self):
        data = password_service.UserPasswordSetReset(
            **self.validated_data
        ).perform_tasks()
        return data


class AuthenticationSerializer(serializers.Serializer):
    client_id = serializers.CharField()
    session_token = serializers.CharField()

    def verify_session(self):
        authentication_obj = authentication_service.Authentication(
            **self.validated_data
        )
        return authentication_obj.perform_tasks()
