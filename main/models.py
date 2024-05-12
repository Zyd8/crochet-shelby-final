from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):

    def __str__(self):
        return self.username

class Product(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()

    def __str__(self):
        return self.name
    
class Cart(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='carts')
    products = models.ManyToManyField(Product, related_name='carts', through='CartItem')

    created = models.DateField(auto_now_add=True)
    shipping_fee = models.FloatField()
    total_price = models.FloatField()
    shipping_address = models.TextField(null=True)

    def __str__(self):
        return f"Order #{self.id}: {self.status}"

class CartItem(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order #{self.order.id}"
    
class Order(models.Model):
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='orders')

