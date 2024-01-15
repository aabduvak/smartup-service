import requests
from django.conf import settings

ESKIZ_EMAIL = settings.ESKIZ_EMAIL
ESKIZ_PASSWORD = settings.ESKIZ_PASSWORD
ESKIZ_URL = settings.ESKIZ_URL

def get_token():
	url = f'http://{ESKIZ_URL}/auth/login'
	data = {
		"email": ESKIZ_EMAIL,
		"password": ESKIZ_PASSWORD
	}

	response = requests.post(url=url, data=data)
	if response.status_code == 200:
		return response.json()
	return None

# Removed from provider API
#def delete_token(token):
#	url = f'http://{ESKIZ_URL}/auth/invalidate'

#	headers = {
#		"Authorization": f"Bearer {token}"
#	}
#	response = requests.delete(url=url, headers=headers)
#	return response

def get_balance(token):
	url = f'http://{ESKIZ_URL}/user/get-limit'

	headers = {
		"Authorization": f"Bearer {token}"
	}
	response = requests.get(url=url, headers=headers)
	return response.json()

def send_message(phone, message, token):
    url = f'http://{ESKIZ_URL}/message/sms/send'

    data = {
        "mobile_phone": phone,
        "message": message,
        "from": "4546",
    }

    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.post(url=url, data=data, headers=headers)

    if response.status_code == 200:
        return response.json()
    return None