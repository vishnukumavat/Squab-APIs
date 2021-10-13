from django.db import models
from django.core.validators import RegexValidator


MALE = "male"
FEMALE = "female"
OTHER = "other"

GENDER_CHOICES = ((MALE, "male"), (FEMALE, "female"), (OTHER, "other"))

TIME_ZONE_VALIDATOR = RegexValidator(r"UTC[+-][0-9]{2}:[0-9]{2}")


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    extra_details = models.JSONField(default=dict, blank=True, null=True)

    class Meta:
        abstract = True


class CountryDataModel(BaseModel):
    country_name = models.CharField(max_length=64)
    iso_code = models.CharField(max_length=16)
    dialing_code = models.IntegerField()
    time_zone = models.CharField(max_length=16, validators=[TIME_ZONE_VALIDATOR])
    icon_link = models.CharField(max_length=256)

    class Meta:
        db_table = "country_data"
