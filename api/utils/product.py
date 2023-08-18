from api.models import Product, Brand

from .get_data import get_data

def create_brands():
    columns = ["producer_id","name","region_name"]
    response = get_data('/b/anor/mr/producer_list+x&table', columns=columns)
   
    if response['count'] <= 0:
        return None
    
    brands = response['data']
    for brand in brands:
        if not Brand.objects.filter(smartup_id=brand[0]).exists():
            Brand.objects.create(
                smartup_id = brand[0],
                name = brand[1],
            )
    return True
    

def create_product(code: str):    
    columns = [
        "product_id",
        "code",
        "name",
        "ikpu",
        "barcodes",
        "producer_name"
    ]
    
    filter = [
        "search_code",
        "search",
        f"%{code}%"
    ]
  
    response = get_data('/b/ref/product_list+x&table', columns=columns, filter=filter)
    
    if response['count'] <= 0:
        return None
    
    data = response['data'][0]
    if Product.objects.filter(code=data[1]).exists():
        return Product.objects.get(code=data['code'])
    
    product = Product.objects.create(
        code = data[1],
        smartup_id = data[0],
        name = data[2],
        barcode = data[4],
        fiskal_code = data[3],
    )
    
    if not Brand.objects.filter(name=data[5]).exists():
        create_brands()
    
    if Brand.objects.filter(name=data[5]).exists():
        brand = Brand.objects.get(name=data[5])
        product.brand = brand
    
    product.save()    
    return product
    