# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('product/quick-view/<int:product_id>/', views.quick_view, name='quick_view'),
    
    # Cart URLs
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('cart/data/', views.get_cart_data, name='get_cart_data'),
    
    # Checkout URLs
    path('checkout/', views.checkout, name='checkout'),
    path('order/confirmation/<str:order_number>/', views.order_confirmation, name='order_confirmation'),
    
    # Auth URLs
    path('auth/login/', views.login_view, name='login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('auth/register/', views.register_view, name='register'),
    
    # User URLs
    path('user/dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user/orders/', views.user_orders, name='user_orders'),
    path('user/profile/', views.user_profile, name='user_profile'),
    
    # Additional URLs
    path('track-search/', views.track_search, name='track_search'),
    path('apply-coupon/', views.apply_coupon, name='apply_coupon'),
    path('products/load-more/', views.load_more_products, name='load_more_products'),
    
    # Static Pages
    path('about-us/', views.about_us, name='about_us'),
    path('contact-us/', views.contact_us, name='contact_us'),
    path('offers/', views.offers, name='offers'),
    path('robots.txt', views.robots_txt, name='robots_txt'),
]