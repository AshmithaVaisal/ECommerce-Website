
from django.contrib import admin
from django.urls import path
from.import views


urlpatterns = [
    
    
    path('',views.home ,name="home"),
    path('register',views.register ,name="register"),
    path('login',views.login_page,name="login"),
    path('logout',views.logout_page,name="logout"),
    path('cart',views.cart_page,name="cart"),
    # ashmitha here made the changes get_cart_count
    # path('get_cart_count/', views.get_cart_count, name='get_cart_count'),
    # ashmitha added cart_count
    path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
    path('cart_count/', views.cart_count, name='cart_count'),
    path('get_favourite_count/', views.get_favourite_count, name='get_favourite_count'),
    path('fav',views.fav_page,name="fav"),
    path('favviewpage',views.favviewpage,name="favviewpage"),
    path('remove_cart/<str:cid>',views.remove_cart,name="remove_cart"),
    path('remove_fav/<str:fid>',views.remove_fav,name="remove_fav"),
    path('collections',views.collections ,name="collections"),
    path('collections/<str:name>',views.collectionsview ,name="collections"),
    path('collections/<str:cname>/<str:pname>/',views.product_details ,name="product_details"),
    path('addtocart',views.add_to_cart,name="addtocart"),
    # ashmitha mdae changes
    path('checkout/',views.checkout,name='checkout'),
    path(' initiate_payment/',views.initiate_payment, name='initiate_payment'),
    path('complete_payment/',views.complete_payment, name='complete_paymen'),
    path('payment-success/', views.payment_success, name='payment_success'),
    # path('payment-failure/', views.payment_failure, name='payment_failure'),

    
]
