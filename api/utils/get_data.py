from django.conf import settings
import requests

API_BASE = settings.SMARTUP_URL

def get_data(endpoint, columns, session, parent=None, filter=None, limit=100, offset=0):
    url = f'https://{API_BASE}/b/' + endpoint

    data = {
        "p": {
            "column": columns,
            "filter": [],
            "sort": [],
            "offset": offset,
            "limit": limit
        },
    }
    
    if parent:
        data["d"] = {
            "parent_id": parent
        }
    if filter:
        for item in filter:
            data["p"]["filter"].append(item)
    header = {
        'Cookie': session,
    }
    
    response = requests.post(url=url, json=data, headers=header)
    return response.json()