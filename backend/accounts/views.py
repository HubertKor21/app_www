from django.shortcuts import render, redirect
from django.http import JsonResponse
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from dj_rest_auth.registration.views import SocialLoginView

# Create your views here.

class GoogleLogin(SocialLoginView): # if you want to use Authorization Code Grant, use this
    adapter_class = GoogleOAuth2Adapter
    callback_url = "http://localhost:5173/"
    client_class = OAuth2Client

def email_confirmation(request, key):
    return redirect(f"http://localhost:5173/dj-rest-auth/registration/account-confirm-email/{key}")

def reset_password_confirm(request, uid, token):
    return redirect(f"http://localhost:5173/reset/password/confirm/{uid}/{token}")