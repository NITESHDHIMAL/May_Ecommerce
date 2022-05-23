from ctypes import addressof
from datetime import date, datetime
from email import message
import email
from email.mime import image
from pyexpat import model
from tkinter.tix import Tree
from turtle import Turtle
from unicodedata import name
from django.db import models
from django.contrib.auth.models import User

# Create your models here.



class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Brand(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)

    def __str__(self) -> str:
        return self.name

class Price(models.Model):
    PRICE_FILTER = {
        ('10 To 100','10 To 100'),
        ('100 To 1000','100 To 1000'),
        ('1000 To 10000','1000 To 10000'),
        ('10000 To 20000','10000 To 20000'),
    }
    price = models.CharField(choices=PRICE_FILTER,max_length=100)

    def __str__(self) -> str:
        return self.price


class Color(models.Model):
    name = models.CharField(max_length=200)
    color_id = models.CharField(max_length=100)
    color_class = models.CharField(max_length=100)
    color_for = models.CharField(max_length=100,default=0)

    def __str__(self) -> str:
        return self.name


class Product(models.Model):
    STOCK = ('In Stock','In Stock'),('Out of Stock','Out of Stock')
    STATUS = ('Publish','Publish'),('Draft','Draft')

    name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=300)
    image = models.ImageField(upload_to = 'product')
    price = models.IntegerField()
    discounted_price = models.IntegerField()
    description = models.TextField()

    categories = models.ForeignKey(Category,on_delete=models.CASCADE,null=True)
    brand = models.ForeignKey(Brand,on_delete=models.CASCADE)
    filter_price = models.ForeignKey(Price,on_delete=models.CASCADE,null=True)
    color = models.ForeignKey(Color,on_delete=models.CASCADE)
    stock = models.CharField(choices=STOCK,max_length=100)
    status = models.CharField(choices=STATUS,max_length=100)

    def __str__(self) -> str:
        return self.name


class Cart(models.Model):
	user = models.CharField(max_length=400)
	slug= models.CharField(max_length=400)
	items = models.ForeignKey(Product,on_delete=models.CASCADE)
	quantity = models.IntegerField(default=1)
	checkout = models.BooleanField(default= False)

	def __str__(self):
		return self.user


class Contact(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    message = models.TextField()

    def __str__(self):
        return self.name


class Hero(models.Model):
    image = models.ImageField(upload_to = 'hero')
    

class Banner(models.Model):
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to = 'banner')

    def __str__(self) -> str:
        return self.name


class Otp(models.Model):
    user = models.CharField(max_length=400)
    token = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.user


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    address = models.TextField(max_length=100)
    postcode = models.IntegerField()
    city = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.IntegerField()
    amount = models.CharField(max_length=500)
    payment_id = models.CharField(max_length=500,null=True,blank=True)
    paid = models.BooleanField(default=False,null=True)
    date = models.DateField(auto_now_add = Tree)

    def __str__(self):
        return self.user.username

class OrderItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    order = models.ForeignKey(Order,on_delete=models.CASCADE)
    product = models.CharField(max_length=200)
    image = models.ImageField(upload_to = 'product/order')
    quantity = models.CharField(max_length=20)
    price = models.CharField(max_length=50)
    total = models.CharField(max_length=1000)

    def __str__(self) -> str:
        return self.order.user.username




     































