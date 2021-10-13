from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from users import views as users_views

urlpatterns = [
    path(
        r"user/update/profile/",
        users_views.UpdateUserProfileView.as_view(),
        name="UpdateUserProfileView",
    )
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)
