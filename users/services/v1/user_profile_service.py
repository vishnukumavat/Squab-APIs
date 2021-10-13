from common.models import CountryDataModel
from users.models import UsersModel


class UpdateUserProfile(object):
    def __init__(self, profile_data):
        self.user_id = profile_data["user_id"]
        self.profile_data = profile_data

    def _prepare_model_data(self):
        if self.profile_data.get("country_iso_code"):
            del self.profile_data["country_iso_code"]
        del self.profile_data["user_id"]

    def _update_country_id_in_profile_data(self):
        country_obj = CountryDataModel.objects.get(
            iso_code=self.profile_data["country_iso_code"], is_active=True
        )
        self.profile_data.update({"country_data_id": country_obj.id})

    def _update_user_data(self):
        if self.profile_data.get("country_iso_code"):
            self._update_country_id_in_profile_data()
        self._prepare_model_data()
        UsersModel.objects.filter(id=self.user_id, is_active=True).update(
            **self.profile_data
        )

    def perform_tasks(self):
        if not self.profile_data:
            return {"result": "error", "message": "No data Provided for update"}
        self._update_user_data()
        return {"result": "success", "message": "Profile Updated Successfully"}
