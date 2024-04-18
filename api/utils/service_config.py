from api.models import ServiceConfiguration


def toggle_service(id: str) -> None:
    service = ServiceConfiguration.objects.get(id=id)

    if service.is_active:
        service.is_active = False
    else:
        service.is_active = True
    service.save()


def get_service(name: str):
    if ServiceConfiguration.objects.filter(name=name).exists():
        return ServiceConfiguration.objects.get(name=name)
    return None
