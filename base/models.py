from django.db import models
from django.conf import settings
from django.contrib import admin
from uuid import uuid4


class Catagory(models.Model):
    title = models.CharField(max_length=250)
    feature_product = models.ForeignKey('Product',on_delete=models.SET_NULL,null=True,related_name='+',blank=True)
    
    def __str__(self) -> str:
        return self.title
    
    class Meta:
        ordering = ['title']

class Product(models.Model):
    title = models.CharField(max_length=250)
    slug = models.SlugField(default='-')
    description = models.TextField()
    price = models.DecimalField(max_digits=10,decimal_places=2)
    inventory = models.IntegerField()
    last_update = models.DateTimeField(auto_now=True)
    catagory = models.ForeignKey(Catagory,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return self.title
    class Meta:
        ordering = ['title']


class ProductImage(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='base/images')


class Like(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='like')
    customer = models.ForeignKey('Customer',on_delete=models.SET_NULL,related_name='+',null = True,blank= True)
    like = models.PositiveSmallIntegerField()
    date =  models.DateField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.like)

class Customer(models.Model):
    phone = models.CharField(max_length=200,null=True)
    date_of_birth = models.DateField(null=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    @admin.display(ordering='user__first_name')
    def first_name(self):
        return self.user.first_name
        
    @admin.display(ordering='user__last_name')
    def last_name(self):
        return self.user.last_name
    
    def email(self):
        return self.user.email

    def __str__(self):
        return f'{self.user.first_name} {self.user.last_name}'

    class Meta:
        ordering = ['user__first_name', 'user__last_name']
        

class Address(models.Model):
    street = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    country = models.CharField(max_length=250,null=True)
    customer = models.OneToOneField(Customer,on_delete=models.CASCADE,primary_key=True)

    def __str__(self) -> str:
        return f'{self.street}, {self.city}, {self.country}'

class Order(models.Model):
    PAYMENT_PENDING = 'P'
    PAYMENT_COMPLETE = 'C'
    PAYMENT_FAILED =  'F'

    PAYMENT_STATUS_CHOICES = [
        (PAYMENT_PENDING,'Pending'),
        (PAYMENT_COMPLETE,'Complete'),
        (PAYMENT_FAILED,'Failed')
    ]
    placed_at = models.DateTimeField(auto_now_add=True)
    payment_status = models.CharField(max_length=1, choices=PAYMENT_STATUS_CHOICES,default=PAYMENT_PENDING)
    customer = models.ForeignKey(Customer,on_delete=models.PROTECT)

    def __str__(self) -> str:
        return f'{self.customer.first_name} {self.customer.last_name}'
    

    class Meta:
        permissions = [
            ('cancel_order','Can Cancel Order')
        ]



class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT,related_name='items')
    product = models.ForeignKey(Product,on_delete=models.PROTECT,related_name='orderitem')
    quantity = models.PositiveSmallIntegerField()

    def __str__(self) -> str:
        return self.product.title

class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return str(self.id)


class CartItem(models.Model):
    cart = models.ForeignKey(Cart,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()

    class Meta:
        unique_together = [['cart','product']]



