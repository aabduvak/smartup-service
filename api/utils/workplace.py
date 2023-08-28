from asgiref.sync import sync_to_async

from api.models import WorkPlace
from .get_data import get_data

def create_workplaces(branch_id):
    columns = [
        "room_id",
        "code",
        "name"
    ]
    
    filter = [
        "state",
        "=",
        "A"
    ]

    response = get_data(endpoint='/b/fp/room_list+x&table', columns=columns, filter=filter, branch_id=branch_id)
    if not response or response['count'] <= 0:
        return None
    
    workplaces = response['data']
    try:    
        for workplace in workplaces:
            if not WorkPlace.objects.filter(smartup_id=workplace[0]).exists():
                WorkPlace.objects.create(
                    smartup_id=workplace[0],
                    code = workplace[1],
                    name=workplace[2],
                )
        return True
    except:
        return None

def create_workplace(id, branch_id):
    
    if not id:
        return None
    
    filter =  [
        "room_id",
        "=",
        id
    ]
    
    columns = [
        "room_id",
        "code",
        "name"
    ]
    
    response = get_data(endpoint='/b/fp/room_list+x&table', columns=columns, filter=filter, branch_id=branch_id)
    if not response or response['count'] != 1:
        return None
    
    workplace = response['data'][0]

    if not WorkPlace.objects.filter(smartup_id=workplace[0]).exists():
        WorkPlace.objects.create(
            smartup_id=workplace[0],
            code = workplace[1],
            name=workplace[2]
        )
    return True

@sync_to_async
def get_workplace_list():
    workplaces = WorkPlace.objects.all()
    return workplaces

def get_disabled_workplace_list():
    return WorkPlace.objects.filter(is_active=False)

def disabled_workplace(customer):
    blacklist = get_disabled_workplace_list()
    workplaces = customer.workplaces.all()
    for workplace in workplaces:
        if workplace in blacklist:
            return True
    return False

def toggle_workplace(id):
    if not id:
        return None
    
    workplace = WorkPlace.objects.get(id=id)
    if workplace.is_active:
        workplace.is_active = False
    else:
        workplace.is_active = True
    workplace.save()
    return True