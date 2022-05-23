from cgitb import lookup
from http import client
from itertools import count, product
from multiprocessing import context
from django import views
from django.conf import settings
from django.shortcuts import render,redirect
from django.views.generic import View
from .models import *
from django.contrib.auth.decorators import login_required
from cart.cart import Cart
from django.contrib.auth.models import User
from django.contrib import messages
from django.core.mail import EmailMessage
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt

import razorpay

client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID,settings.RAZORPAY_KEY_SECRECT))

# Create your views here.


class BaseView(View):
    views = {}


class HomeView(BaseView):
    def get(self,request):
        self.views['hero'] = Hero.objects.all()
        self.views['banner'] = Banner.objects.all()



        return render(request,'index.html',self.views)


class ProductView(BaseView):
    def get(self,request):
        self.views['categories'] = Category.objects.all()
        self.views['brand'] = Brand.objects.all()
        self.views['price'] = Price.objects.all()
        self.views['color'] = Color.objects.all()
 

        CATID = request.GET.get('categories')
        COLOR = request.GET.get('color')
        PRICE  = request.GET.get('price')

        if CATID:
            self.views['product'] = Product.objects.filter(categories=CATID)
        elif COLOR:
            self.views['product'] = Product.objects.filter(color=COLOR)
        elif PRICE:
            self.views['product']= Product.objects.filter(filter_price=PRICE)
        else:
            self.views['product'] = Product.objects.filter(status = 'Publish').order_by('-id')

        return render(request,'product.html',self.views)


class SearchView(BaseView):
    def get(self,request):
        self.views['categories'] = Category.objects.all()
        self.views['brand'] = Brand.objects.all()
        self.views['price'] = Price.objects.all()
        self.views['color'] = Color.objects.all()

        if request.method == 'GET':
            query = request.GET['query']

            lookups = Q(name__icontains = query) | Q(description__icontains = query)
            self.views['product'] = Product.objects.filter(lookups).distinct
        
        return render(request,'search.html',self.views)



class ProductDetailView(BaseView):
    def get(self,request,id):
        self.views['categories'] = Category.objects.all()
        self.views['brand'] = Brand.objects.all()
        self.views['price'] = Price.objects.all()
        self.views['color'] = Color.objects.all()
        self.views['product'] = Product.objects.filter(id=id).first()
        

        return render(request,'product_view.html',self.views)


