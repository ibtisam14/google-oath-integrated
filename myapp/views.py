import requests
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def google_login_redirect(request):
    redirect_uri = settings.GOOGLE_REDIRECT_URI
    client_id = settings.GOOGLE_CLIENT_ID
    scope = "openid email profile"
    params = {
        "response_type": "code",
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "access_type": "offline",
        "prompt": "consent",
    }
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"
    return HttpResponseRedirect(auth_url)


@csrf_exempt
def google_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to obtain access token", "details": token_json}, status=400)

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(GOOGLE_USERINFO_URL, headers=headers).json()

    return JsonResponse({
        "message": "Google login successful!",
        "user_info": userinfo,
        "token_data": token_json
    })


GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_URL = "https://api.github.com/user"


def github_login_redirect(request):
    redirect_uri = settings.GITHUB_REDIRECT_URI
    client_id = settings.GITHUB_CLIENT_ID
    scope = "read:user user:email"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }
    auth_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"
    return HttpResponseRedirect(auth_url)


@csrf_exempt
def github_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    token_data = {
        "client_id": settings.GITHUB_CLIENT_ID,
        "client_secret": settings.GITHUB_CLIENT_SECRET,
        "code": code,
        "redirect_uri": settings.GITHUB_REDIRECT_URI,
    }

    headers = {"Accept": "application/json"}
    token_response = requests.post(GITHUB_TOKEN_URL, data=token_data, headers=headers)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to obtain access token", "details": token_json}, status=400)

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(GITHUB_USERINFO_URL, headers=headers).json()

    return JsonResponse({
        "message": "GitHub login successful!",
        "user_info": userinfo,
        "token_data": token_json
    })


FACEBOOK_AUTH_URL = "https://www.facebook.com/v18.0/dialog/oauth"
FACEBOOK_TOKEN_URL = "https://graph.facebook.com/v18.0/oauth/access_token"
FACEBOOK_USERINFO_URL = "https://graph.facebook.com/me?fields=id,name,email,picture"


def facebook_login_redirect(request):
    client_id = settings.FACEBOOK_CLIENT_ID
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    scope = "email,public_profile"
    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
        "response_type": "code",
        "auth_type": "rerequest",
    }
    auth_url = f"{FACEBOOK_AUTH_URL}?{urlencode(params)}"
    return HttpResponseRedirect(auth_url)


@csrf_exempt
def facebook_callback(request):
    code = request.GET.get("code")
    if not code:
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
    params = {
        "client_id": settings.FACEBOOK_CLIENT_ID,
        "redirect_uri": settings.FACEBOOK_REDIRECT_URI,
        "client_secret": settings.FACEBOOK_CLIENT_SECRET,
        "code": code,
    }

    token_response = requests.get(token_url, params=params)
    token_json = token_response.json()
    access_token = token_json.get("access_token")

    if not access_token:
        return JsonResponse({"error": "Failed to obtain access token", "details": token_json}, status=400)

    userinfo_url = "https://graph.facebook.com/me"
    user_params = {
        "fields": "id,name,email,picture",
        "access_token": access_token,
    }

    userinfo_response = requests.get(userinfo_url, params=user_params)
    userinfo = userinfo_response.json()

    return JsonResponse({
        "message": "Facebook login successful!",
        "user_info": userinfo,
        "token_data": token_json,
    })
