import codecs
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from users.models import UsersModel
from django.conf import settings
from common.constants import EMAIL_TEMPLATE_LIBRARY


class SendTemplateEmail(object):
    def __init__(
        self, user_id, email_type, subject_fields_data={}, html_fields_data={}
    ):
        self.user_id = user_id
        self.email_type = email_type
        self.subject_fields_data = subject_fields_data
        self.html_fields_data = html_fields_data
        self.email_type_data = None
        self.sender_email = None
        self.receiver_email = None
        self.receiver_name = None
        self.subject = None
        self.html_str = None

    def _validate_email_fields(self):
        required_fields = self.email_type_data["template_fields"]
        received_fields = list(self.html_fields_data.keys())

        missing_fields = list(set(required_fields) - set(received_fields))
        if missing_fields:
            field_str = ", ".join(missing_fields)
            return {
                "result": "error",
                "message": f"{field_str} keys missing for HTML template",
            }
        return {"result": "success"}

    def _validate_subject_fileds(self):
        required_fields = self.email_type_data["subject_fields"]

        missing_fields = list(set(required_fields) - set(self.subject_fields_data))
        if missing_fields:
            field_str = ", ".join(missing_fields)
            return {
                "result": "error",
                "message": f"{field_str} keys missing for email subject",
            }
        return {"result": "success"}

    def _set_sender_email(self):
        self.sender_email = "{sender} <{sender_email}>".format(
            sender=self.email_type_data["sender"],
            sender_email=settings.EMAIL_CONFIG["email_id"],
        )

    def _set_user_email_and_name(self):
        users_obj = UsersModel.objects.get(id=self.user_id, is_active=True)
        self.receiver_name = (
            users_obj.first_name if users_obj.first_name else "Squab User"
        )
        if users_obj.last_name:
            self.receiver_name += users_obj.last_name
        self.receiver_name = self.receiver_name.title()
        self.receiver_email = self.email_type_data["receiver"].format(
            user_name=self.receiver_name, user_email=users_obj.email_id
        )

    def _generate_subject(self):
        self.subject = self.email_type_data["subject"].format(
            **self.subject_fields_data
        )

    def _generate_html_template(self):
        self.html_str = (
            codecs.open(self.email_type_data["template_path"], "r", "utf-8")
            .read()
            .format(**self.html_fields_data)
        )

    def _validate_and_generate_email_data(self):
        resp = self._validate_email_fields()
        if resp.get("result") == "error":
            return resp

        resp = self._validate_subject_fileds()
        if resp.get("result") == "error":
            return resp
        self._set_sender_email()
        self._set_user_email_and_name()
        self._generate_subject()
        self._generate_html_template()
        return {"result": "success"}

    def _send_template_email(self):
        try:
            smtp_con = smtplib.SMTP("smtp.gmail.com")
            smtp_con.starttls()
            smtp_con.login(
                settings.EMAIL_CONFIG["email_id"], settings.EMAIL_CONFIG["password"]
            )
            msg = MIMEMultipart()
            msg["From"] = self.sender_email
            msg["To"] = ",".join([self.receiver_email])
            msg["Subject"] = self.subject
            msg.attach(MIMEText(self.html_str, "html"))

            smtp_con.sendmail(self.sender_email, self.receiver_email, msg.as_string())
            smtp_con.quit()
            return {"result": "success", "message": "Email sent successfully"}
        except Exception as e:
            return {"result": "error", "message": f"Error : {str(e)}"}

    def _generate_and_send_email(self):
        resp = self._validate_and_generate_email_data()
        if resp.get("result") == "error":
            return resp
        return self._send_template_email()

    def perform_tasks(self):
        if EMAIL_TEMPLATE_LIBRARY.get(self.email_type):
            self.email_type_data = EMAIL_TEMPLATE_LIBRARY[self.email_type]
            return self._generate_and_send_email()
        return {
            "result": "error",
            "message": f"{self.email_type} not a registered email_type",
        }
