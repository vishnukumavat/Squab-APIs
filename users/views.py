from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from . import serializers as users_serializer
from common.decorators import meta_data_response, session_authorize


class UpdateUserProfileView(APIView):
    @meta_data_response()
    @session_authorize()
    def post(self, request, *args, **kwargs):
        request_data = dict(request.data)
        serializer = users_serializer.UpdateUserProfileSerializer(data=request_data)
        if serializer.is_valid():
            user_profile_data = serializer.save()
            return Response(user_profile_data, status=status.HTTP_200_OK)
        return Response(
            {"result": "error", "message": serializer.errors},
            status=status.HTTP_400_BAD_REQUEST,
        )
