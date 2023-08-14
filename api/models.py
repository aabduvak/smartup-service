import uuid
from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        abstract = True

class Branch(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    smartup_id = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return f'{self.name} | {self.smartup_id}'

class Region(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    smartup_id = models.CharField(max_length=255,null=True, blank=True)
    
    def __str__(self):
        return self.name

class City(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=True, blank=True)
    smartup_id = models.CharField(max_length=255, null=True, blank=True)
    def __str__(self):
        return self.name

class District(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    name = models.CharField(max_length=255)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True, blank=True)
    smartup_id = models.CharField(max_length=255, null=True, blank=True)
    
    def __str__(self):
        return f'{self.name} | {self.city.name}'


class User(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    smartup_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, )
    phone = models.CharField(max_length=255, null=True, blank=True)
    
    address = models.CharField(max_length=255, null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.smartup_id} | {self.name}'

class Product(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    smartup_id = models.CharField(max_length=255)
    name = models.CharField(max_length=255, )
    code = models.CharField(max_length=255, )
    price = models.DecimalField(max_digits=12, decimal_places=2)
    
    def __str__(self) -> str:
        return f'{self.name} | {self.smartup_id}'

class Currency(BaseModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    
    def __str__(self) -> str:
        return self.name

class PaymentType(BaseModel):
    id = models.UUIDField(primary_key=True, unique=True, default=uuid.uuid4)
    name = models.CharField(max_length=255)
    smartup_id = models.CharField(max_length=255)
    currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, null=True)
    def __str__(self) -> str:
        return self.name

class Payment(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    smartup_id = models.CharField(max_length=255, )
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    base_amount = models.DecimalField(max_digits=12, decimal_places=2)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    date_of_payment = models.DateField(auto_now=True)
    def __str__(self) -> str:
        return 

class Deal(BaseModel):
    id = models.UUIDField(unique=True, default=uuid.uuid4, primary_key=True)
    smartup_id = models.CharField(max_length=255, )
    total = models.DecimalField(max_digits=12, decimal_places=2)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    date_of_order = models.DateField(auto_now=True)
    date_of_shipment = models.DateField(auto_now=True)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True)
    
    def __str__(self) -> str:
        return f'{self.smartup_id} | {self.customer.name}'

class OrderDetails(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='deals')
    deal = models.ForeignKey(Deal, on_delete=models.CASCADE, related_name='details')
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)

    def __str__(self) -> str:
        return f'Order for {self.quantity} {self.product.name} in Deal {self.deal.smartup_id}'