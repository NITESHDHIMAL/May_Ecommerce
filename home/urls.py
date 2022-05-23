from argparse import Namespace
from django.urls import path
from .views import *
from . import views


urlpatterns = [
    path('',HomeView.as_view(),name='home'),
    path('product/',ProductView.as_view(),name='product'),
    path('product/<str:id>/',ProductDetailView.as_view(),name='product_detail'),
    path('wishlist/',WishListView.as_view(),name='wishlist'),

#     path('cart/<slug>',cart, name = 'cart'),
#     path('decreasecart/<slug>',decreasecart, name = 'decreasecart'),
#     path('wishlist/',CartView.as_view(), name = 'wishlist'),
   
    
    # user registrations
    path('register/',register,name='register'),
    path('verify/',verification_code,name='verify'),

    path('search/',SearchView.as_view(),name='search'),

    # add to cart part
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/',
         views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/',
         views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('cart/cart-detail/',views.cart_detail,name='cart_detail'),

    # path('cart/checkout/',CheckOutView.as_view(),name='checkout'),
    path('cart/checkout/',checkout,name='checkout'),
    # path('cart/checkout/placeorder',PlaceOrderView.as_view(), name='place_order'),
    path('cart/checkout/placeorder',placeorder, name='place_order'),
    path('success',success,name='success'),
    

     #contact page
    path('contact/',contact,name='contact'),

    path('your_order',your_order,name='your_order')
  



]













