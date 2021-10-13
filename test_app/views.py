from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from common.decorators import meta_data_response, session_authorize


class TestSessionAuthorizationView(APIView):
    @meta_data_response()
    @session_authorize()
    def get(self, request, *args, **kwargs):
        data = {"result": "success", "message": "Session authorization working fine"}
        return Response(data, status=status.HTTP_200_OK)
