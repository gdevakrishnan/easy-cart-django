from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register', views.register, name='register'),
    path('login', views.login_page, name='login'),
    path('logout', views.logout_page, name='logout'),
    path('collections', views.collections, name='collections'),
    path('collections/<str:name>', views.collections_view, name='collections'),
    path('collections/<str:cname>/<str:pname>', views.product_view, name='collections'),
    path('features', views.features, name='features'),
    path('addtocart', views.add_to_cart, name='addtocart'),
    path('cart', views.cart, name='cart'),
    path('cart/<str:pid>', views.delete_cart_item, name='cart')
]