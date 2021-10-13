from authentication.models import UserLoginModel


class Authentication(object):
    def __init__(self, client_id, session_token):
        self.client_id = client_id
        self.session_token = session_token

    def _get_user_id_from_session(self):
        login_obj = UserLoginModel.objects.filter(
            session_token=self.session_token, client_id=self.client_id, is_active=True
        ).first()

        return login_obj.user_id if login_obj else None

    def perform_tasks(self):
        default_response = {
            "result": "error",
            "authorized": False,
            "user_id": None,
            "message": "Authorization Failed",
            "session_token": self.session_token,
            "client_id": self.client_id,
        }
        user_id = self._get_user_id_from_session()
        if not user_id:
            return default_response
        default_response.update(
            {
                "result": "success",
                "authorized": True,
                "user_id": user_id,
                "message": "Successfully Authorized",
            }
        )
        return default_response
