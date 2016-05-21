from rest_framework import routers
from rest_framework.urlpatterns import url, format_suffix_patterns
from .views import UsersView, RegisterView, GoogleAuthView

urlpatterns = [
    url(r'^api/v1/users/$', UsersView.as_view(), name="users"),
    url(r'^api/v1/register/$', RegisterView.as_view(), name="register"),
    url(r'', GoogleAuthView.as_view(), name="auth"),
]