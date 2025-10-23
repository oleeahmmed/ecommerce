# context_processors.py
from django.conf import settings
from .models import Cart, Category, StoreSettings, SearchQuery, Promotion, SpecialOffer, Coupon

def cart_items(request):
    cart = None
    cart_items_count = 0
    cart_total = 0
    cart_items = []
    
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        if session_key:
            cart, created = Cart.objects.get_or_create(session_key=session_key)
    
    if cart:
        cart_items_count = cart.total_items
        cart_total = cart.total_price
        cart_items = cart.items.select_related('product').all()
    
    return {
        'cart': cart,
        'cart_items_count': cart_items_count,
        'cart_total': cart_total,
        'cart_items': cart_items,
    }

def store_settings(request):
    """Add store settings to all templates"""
    try:
        from django.db import connection
        # Check if the table exists
        with connection.cursor() as cursor:
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='ecommerce_storesettings';")
            if cursor.fetchone():
                settings = StoreSettings.get_settings()
            else:
                settings = None
    except Exception as e:
        # Fallback if table doesn't exist yet or any other error
        settings = None
    
    return {
        'store_settings': settings,
    }

def categories_processor(request):
    """Add categories to all templates"""
    categories = Category.objects.filter(is_active=True)
    return {
        'categories': categories,
    }

def trending_searches(request):
    """Add trending searches to all templates"""
    trending = SearchQuery.objects.all()[:8]
    return {
        'trending_searches': trending,
    }

def promotions_processor(request):
    """Add active promotions to all templates"""
    active_promotions = Promotion.objects.filter(is_active=True)[:3]
    return {
        'active_promotions': active_promotions,
    }

def special_offers_processor(request):
    """Add special offers to all templates"""
    special_offers = SpecialOffer.objects.filter(is_active=True)[:3]
    return {
        'special_offers': special_offers,
    }

def coupons_processor(request):
    """Add active coupons to all templates"""
    active_coupons = Coupon.objects.filter(is_active=True)[:3]
    return {
        'active_coupons': active_coupons,
    }

def facebook_pixel(request):
    """Add Facebook Pixel configuration to all templates"""
    return {
        'FACEBOOK_PIXEL_ID': getattr(settings, 'FACEBOOK_PIXEL_ID', None),
        'FACEBOOK_PIXEL_ENABLED': getattr(settings, 'FACEBOOK_PIXEL_ENABLED', True),
        'FACEBOOK_PIXEL_DEBUG': getattr(settings, 'FACEBOOK_PIXEL_DEBUG', False),
    }