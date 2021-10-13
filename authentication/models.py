from django.db import models
from common.models import BaseModel, MALE, GENDER_CHOICES

PLATFORM_DEFAULT = "google"


class UserLoginModel(BaseModel):
    user = models.ForeignKey("users.UsersModel", on_delete=models.CASCADE)
    platform = models.CharField(max_length=256, default=PLATFORM_DEFAULT)
    platform_token = models.TextField(editable=False, blank=True, null=False)
    client_id = models.CharField(max_length=64, unique=True)
    client_type = models.CharField(max_length=16)
    client_description = models.TextField(editable=False, blank=True, null=True)
    ipv4_address = models.CharField(max_length=16)
    session_token = models.CharField(
        db_index=True,
        unique=True,
        editable=False,
        blank=True,
        null=True,
        max_length=256,
    )

    class Meta(object):
        db_table = "user_login"


class UserPlatformProfileModel(BaseModel):
    user = models.ForeignKey("users.UsersModel", on_delete=models.CASCADE)
    email_id = models.EmailField(db_index=True, unique=True, blank=False, null=False)
    first_name = models.CharField(max_length=256)
    last_name = models.CharField(max_length=256, default="")
    profile_pic_link = models.URLField(max_length=500)
    gender = models.CharField(max_length=16, default=MALE, choices=GENDER_CHOICES)
    platform = models.CharField(max_length=64, default=PLATFORM_DEFAULT)
    platform_user_id = models.CharField(max_length=256, blank=False, null=False)
    data = models.JSONField(default=dict)

    class Meta(object):
        db_table = "user_platform_profile"
        unique_together = ("email_id", "platform")


class UserPasswordModel(BaseModel):
    user = models.OneToOneField("users.UsersModel", on_delete=models.CASCADE)
    password = models.CharField(max_length=512, editable=False, null=True)
    otp = models.IntegerField(editable=False, null=True)
    is_otp_verified = models.BooleanField(default=False, null=True)
    otp_created_at = models.DateTimeField(null=True)

    class Meta(object):
        db_table = "user_password"
