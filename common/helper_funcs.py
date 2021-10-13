from django.utils.crypto import get_random_string


def get_client_ip_from_request(request):
    x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
    if x_forwarded_for:
        ip = x_forwarded_for.split(",")[0]
    else:
        ip = request.META.get("REMOTE_ADDR")
    return ip


def generate_session_token(client_id):
    return f"squab${str(client_id)}${get_random_string(64)}"
