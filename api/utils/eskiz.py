import requests
from datetime import datetime, timedelta
from django.utils import timezone
from django.conf import settings

from api.utils.telegram import send_telegram_message
from api.models import EskizServiceConfig

ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL
ESKIZ_DEFAULT_NICK = settings.ESKIZ_DEFAULT_NICK


def _create_token() -> str:
    url = f"https://{ESKIZ_URL}/auth/login"
    data = {"email": ESKIZ_EMAIL, "password": ESKIZ_PASSWORD}

    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        return response.json()["data"]["token"]

    send_telegram_message(f"❌ Error while creating token:\n{response.text}")
    raise NotImplementedError(response.text)


def _refresh_token(token: str) -> str:
    url = f"https://{ESKIZ_URL}/auth/refresh"
    headers = {"Authorization": f"Bearer {token}"}

    response = requests.patch(url=url, headers=headers)
    if response.status_code == 200:
        return response.json()["data"]["token"]

    send_telegram_message(f"❌ Error while refreshing token:\n{response.text}")
    raise NotImplementedError(response.text)


def get_token() -> str:
    eskiz = EskizServiceConfig.objects.first()
    now = timezone.now()

    if not eskiz or not eskiz.token:
        eskiz = EskizServiceConfig.objects.create(
            token=_create_token(), expires_at=now + timedelta(days=29)
        )

    if eskiz.expires_at <= now:
        token = _refresh_token(eskiz.token)
        eskiz.refresh_token(token)

    return eskiz.token


def get_balance(token: str):
    url = f"https://{ESKIZ_URL}/user/get-limit"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url=url, headers=headers)
    return response.json()


def get_nickname(token: str) -> str:
    url = f"https://{ESKIZ_URL}/nick/me"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        nick_list = response.json()
        if len(nick_list) == 0:
            return ESKIZ_DEFAULT_NICK
        return response.json()[0]
    return ESKIZ_DEFAULT_NICK


def send_message(phone: str, message: str, token: str, nick: str):
    url = f"https://{ESKIZ_URL}/message/sms/send"

    data = {
        "mobile_phone": phone,
        "message": message,
        "from": nick,
    }

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.post(url=url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None
