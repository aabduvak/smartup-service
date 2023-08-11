from django.conf import settings
import requests

API_BASE = settings.SMARTUP_URL

def get_data(endpoint: str, columns, session: str, limit=100, offset=0, **kwargs):
    url = f'https://{API_BASE}' + endpoint

    data = {
        "p": {
            "column": columns,
            "filter": [],
            "sort": [],
            "offset": offset,
            "limit": limit
        },
        "d": {}
    }
    
    if 'parent' in kwargs:
        data["d"] = {
            "parent_id": kwargs['parent']
        }
    
    if 'remove_parent' in kwargs and kwargs['remove_parent']:
        data.pop("d")
    
    if 'filter' in kwargs:
        data["p"]["filter"] = kwargs['filter']
        data["d"]["is_filial"] = "N"
    
    header = {
        'Cookie': session,
    }
    response = requests.post(url=url, json=data, headers=header)
    if response.status_code == 200:
        return response.json()
    return None

def get_xml_data():
    pass