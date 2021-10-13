from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers as authentication_serializers
from common.decorators import meta_data_response, session_authorize
from common.helper_funcs import get_client_ip_from_request


class RegisterUserView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = authentication_serializers.RegisterUserSerializer(
            data=request_data
        )
        if serializer.is_valid():
            otp_data = serializer.trigger_event()
            return Response(otp_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyEmailVerificationOTPView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        request_data.update(
            {
                "client_type": "web",
                "client_description": request.META.get("HTTP_USER_AGENT"),
                "ipv4_address": get_client_ip_from_request(request),
            }
        )
        serializer = authentication_serializers.VerifyEmailVerificationOTPSerializer(
            data=request_data
        )
        if serializer.is_valid():
            otp_data = serializer.verify_otp()
            return Response(otp_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class ResendOTPView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = authentication_serializers.ResendOTPSerializer(data=request_data)
        if serializer.is_valid():
            otp_data = serializer.trigger_event()
            return Response(otp_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserSocialLoginView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        request_data.update(
            {
                "platform": "google",
                "client_type": "web",
                "client_description": request.META.get("HTTP_USER_AGENT"),
                "ipv4_address": get_client_ip_from_request(request),
            }
        )
        serializer = authentication_serializers.UserSocialLoginSerializer(
            data=request_data
        )
        if serializer.is_valid():
            user_login_data = serializer.trigger_event()
            return Response(user_login_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserEmailPasswordLoginView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        request_data.update(
            {
                "client_type": "web",
                "client_description": request.META.get("HTTP_USER_AGENT"),
                "ipv4_address": get_client_ip_from_request(request),
            }
        )
        serializer = authentication_serializers.UserEmailPasswordLoginSerializer(
            data=request_data
        )
        if serializer.is_valid():
            user_login_data = serializer.trigger_event()
            return Response(user_login_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserLogoutView(APIView):
    @meta_data_response()
    @session_authorize()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = authentication_serializers.UserLogoutSerializer(data=request_data)
        if serializer.is_valid():
            user_logout_data = serializer.trigger_event()
            return Response(user_logout_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class CreateForgotPasswordOTPView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = authentication_serializers.CreateForgotPasswordOTPSerializer(
            data=request_data
        )
        if serializer.is_valid():
            otp_data = serializer.trigger_event()
            return Response(otp_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class VerifyForgotPasswordOTPView(APIView):
    @meta_data_response()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        request_data.update(
            {
                "client_type": "web",
                "client_description": request.META.get("HTTP_USER_AGENT"),
                "ipv4_address": get_client_ip_from_request(request),
            }
        )
        serializer = authentication_serializers.VerifyForgotPasswordOTPSerializer(
            data=request_data
        )
        if serializer.is_valid():
            otp_data = serializer.verify_otp()
            return Response(otp_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )


class UserPasswordSetResetView(APIView):
    @meta_data_response()
    @session_authorize()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = authentication_serializers.UserPasswordSetResetSerializer(
            data=request_data
        )
        if serializer.is_valid():
            user_password_data = serializer.trigger_event()
            return Response(user_password_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
