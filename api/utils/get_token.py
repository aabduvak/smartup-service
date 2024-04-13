import requests
from django.conf import settings

LOGIN = settings.SMARTUP_LOGIN
PASSWORD = settings.SMARTUP_PASSWORD
API_BASE = settings.SMARTUP_URL


def obtain_token():
    url = f"https://{API_BASE}/b/anor/s$logon"

    data = {"login": LOGIN, "password": PASSWORD}
    response = requests.post(url, data)

    if response.status_code == 200:
        key = "JSESSIONID"
        value = response.cookies.get(key)
        session = key + "=" + value
        return session
    return None
