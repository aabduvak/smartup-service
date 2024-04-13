from api.models import Product, Brand

from .get_data import get_data, get_json_data


def create_brands():
    columns = ["producer_id", "name", "region_name"]
    response = get_data("/b/anor/mr/producer_list+x&table", columns=columns)

    if response["count"] <= 0:
        return None

    brands = response["data"]
    for brand in brands:
        if not Brand.objects.filter(smartup_id=brand[0]).exists():
            Brand.objects.create(
                smartup_id=brand[0],
                name=brand[1],
            )
    return True


def create_product(code: str):
    columns = ["product_id", "code", "name", "ikpu", "barcodes", "producer_name"]

    filter = ["search_code", "search", f"%{code}%"]

    response = get_data("/b/ref/product_list+x&table", columns=columns, filter=filter)

    if response["count"] <= 0:
        return None

    data = response["data"][0]
    if Product.objects.filter(code=data[1]).exists():
        return Product.objects.get(code=data["code"])

    product = Product.objects.create(
        code=data[1],
        smartup_id=data[0],
        name=data[2],
        barcode=data[4],
        fiskal_code=data[3],
    )

    if not Brand.objects.filter(name=data[5]).exists():
        create_brands()

    if Brand.objects.filter(name=data[5]).exists():
        brand = Brand.objects.get(name=data[5])
        product.brand = brand

    product.save()
    return product


def create_products(branch):
    products = get_json_data(endpoint="/b/es/porting+exp$se_product", branch=branch)

    if not products:
        return None
    try:
        for product in products:
            if Product.objects.filter(code=product["code"]).exists():
                continue

            new_product = Product.objects.create(
                code=product["code"],
                smartup_id=product["product_id"],
                name=product["name"],
            )

            if product["ikpu"] != "":
                new_product.fiskal_code = product["ikpu"]

            if len(product["barcodes"]) >= 1:
                new_product.barcode = product["barcodes"][0]

            if not Brand.objects.filter(name=product["producer_name"]).exists():
                create_brands()

            if Brand.objects.filter(name=product["producer_name"]).exists():
                brand = Brand.objects.get(name=product["producer_name"])
                new_product.brand = brand
            new_product.save()

        return True
    except:
        return None
