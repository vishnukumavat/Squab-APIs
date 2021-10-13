from users.models import UsersModel
from common.email_service import SendTemplateEmail
from authentication.models import UserPasswordModel, UserLoginModel
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.utils.crypto import get_random_string
from django.conf import settings
from random import randint
from common.helper_funcs import generate_session_token
from datetime import timedelta
from django.db import transaction


class RegisterUser(object):
    def __init__(self, email_id):
        self.email_id = email_id

    def _user_exists_with_email(self):
        return UsersModel.objects.filter(email_id=self.email_id, is_active=True).first()

    def _create_user(self):
        user_object = UsersModel.objects.create(
            email_id=self.email_id,
            is_active=True,
            defaults={},
        )
        user_object.save()
        return user_object

    def _create_otp(self, user_id, otp):
        user_password_obj = UserPasswordModel.objects.create(
            user_id=user_id,
            is_active=True,
            otp=otp,
            is_otp_verified=False,
            otp_created_at=timezone.now(),
            password=make_password(
                get_random_string(length=16), salt=settings.PASSWORD_SALT
            ),
        )
        user_password_obj.save()

    def _send_otp_email(self, user_id, otp):
        user_name = self.email_id.split("@")[0]
        email_resp = SendTemplateEmail(
            user_id=user_id,
            email_type="email_verification",
            subject_fields_data={"user_name": user_name},
            html_fields_data={"user_name": user_name, "otp": otp},
        ).perform_tasks()
        return email_resp

    def _generate_otp_and_send_email(self, user_id):
        otp = randint(100000, 999999)
        self._create_otp(user_id=user_id, otp=otp)
        return self._send_otp_email(user_id=user_id, otp=otp)

    def perform_tasks(self):
        with transaction.atomic():
            user_obj = self._user_exists_with_email()
            if not user_obj:
                user_obj = self._create_user()
                return self._generate_otp_and_send_email(user_obj.id)
            return {
                "result": "error",
                "message": "Email Id already registered, Please try sigin using password",
            }


class VerifyEmailVerificationOTP(object):
    def __init__(
        self, email_id, otp, client_id, client_type, client_description, ipv4_address
    ):
        self.email_id = email_id
        self.otp = otp
        self.client_id = client_id
        self.client_type = client_type
        self.client_description = client_description
        self.ipv4_address = ipv4_address
        self.new_session_token = generate_session_token(self.client_id)

    def _user_exists_with_email(self):
        return UsersModel.objects.filter(email_id=self.email_id, is_active=True).first()

    def _is_valid_otp(self, user_id):
        try:
            user_password_obj = UserPasswordModel.objects.get(
                user_id=user_id,
                otp=self.otp,
                is_otp_verified=False,
                otp_created_at__gt=timezone.now() - timedelta(minutes=5),
                is_active=True,
            )
            user_password_obj.is_otp_verified = True
            user_password_obj.save()
        except UserPasswordModel.DoesNotExist:
            user_password_obj = None
        return True if user_password_obj else False

    def _create_user_session(self, user_obj):
        user_id = user_obj.id
        user_login_object = UserLoginModel.objects.create(
            user_id=user_id,
            client_id=self.client_id,
            platform="email_password",
            is_active=True,
            client_type=self.client_type,
            client_description=self.client_description,
            ipv4_address=self.ipv4_address,
            session_token=self.new_session_token,
        )
        user_login_object.save()
        return user_login_object

    def _get_response_data(self):
        response_data = {
            "result": "success",
            "session_token": self.new_session_token,
            "client_id": self.client_id,
        }
        return response_data

    def _verify_otp_and_create_session(self, user_obj):
        if self._is_valid_otp(user_obj.id):
            self._create_user_session(user_obj)
            return self._get_response_data()
        return {
            "result": "error",
            "message": "OTP Invalid/Expired, Please provide valid OTP",
        }

    def perform_tasks(self):
        user_obj = self._user_exists_with_email()
        if user_obj:
            return self._verify_otp_and_create_session(user_obj)
        return {
            "result": "error",
            "message": "Invalid email, Please retry with correct Email",
        }
