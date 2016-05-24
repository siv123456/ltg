from rest_framework import routers
from rest_framework.urlpatterns import url, format_suffix_patterns
from .views import UsersView, RegisterView, GoogleAuthView

urlpatterns = [
    url(r'^users/$', UsersView.as_view(), name="users"),
    url(r'^register/$', RegisterView.as_view(), name="register"),
    url(r'^auth/$', GoogleAuthView.as_view(), name="auth"),
]