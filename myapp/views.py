import requests
from urllib.parse import urlencode
from django.conf import settings
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt

# Google OAuth endpoints
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"
GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_USERINFO_URL = "https://www.googleapis.com/oauth2/v2/userinfo"


def google_login_redirect(request):
    """
    STEP 1: Redirect user to Google's OAuth2 consent screen.
    Added print statements to debug redirect URL issues.
    """
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

    # Properly encode parameters
    auth_url = f"{GOOGLE_AUTH_URL}?{urlencode(params)}"

    # 🧩 DEBUGGER — print everything clearly
    print("====================================")
    print("🟢 GOOGLE OAUTH DEBUG INFO")
    print("Redirect URI (in settings):", redirect_uri)
    print("Generated Auth URL:", auth_url)
    print("====================================")

    return HttpResponseRedirect(auth_url)


@csrf_exempt
def google_callback(request):
    """
    STEP 2: Handle the callback from Google.
    Exchange 'code' for access token, then retrieve user info.
    """
    code = request.GET.get("code")
    if not code:
        print("❌ Missing authorization code in callback.")
        return JsonResponse({"error": "Missing authorization code"}, status=400)

    token_data = {
        "code": code,
        "client_id": settings.GOOGLE_CLIENT_ID,
        "client_secret": settings.GOOGLE_CLIENT_SECRET,
        "redirect_uri": settings.GOOGLE_REDIRECT_URI,
        "grant_type": "authorization_code",
    }

    print("🔵 Exchanging code for token with:", GOOGLE_TOKEN_URL)
    print("Token Request Payload:", token_data)

    token_response = requests.post(GOOGLE_TOKEN_URL, data=token_data)
    token_json = token_response.json()
    print("🟡 Token Response JSON:", token_json)

    access_token = token_json.get("access_token")
    if not access_token:
        print("❌ Failed to obtain access token.")
        return JsonResponse(
            {"error": "Failed to obtain access token", "details": token_json},
            status=400
        )

    headers = {"Authorization": f"Bearer {access_token}"}
    userinfo_response = requests.get(GOOGLE_USERINFO_URL, headers=headers)
    userinfo = userinfo_response.json()

    print("🟢 User Info:", userinfo)

    return JsonResponse({
        "message": "Google login successful!",
        "user_info": userinfo,
        "token_data": token_json
    })
