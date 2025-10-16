import requests
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# -------------------------------
# GOOGLE OAUTH CONFIG
# -------------------------------
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def google_login_redirect(request):
    """STEP 1: Redirect user to Google's OAuth2 consent screen."""
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

    print("====================================")
    print("🟢 GOOGLE OAUTH DEBUG INFO")
    print("Redirect URI:", redirect_uri)
    print("Generated Auth URL:", auth_url)
    print("====================================")

    return HttpResponseRedirect(auth_url)


@csrf_exempt
def google_callback(request):
    """STEP 2: Handle callback from Google."""
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
        return JsonResponse(
            {"error": "Failed to obtain access token", "details": token_json},
            status=400
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(GOOGLE_USERINFO_URL, headers=headers).json()

    print("🟢 GOOGLE USER INFO:", userinfo)

    return JsonResponse({
        "message": "Google login successful!",
        "user_info": userinfo,
        "token_data": token_json
    })


# -------------------------------
# GITHUB OAUTH CONFIG
# -------------------------------
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"
GITHUB_USERINFO_URL = "https://api.github.com/user"


def github_login_redirect(request):
    """STEP 1: Redirect user to GitHub's OAuth2 authorization screen."""
    redirect_uri = settings.GITHUB_REDIRECT_URI
    client_id = settings.GITHUB_CLIENT_ID
    scope = "read:user user:email"

    params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "scope": scope,
    }

    auth_url = f"{GITHUB_AUTH_URL}?{urlencode(params)}"

    print("====================================")
    print("🟢 GITHUB OAUTH DEBUG INFO")
    print("Redirect URI:", redirect_uri)
    print("Generated Auth URL:", auth_url)
    print("====================================")

    return HttpResponseRedirect(auth_url)


@csrf_exempt
def github_callback(request):
    """STEP 2: Handle callback from GitHub."""
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
        return JsonResponse(
            {"error": "Failed to obtain access token", "details": token_json},
            status=400
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo = requests.get(GITHUB_USERINFO_URL, headers=headers).json()

    print("🟢 GITHUB USER INFO:", userinfo)

    return JsonResponse({
        "message": "GitHub login successful!",
        "user_info": userinfo,
        "token_data": token_json
    })
