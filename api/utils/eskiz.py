import requests
from django.conf import settings

ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL
ESKIZ_DEFAULT_NICK = settings.ESKIZ_DEFAULT_NICK


def get_token():
    url = f"http://{ESKIZ_URL}/auth/login"
    data = {"email": ESKIZ_EMAIL, "password": ESKIZ_PASSWORD}

    response = requests.post(url=url, data=data)
    if response.status_code == 200:
        return response.json()
    return None


# Removed from provider API
# def delete_token(token):
# 	url = f'http://{ESKIZ_URL}/auth/invalidate'

# 	headers = {
# 		"Authorization": f"Bearer {token}"
# 	}
# 	response = requests.delete(url=url, headers=headers)
# 	return response


def get_balance(token: str):
    url = f"http://{ESKIZ_URL}/user/get-limit"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url=url, headers=headers)
    return response.json()


def get_nickname(token: str) -> str:
    url = f"http://{ESKIZ_URL}/nick/me"

    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url=url, headers=headers)

    if response.status_code == 200:
        nick_list = response.json()
        if len(nick_list) == 0:
            return ESKIZ_DEFAULT_NICK
        return response.json()[0]
    return ESKIZ_DEFAULT_NICK


def send_message(phone: str, message: str, token: str, nick: str):
    url = f"http://{ESKIZ_URL}/message/sms/send"

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
