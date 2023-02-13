from django.urls import path

from oauth_api.views import ConnectWithGoogleApi, GoogleLoginApi

api_urls = [
    path("oauth2/google/", GoogleLoginApi.as_view(), name="oauth2-login-google"),
    path(
        "oauth2/google/connect/", ConnectWithGoogleApi.as_view(), name="google-connect"
    ),
]
