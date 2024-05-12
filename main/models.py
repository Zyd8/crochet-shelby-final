from django.contrib.auth.models import AbstractUser
from django.db import models

class MyUser(AbstractUser):
    def __str__(self):
        return self.username

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('Audio', 'Audio'),
        ('Home', 'Home'),
        ('Accessories', 'Accessories'),
    )

    name = models.CharField(max_length=255)
    price = models.FloatField()
    image1 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image2 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    image3 = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField()
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)

    def __str__(self):
        return self.name

class Cart(models.Model):
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, related_name='carts', through='CartItem')

    created = models.DateField(auto_now_add=True)
    shipping_fee = models.FloatField(null=True)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return f"Cart for {self.user.username}"
    
class CartItem(models.Model):
    order = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    additional_notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Cart for {self.order.user.username}"

class Order(models.Model):
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE, related_name='orders')
    STATUS_CHOICES = (
        ('Pending', 'Pending'),
        ('Shipped', 'Shipped'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    contact_number = models.CharField(max_length=20, null=True, blank=True)
    shipping_address = models.TextField(null=False)
    created = models.DateField(auto_now_add=True)
    total_price = models.FloatField(null=True)

    def __str__(self):
        return f"Order for {self.user.username}#{self.id}: {self.status}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    additional_notes = models.TextField(null=True)

    def __str__(self):
        return f"{self.quantity} x {self.product.name} in Order for {self.order.user.username}#{self.order.id}"
