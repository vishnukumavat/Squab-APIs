import requests
from django.conf import settings
from common.exceptions import ErrorMessage
from authentication import constants as authentication_constants


class PlatformProfile(object):
    def __init__(self, platform, platform_token):
        self.platform = platform
        self.platform_token = platform_token

    def _get_google_data(self, raw_user_data):
        user_data = {
            "platform": self.platform,
            "platform_user_id": raw_user_data["sub"],
            "first_name": raw_user_data["given_name"],
            "last_name": raw_user_data.get("family_name", ""),
            "email_id": raw_user_data["email"],
            "profile_pic_link": raw_user_data.get("picture", ""),
        }
        return user_data

    def _get_processed_user_data(self, raw_user_data):
        try:
            if self.platform == "google":
                return self._get_google_data(raw_user_data)
        except Exception as e:
            exception_string = (
                "SocialProfile._get_model_data: Data not found from the Platform token: "
                + str(self.platform)
                + " : "
                + str(e)
            )
            raise ErrorMessage(str(exception_string))

    def _fetch_user_data_from_token(self, token_url):
        try:
            data = requests.get(token_url)
            return data.json()
        except Exception as e:
            raise ErrorMessage("Social Media data not found due to: " + str(e))

    def _get_platform_token_url(self):
        platform_url_data = {
            "google": settings.EXTERNAL_URLS["GOOGLE"]["token_data_url"].format(
                platform_token=self.platform_token
            ),
        }
        if self.platform not in list(platform_url_data.keys()):
            raise ErrorMessage("Platform not supported")
        return platform_url_data[self.platform]

    def perform_task(self):
        token_url = self._get_platform_token_url()
        raw_user_data = self._fetch_user_data_from_token(token_url)
        return self._get_processed_user_data(raw_user_data=raw_user_data)