@login_required(login_url="/accounts/login/")
def cart_add(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("/product/")


@login_required(login_url="/accounts/login/")
def item_clear(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.remove(product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_increment(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.add(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def item_decrement(request, id):
    cart = Cart(request)
    product = Product.objects.get(id=id)
    cart.decrement(product=product)
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_clear(request):
    cart = Cart(request)
    cart.clear()
    return redirect("cart_detail")


@login_required(login_url="/accounts/login/")
def cart_detail(request):
    return render(request, 'cart/cart_detail.html')

 
def checkout(request):
    amount = request.POST.get('5000')
    # amount_float = float(amount_str)
    # amount = int(amount_float)
    


    
    payment = client.order.create ({
        "amount": 5000, 
        "currency": "INR",
        'payment_capture': '1',
        
        })
    
    order_id = payment['id']
    context = {
        'order_id':order_id,
        'payment':payment,
    }
    
    return render(request,'check-out.html',context)


# class PlaceOrderView(BaseView):
#     def get(self,request):
#         if request.method == 'POST':
#             firstname = request.POST.get['firstname']

#             print(firstname)
        
#         return render(request,'cart/placeorder.html',self.views)

 
def placeorder(request):
    if request.method == 'POST':
        uid = request.session.get('_auth_user_id')
        user = User.objects.get(id=uid)
        cart = request.session.get('cart')
        
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        country = request.POST['country']
        address = request.POST['address']
        postcode = request.POST['postcode']
        city = request.POST['city']
        email = request.POST['email']
        phone = request.POST['phone']
        amount = request.POST['amount']

        payment = request.POST['payment']
        order_id = request.POST['order_id']

        context = {
            'order_id':order_id,
        }

        order = Order (
            user = user,
            firstname = firstname,
            lastname = lastname,
            country = country,
            address = address,
            postcode = postcode,
            city = city,
            email = email,
            phone = phone,
            payment_id = order_id,
            amount = amount,
             
        )
        order.save()
        for i in cart:
            a = (int(cart[i]['price']))
            b = cart[i]['price']
            total  = a * b
            print(total)

            item = OrderItem(
                user = user,
                order = order,
                product = cart[i]['name'],
                image = cart[i]['image'],
                quantity = cart[i]['quantity'],
                price = cart[i]['price'],
                total = total
                
            )
            item.save()
         

        return render(request,'cart/placeorder.html',context)


def your_order(request):
    uid = request.session.get('_auth_user_id')
    user = User.objects.get(id=uid)
    
    order = OrderItem.objects.filter(user = user)
    
    context = {
        'order':order
    }


    return render(request,'your_order.html',context)


@csrf_exempt
def success(request):
    if request.method == 'POST':
        a = request.POST
        order_id = ""
        for key, value in a.items():
            if key == 'razorpay_order_id':
                order_id = value
                break
        
        user = Order.objects.filter(payment_id = order_id).first()
        user.paid = True
        user.save()


    return render(request,'cart/thank-you.html')


class WishListView(BaseView):
    def get(self,request):
        return render(request,'wishlist.html',self.views)



# def cart(request,slug):
# 	if Cart.objects.filter(slug = slug,user=request.user.username,checkout = False).exists():
# 		quantity = Cart.objects.get(slug = slug,user=request.user.username,checkout = False).quantity
# 		quantity = quantity + 1
# 		Cart.objects.filter(slug = slug,user=request.user.username,checkout = False).update(quantity = quantity)
# 	else:
# 		username = request.user.username
# 		data = Cart.objects.create(
# 			user = username,
# 			slug = slug,
# 			items = Product.objects.filter(slug = slug)[0]
# 		)
# 		data.save()

# 	return redirect('/wishlist')


# def decreasecart(request,slug):
# 	if Cart.objects.filter(slug = slug,user=request.user.username,checkout = False).exists():
# 		quantity = Cart.objects.get(slug = slug,user=request.user.username,checkout = False).quantity
# 		if quantity > 1:
# 			quantity = quantity + 1
# 			Cart.objects.filter(slug = slug,user=request.user.username,checkout = False).update(quantity = quantity)
# 	return redirect('/wishlist')


# class CartView(BaseView):
# 	def get(self,request):
# 		self.views['cart_product'] = Cart.objects.filter(user=request.user.username,checkout = False)
# 		return render(request,'wishlist.html',self.views)





from django.core.mail import EmailMessage
from django.contrib.auth.models import User
from django.contrib import messages
import random

def register(request):
	if request.method == "POST":
		username = request.POST['username']
		email = request.POST['email']
		password = request.POST['password']
		confirm_password = request.POST['confirm_password']

		if password == confirm_password:
			randomlist = random.sample(range(1000, 9999), 1)

			if User.objects.filter(username = username).exists():
				messages.error(request,'The username is already taken')
				return redirect('/signup')

			elif User.objects.filter(email = email).exists():
				messages.error(request,'The email is already taken')
				return redirect('/signup')
			else:
				user = User.objects.create_user(
					username = username,
					email = email,
					password = password
					)
				user.save()
				User.objects.filter(username = username).update(is_active = False)

				code = Otp.objects.create(
					user = username,
					token = randomlist[0]
					)
				code.save()

				email = EmailMessage(
				    'Email verification code',
				    f'Please enter email verification code {randomlist[0]}',
				    'c6d2700b477494',
				    [email]
				    )
				email.send()
				messages.error(request,'The otp is sent to your email.')
				return redirect('/verify/')
		else:
			messages.error(request,'The password does not match')
			return render(request,'register.html')
	return render(request,'register.html')


def verification_code(request):
    if request.method == 'POST':
        username = request.POST['username']
        code = request.POST['code']

        if Otp.objects.filter(token=code,user=username).exists():
            User.objects.filter(username = username).update(is_active = True)
            return redirect('home')

    return render(request,'code.html')

 
def contact(request):
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        message = request.POST['message']

        data = Contact.objects.create (
            name = name,
            email = email,
            message = message
            )
        
        data.save()
        email = EmailMessage(
            'Hello',
            'Hello thanks for the messaging us. We will get follow back to you!',
            '6aab7ce21cc185',
            [email],
            )
        email.send()
        return redirect('home')
        
    return render(request,'contact.html')







