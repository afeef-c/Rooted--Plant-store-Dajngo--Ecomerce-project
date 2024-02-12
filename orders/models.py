from django.db import models

from accounts.models import Account
from store.models import Product, Variation

# Create your models here.

class Payment(models.Model):
    STATUS = (
        ('Processing','Processing'),
        ('Pending','Pending'),
        ('Completed','Completed'),
        ('Cancelled','Cancelled'),

    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_id = models.CharField(max_length=100, null=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.CharField(max_length=100)
    status = models.CharField(max_length=100, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f"{self.user}-{self.payment_method}"
    
class Order(models.Model):
    
    STATUS = (
        ('Processing','Processing'),
        ('Confirmed','Confirmed'),
        ('Shipped','Shipped'),
        ('Cancelled','Cancelled'),
        ('Completed','Completed'),
        ('Delivered','Delivered')
    )

    user = models.ForeignKey(Account, on_delete=models.SET_NULL, null=True)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL,blank=True, null=True )
    order_number = models.CharField(max_length=20)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=50)
    address_line_1 = models.CharField(max_length=50)
    address_line_2 = models.CharField(max_length=50, blank=True)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    pin_code = models.CharField(max_length=15)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    tax = models.FloatField()
    shipping_fee = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Processing')
    ip = models.CharField(blank=True, max_length=20)
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    def full_address(self):

        return f"{self.address_line_1} , {self.address_line_2} "


    def __str__(self) -> str:
        return self.first_name
    
class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variations = models.ManyToManyField(Variation, blank=True)
    quantity = models.IntegerField()
    product_price = models.FloatField(null=True)
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.product.product_name
    