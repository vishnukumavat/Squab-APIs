from django.contrib.auth.hashers import make_password, check_password
from django.utils.crypto import get_random_string
from django.conf import settings
from authentication.constants import RESEND_OTP_CHOICES
from common.constants import EMAIL_TEMPLATE_LIBRARY
from users.models import UsersModel
from authentication.models import UserPasswordModel, UserLoginModel
from random import randint
from django.utils import timezone
from common.email_service import SendTemplateEmail
from datetime import timedelta
from common.helper_funcs import generate_session_token


class UserPasswordSetReset(object):
    def __init__(self, user_id, raw_password, confirm_raw_password):
        self.user_id = user_id
        self.raw_password = raw_password
        self.confirm_raw_password = confirm_raw_password

    def _create_or_update_password(self):
        user_password_obj, is_created = UserPasswordModel.objects.update_or_create(
            user_id=self.user_id,
            is_active=True,
            defaults={
                "password": make_password(
                    self.raw_password, salt=settings.PASSWORD_SALT
                ),
            },
        )

    def _match_passwords(self):
        if self.raw_password != self.confirm_raw_password:
            return {"result": "error", "message": "Password not matched"}
        return {"result": "success"}

    def perform_tasks(self):
        resp = self._match_passwords()
        if resp.get("result") == "error":
            return resp
        self._create_or_update_password()
        return {"result": "success", "message": "Password Updated Successfully"}


class CreateForgotPasswordOTP(object):
    def __init__(self, email_id):
        self.email_id = email_id

    def _user_exists_with_email(self):
        return UsersModel.objects.filter(email_id=self.email_id).first()

    def _create_or_update_otp(self, user_id, otp):
        user_password_obj, is_created = UserPasswordModel.objects.update_or_create(
            user_id=user_id,
            is_active=True,
            defaults={
                "otp": otp,
                "is_otp_verified": False,
                "otp_created_at": timezone.now(),
            },
        )
        if is_created:
            user_password_obj.password = make_password(
                get_random_string(length=16), salt=settings.PASSWORD_SALT
            )
            user_password_obj.save()

    def _send_otp_email(self, user_obj, otp):
        user_name = (
            user_obj.first_name + " " + user_obj.last_name if user_obj.last_name else ""
        )
        user_name = user_name.title()
        email_resp = SendTemplateEmail(
            user_id=user_obj.id,
            email_type="forgot_password",
            subject_fields_data={"user_name": user_name},
            html_fields_data={"user_name": user_name, "otp": otp},
        ).perform_tasks()
        return email_resp

    def _generate_otp_and_send_email(self, user_obj):
        otp = randint(100000, 999999)
        self._create_or_update_otp(user_id=user_obj.id, otp=otp)
        return self._send_otp_email(user_obj=user_obj, otp=otp)

    def _send_otp(self, user_obj):
        resp = self._generate_otp_and_send_email(user_obj=user_obj)
        if resp.get("result") == "error":
            return {
                "result": "error",
                "message": "Something went wrong, Please try again",
            }
        return {
            "result": "success",
            "message": f"OTP Sent Successfully to {self.email_id}",
        }

    def perform_tasks(self):
        user_obj = self._user_exists_with_email()
        if user_obj:
            return self._send_otp(user_obj)
        return {
            "result": "error",
            "message": "Invalid email, Please retry with correct Email",
        }


class VerifyForgotPasswordOTP(object):
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

    def _update_or_create_user_session(self, user_obj):
        user_id = user_obj.id
        user_login_object, is_created = UserLoginModel.objects.update_or_create(
            user_id=user_id,
            client_id=self.client_id,
            platform="email_password",
            is_active=True,
            defaults={
                "client_type": self.client_type,
                "client_description": self.client_description,
                "ipv4_address": self.ipv4_address,
                "session_token": self.new_session_token,
            },
        )
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
            self._update_or_create_user_session(user_obj)
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


class ResendOTP(object):
    def __init__(self, email_id, otp_type):
        self.email_id = email_id
        self.type = otp_type

    def _user_exists_with_email(self):
        return UsersModel.objects.filter(email_id=self.email_id, is_active=True).first()

    def _create_or_update_otp(self, user_id, otp):
        user_password_obj, is_created = UserPasswordModel.objects.update_or_create(
            user_id=user_id,
            is_active=True,
            defaults={
                "otp": otp,
                "is_otp_verified": False,
                "otp_created_at": timezone.now(),
            },
        )
        if is_created:
            user_password_obj.password = make_password(
                get_random_string(length=16), salt=settings.PASSWORD_SALT
            )
            user_password_obj.save()

    def _send_otp_email(self, user_id, otp):
        user_name = self.email_id.split("@")[0]
        email_resp = SendTemplateEmail(
            user_id=user_id,
            email_type=self.type,
            subject_fields_data={"user_name": user_name},
            html_fields_data={"user_name": user_name, "otp": otp},
        ).perform_tasks()
        return email_resp

    def _generate_otp_and_send_email(self, user_id):
        otp = randint(100000, 999999)
        self._create_or_update_otp(user_id=user_id, otp=otp)
        return self._send_otp_email(user_id=user_id, otp=otp)

    def perform_tasks(self):
        if self.type in RESEND_OTP_CHOICES:
            user_obj = self._user_exists_with_email()
            if user_obj:
                return self._generate_otp_and_send_email(user_obj.id)
            return {
                "result": "error",
                "message": "Invalid Email Id",
            }
        return {"result": "error", "message": "Invalid email type"}
