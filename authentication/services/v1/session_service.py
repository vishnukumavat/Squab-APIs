from django.contrib.auth.hashers import check_password
from authentication.services.v1 import platform_service
from authentication.models import (
    UserLoginModel,
    UserPasswordModel,
    UserPlatformProfileModel,
)
from users.models import UsersModel
from django.db import transaction
from common.helper_funcs import generate_session_token


class UserSocialLogin(object):
    def __init__(self, login_data):
        self.platform = login_data["platform"]
        self.platform_token = login_data["platform_token"]
        self.client_id = login_data["client_id"]
        self.client_type = login_data.get("client_type")
        self.client_description = login_data.get("client_description")
        self.ipv4_address = login_data.get("ipv4_address")
        self.social_profile = self._platform_profile()
        self.new_session_token = generate_session_token(self.client_id)
        self.is_new_user = False

    def _platform_profile(self):
        user_platform_profile_obj = platform_service.PlatformProfile(
            self.platform, self.platform_token
        )
        return user_platform_profile_obj.perform_task()

    def _get_or_create_user(self):
        user_object, is_created = UsersModel.objects.get_or_create(
            email_id=self.social_profile["email_id"],
            is_active=True,
            defaults={
                "first_name": self.social_profile["first_name"],
                "last_name": self.social_profile.get("last_name", ""),
                "profile_pic_link": self.social_profile["profile_pic_link"],
            },
        )
        self.is_new_user = is_created
        return user_object

    def _update_or_create_user_login(self, user_object):
        user_id = user_object.id
        user_login_object, is_created = UserLoginModel.objects.update_or_create(
            user_id=user_id,
            client_id=self.client_id,
            platform=self.platform,
            is_active=True,
            defaults={
                "platform_token": self.platform_token,
                "client_type": self.client_type,
                "client_description": self.client_description,
                "ipv4_address": self.ipv4_address,
                "session_token": self.new_session_token,
            },
        )
        return user_login_object

    def _update_or_create_user_platform_profile(self, user_object):
        user_id = user_object.id
        (
            platform_profile_obj,
            is_created,
        ) = UserPlatformProfileModel.objects.update_or_create(
            user_id=user_id,
            email_id=self.social_profile["email_id"],
            platform=self.platform,
            is_active=True,
            defaults={
                "first_name": self.social_profile["first_name"],
                "last_name": self.social_profile["last_name"],
                "profile_pic_link": self.social_profile["profile_pic_link"],
                "gender": self.social_profile.get("gender", ""),
                "platform_user_id": self.social_profile["platform_user_id"],
            },
        )
        return platform_profile_obj

    def _get_response_data(self, user_id):
        response_data = {
            "result": "success",
            "session_token": self.new_session_token,
            "user_id": user_id,
            "first_name": self.social_profile["first_name"],
            "last_name": self.social_profile["last_name"],
            "email_id": self.social_profile["email_id"],
            "profile_pic_link": self.social_profile["profile_pic_link"],
            "new_user": self.is_new_user,
        }
        return response_data

    def perform_tasks(self):
        with transaction.atomic():
            user_object = self._get_or_create_user()
            self._update_or_create_user_login(user_object)
            self._update_or_create_user_platform_profile(user_object)
            return self._get_response_data(user_id=user_object.id)


class UserEmailPasswordLogin(object):
    def __init__(
        self,
        email_id,
        raw_password,
        client_id,
        client_type,
        client_description,
        ipv4_address,
    ):
        self.email_id = email_id
        self.raw_password = raw_password
        self.client_id = client_id
        self.client_type = client_type
        self.client_description = client_description
        self.ipv4_address = ipv4_address
        self.new_session_token = generate_session_token(self.client_id)

    def _user_exists_with_email(self):
        return UsersModel.objects.filter(email_id=self.email_id, is_active=True).first()

    def _is_valid_password(self, user_id):
        try:
            user_password_obj = UserPasswordModel.objects.get(
                user_id=user_id, is_active=True
            )
        except UserPasswordModel.DoesNotExist:
            user_password_obj = None
        if user_password_obj:
            return check_password(self.raw_password, user_password_obj.password)
        return False

    def _update_or_create_user_session(self, user_id):
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

    def _validate_password_and_create_session(self, user_obj):
        if self.raw_password and self._is_valid_password(user_obj.id):
            self._update_or_create_user_session(user_obj.id)
            return self._get_response_data()
        return {
            "result": "error",
            "message": "Password Incorrect",
        }

    def perform_tasks(self):
        user_obj = self._user_exists_with_email()
        if user_obj:
            return self._validate_password_and_create_session(user_obj)
        return {
            "result": "error",
            "message": "Invalid email, Please retry with correct Email",
        }


class UserLogout(object):
    def __init__(self, logout_data):
        self.session_token = logout_data["session_token"]
        self.user_id = logout_data["user_id"]

    def perform_tasks(self):
        UserLoginModel.objects.filter(
            session_token=self.session_token, user_id=self.user_id, is_active=True
        ).delete()
        return {"result": "success", "message": "Logged Out Successfully"}
