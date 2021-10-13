from django.db import models
from common.models import BaseModel, MALE, GENDER_CHOICES

# Create your models here.


class UsersModel(BaseModel):
    first_name = models.CharField(max_length=128, null=True, blank=True)
    last_name = models.CharField(max_length=128, blank=True, null=True)
    email_id = models.EmailField(db_index=True, unique=True, blank=False, null=False)
    user_mobile = models.CharField(max_length=12, null=True, blank=True)
    dialing_code = models.CharField(max_length=8, null=True, blank=True)
    gender = models.CharField(max_length=16, default=MALE, choices=GENDER_CHOICES)
    user_dob = models.DateField(blank=True, null=True)
    country_data = models.ForeignKey(
        "common.CountryDataModel", on_delete=models.CASCADE, null=True, blank=True
    )
    profile_pic_link = models.CharField(max_length=512, null=True, blank=True)

    class Meta(object):
        db_table = "users"
