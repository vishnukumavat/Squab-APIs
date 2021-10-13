from rest_framework import serializers

from users.services.v1.user_profile_service import UpdateUserProfile


class UpdateUserProfileSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    first_name = serializers.CharField(required=False)
    last_name = serializers.CharField(required=False)
    user_mobile = serializers.CharField(required=False)
    dialing_code = serializers.ChoiceField(required=False, choices=["91"])
    gender = serializers.ChoiceField(
        required=False, choices=["male", "female", "others"]
    )
    profile_pic_link = serializers.CharField(required=False)
    user_dob = serializers.DateField(required=False, format="%Y-%m-%d")
    country_iso_code = serializers.ChoiceField(required=False, choices=["IND"])

    def save(self):
        data = UpdateUserProfile(self.validated_data).perform_tasks()
        return data
