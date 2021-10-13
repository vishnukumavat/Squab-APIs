EMAIL_TEMPLATE_LIBRARY = {
    "email_verification": {
        "sender": "Squab Signup",
        "receiver": "{user_name} <{user_email}>",
        "subject": "Hi {user_name}, Please Verify Your Email",
        "subject_fields": ["user_name"],
        "template_path": "common/templates/email_verification.html",
        "template_fields": ["otp", "user_name"],
    },
    "forgot_password": {
        "sender": "Squab Support",
        "receiver": "{user_name} <{user_email}>",
        "subject": "{user_name} Recover Your Squab Password",
        "subject_fields": ["user_name"],
        "template_path": "common/templates/forgot_password.html",
        "template_fields": ["otp", "user_name"],
    },
}
