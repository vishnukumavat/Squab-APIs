from functools import wraps
from .response import MetaDataResponse
from authentication.serializers import AuthenticationSerializer
from rest_framework import status
from rest_framework.response import Response


def meta_data_response(meta=""):
    def deco(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            vanilla_response = f(*args, **kwargs)
            return MetaDataResponse(
                vanilla_response.data, meta, status=vanilla_response.status_code
            )

        return decorated_function

    return deco


def session_authorize(*args, **kwargs):
    def deco(f):
        def abstract_client_id(request):
            client_id_header_key = "HTTP_CLIENT_ID"
            return request.META.get(client_id_header_key)

        def abstract_session_token(request):
            session_token_header_key = "HTTP_SESSION_TOKEN"
            return request.META.get(session_token_header_key)

        @wraps(f)
        def decorated_function(*args, **kwargs):
            request = args[1]
            authentication_data = {
                "client_id": abstract_client_id(request),
                "session_token": abstract_session_token(request),
            }
            auth_serializer = AuthenticationSerializer(data=authentication_data)
            if auth_serializer.is_valid():
                verified_session_data = auth_serializer.verify_session()
                if verified_session_data["authorized"]:
                    request.data.update(verified_session_data)
                    return f(*args, **kwargs)
                return Response({}, status.HTTP_401_UNAUTHORIZED)
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        return decorated_function

    return deco
