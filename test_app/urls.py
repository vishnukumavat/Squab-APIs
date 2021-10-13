from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from test_app import views as test_app_views

urlpatterns = [
    path(
        r"test/session/",
        test_app_views.TestSessionAuthorizationView.as_view(),
        name="TestSessionAuthorization",
    )
]

urlpatterns = format_suffix_patterns(urlpatterns, suffix_required=False)
