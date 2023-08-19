from api.models import Region, City, District
from .get_data import get_data

def create_regions():
    columns = [
        "region_id",
        "name",
        "lat_lng"
    ]
    
    response = get_data(endpoint='/b/anor/mr/region_list+x&table', columns=columns)
    if response['count'] <= 0:
        return None
    
    regions = response['data']
    try:    
        for region in regions:
            if not Region.objects.filter(smartup_id=region[0]).exists():
                Region.objects.create(
                    smartup_id=region[0],
                    name=region[1],
                )
        return True
    except:
        return None

def create_cities():
    regions = Region.objects.all()
        
    for region in regions:
        columns = [
            "region_id",
            "name",
            "lat_lng"
        ]
        
        response = get_data(endpoint='/b/anor/mr/region_list+cities&table', columns=columns, parent=region.smartup_id)
        if response['count'] <= 0:
            return None
        cities = response['data']
    
        try:    
            for city in cities:
                if not City.objects.filter(smartup_id=city[0]).exists():
                    City.objects.create(
                        smartup_id=city[0],
                        name=city[1],
                        region=region
                    )
            return True
        except:
            return None

def create_districts():
    cities = City.objects.all()
        
    for city in cities:
        columns = [
            "region_id",
            "name",
            "lat_lng"
        ]
        
        response = get_data(endpoint='/b/anor/mr/region_list+towns&table', columns=columns, parent=city.smartup_id)
        if response['count'] <= 0:
            return None
        
        towns = response['data']
        
        try:    
            for town in towns:
                if not District.objects.filter(smartup_id=town[0]).exists():
                    District.objects.create(
                        smartup_id=town[0],
                        name=town[1],
                        city=city
                    )
            return True
        except:
            return None

def create_places():
    if not create_regions():
        return False
    if not create_cities():
        return False
    if not create_districts():
        return False
    return True