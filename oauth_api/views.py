from urllib.parse import urlencode

from django.contrib.auth import login
from django.shortcuts import redirect
from django.urls import reverse
from rest_framework.generics import GenericAPIView, RetrieveAPIView

from contacts import settings
from oauth_api.serializers import InputSerializer
from oauth_api.utils import (google_get_access_token, google_get_user_info,
                             user_get_or_create)

GOOGLE_OAUTH2 = "https://accounts.google.com/o/oauth2/v2/auth?response_type=code \
&client_id={}&redirect_uri={}&prompt=select_account&access_type=offline \
&scope=https://www.googleapis.com/auth/userinfo.email https://www.googleapis.com/auth/userinfo.profile"


class GoogleLoginApi(RetrieveAPIView):
    serializer_class = InputSerializer

    def get(self, request, *args, **kwargs):
        input_serializer = self.get_serializer(data=request.GET)
        input_serializer.is_valid(raise_exception=True)

        validated_data = input_serializer.validated_data

        code = validated_data.get("code")
        error = validated_data.get("error")

        if error or not code:
            params = urlencode({"error": error})
            return redirect(f"{reverse('login')}?{params}")

        redirect_uri = request.build_absolute_uri(reverse("oauth2-login-google"))
        access_token = google_get_access_token(code=code, redirect_uri=redirect_uri)

        user_data = google_get_user_info(access_token=access_token)

        profile_data = {
            "email": user_data["email"],
            "first_name": user_data.get("given_name", ""),
            "last_name": user_data.get("family_name", ""),
        }

        user, _ = user_get_or_create(**profile_data)

        login(request, user)

        return redirect(reverse("contact-list"))


class ConnectWithGoogleApi(GenericAPIView):
    def get(self, request, *args, **kwargs):
        redirect_uri = request.build_absolute_uri(reverse("oauth2-login-google"))
        return redirect(
            GOOGLE_OAUTH2.format(settings.GOOGLE_OAUTH2_CLIENT_ID, redirect_uri)
        )
