import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import get_user_model

User = get_user_model()

GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

@csrf_exempt
def google_login(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid request method"}, status=400)

    import json
    try:
        data = json.loads(request.body)
        token = data.get("token")
        if not token:
            return JsonResponse({"error": "Missing token"}, status=400)
    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=400)

    # Verify token with Google
    response = requests.get(GOOGLE_TOKEN_INFO_URL, params={"id_token": token})

    if response.status_code != 200:
        return JsonResponse({
            "error": "Invalid token",
            "details": response.json()
        }, status=400)

    user_info = response.json()
    email = user_info.get("email")
    name = user_info.get("name", "")
    picture = user_info.get("picture", "")

    # Get or create user
    user, _ = User.objects.get_or_create(email=email, defaults={"username": name})

    return JsonResponse({
        "message": "Login successful",
        "user": {
            "email": email,
            "name": name,
            "picture": picture
        }
    })
