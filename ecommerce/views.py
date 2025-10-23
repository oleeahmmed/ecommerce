from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db import models
import json
from .models import Product, Category, Cart, CartItem, Order, OrderItem, Coupon, SearchQuery, HeroSlider, Promotion, SpecialOffer
from .forms import LoginForm, OrderForm



def product_list(request):
    products = Product.objects.filter(is_active=True)
    categories = Category.objects.filter(is_active=True)
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    search_query = request.GET.get('search')
    sort_by = request.GET.get('sort')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    price_range = request.GET.get('price_range')
    in_stock = request.GET.get('in_stock')
    on_sale = request.GET.get('on_sale')
    brand = request.GET.get('brand')
    
    current_category = None
    
    # Category filter
    if category_slug:
        products = products.filter(category__slug=category_slug)
        current_category = Category.objects.filter(slug=category_slug).first()
    
    # Search filter
    if search_query:
        products = products.filter(
            models.Q(name__icontains=search_query) |
            models.Q(description__icontains=search_query) |
            models.Q(meta_keywords__icontains=search_query)
        )
        # Track search query
        SearchQuery.objects.update_or_create(
            query=search_query,
            defaults={'count': models.F('count') + 1}
        )
    
    # Price range filters
    if price_range:
        if price_range == '0-500':
            products = products.filter(price__lte=500)
        elif price_range == '500-1000':
            products = products.filter(price__gte=500, price__lte=1000)
        elif price_range == '1000-2000':
            products = products.filter(price__gte=1000, price__lte=2000)
        elif price_range == '2000+':
            products = products.filter(price__gte=2000)
    
    # Custom price range
    if min_price:
        try:
            products = products.filter(price__gte=float(min_price))
        except ValueError:
            pass
    
    if max_price:
        try:
            products = products.filter(price__lte=float(max_price))
        except ValueError:
            pass
    
    # Stock filter
    if in_stock == 'true':
        products = products.filter(stock__gt=0)
    
    # Sale filter
    if on_sale == 'true':
        products = products.filter(discount_price__isnull=False).exclude(
            discount_price__gte=models.F('price')
        )
    
    # Brand filter
    if brand:
        products = products.filter(brand__icontains=brand)
    
    # Sorting
    if sort_by:
        if sort_by == 'name':
            products = products.order_by('name')
        elif sort_by == 'price_low':
            products = products.extra(
                select={'effective_price': 'COALESCE(discount_price, price)'}
            ).order_by('effective_price')
        elif sort_by == 'price_high':
            products = products.extra(
                select={'effective_price': 'COALESCE(discount_price, price)'}
            ).order_by('-effective_price')
        elif sort_by == 'newest':
            products = products.order_by('-created_at')
        elif sort_by == 'popular':
            # Order by stock descending as a proxy for popularity
            products = products.order_by('-stock')
        elif sort_by == 'discount':
            products = products.filter(discount_price__isnull=False).extra(
                select={'discount_percent': '((price - discount_price) / price) * 100'}
            ).order_by('-discount_percent')
    else:
        # Default sorting
        products = products.order_by('-created_at')
    
    # Get unique brands for filter
    brands = Product.objects.filter(is_active=True).exclude(
        brand__isnull=True
    ).exclude(brand__exact='').values_list('brand', flat=True).distinct()
    
    # Get price range for filters
    price_stats = Product.objects.filter(is_active=True).aggregate(
        min_price=models.Min('price'),
        max_price=models.Max('price')
    )
    
    # Pagination for initial load
    products_per_page = 12
    total_products = products.count()
    initial_products = products[:products_per_page]
    has_more = total_products > products_per_page
    
    context = {
        'products': initial_products,
        'categories': categories,
        'current_category': current_category,
        'search_query': search_query,
        'has_more': has_more,
        'products_per_page': products_per_page,
        'total_products': total_products,
        'brands': brands,
        'price_stats': price_stats,
        # Current filter values for maintaining state
        'current_sort': sort_by,
        'current_price_range': price_range,
        'current_min_price': min_price,
        'current_max_price': max_price,
        'current_in_stock': in_stock,
        'current_on_sale': on_sale,
        'current_brand': brand,
    }
    return render(request, 'products/list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    context = {
        'product': product,
    }
    return render(request, 'products/detail.html', context)

def get_cart(request):
    if request.user.is_authenticated:
        cart, created = Cart.objects.get_or_create(user=request.user)
    else:
        if not request.session.session_key:
            request.session.create()
        session_key = request.session.session_key
        cart, created = Cart.objects.get_or_create(session_key=session_key)
    return cart

from django.template.loader import render_to_string

@require_POST
def add_to_cart(request):
    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))
        
        product = get_object_or_404(Product, id=product_id, is_active=True)
        cart = get_cart(request)
        
        cart_item, created = CartItem.objects.get_or_create(
            cart=cart,
            product=product,
            defaults={'quantity': quantity}
        )
        
        if not created:
            cart_item.quantity += quantity
            cart_item.save()
        
        # Get updated cart data
        cart_items_count = cart.total_items
        cart_total = cart.total_price
        
        # Render cart items HTML for sidebar
        cart_items_html = render_to_string('cart/cart_items.html', {
            'cart': cart,
            'cart_items': cart.items.select_related('product')
        })
        
        return JsonResponse({
            'success': True,
            'message': 'Product added to cart',
            'cart_items_count': cart_items_count,
            'cart_total': float(cart_total),
            'cart_items_html': cart_items_html
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@require_POST
def update_cart_item(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
        
        cart = get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        
        if quantity <= 0:
            cart_item.delete()
            item_removed = True
        else:
            cart_item.quantity = quantity
            cart_item.save()
            item_removed = False
        
        # Get updated cart data
        cart_items_count = cart.total_items
        cart_total = cart.total_price
        
        # Render cart items HTML for sidebar
        cart_items_html = render_to_string('cart/cart_items.html', {
            'cart': cart,
            'cart_items': cart.items.select_related('product')
        })
        
        return JsonResponse({
            'success': True,
            'cart_items_count': cart_items_count,
            'cart_total': float(cart_total),
            'item_total': float(cart_item.total_price) if not item_removed else 0,
            'item_removed': item_removed,
            'cart_items_html': cart_items_html
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@require_POST
def remove_from_cart(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        
        cart = get_cart(request)
        cart_item = get_object_or_404(CartItem, id=item_id, cart=cart)
        cart_item.delete()
        
        # Get updated cart data
        cart_items_count = cart.total_items
        cart_total = cart.total_price
        
        # Render cart items HTML for sidebar
        cart_items_html = render_to_string('cart/cart_items.html', {
            'cart': cart,
            'cart_items': cart.items.select_related('product')
        })
        
        return JsonResponse({
            'success': True,
            'cart_items_count': cart_items_count,
            'cart_total': float(cart_total),
            'cart_items_html': cart_items_html
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def get_cart_data(request):
    """API endpoint to get current cart data"""
    cart = get_cart(request)
    cart_items_count = cart.total_items
    cart_total = cart.total_price
    
    return JsonResponse({
        'cart_items_count': cart_items_count,
        'cart_total': float(cart_total)
    })
def cart_view(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product')
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
    }
    return render(request, 'cart/cart.html', context)

def checkout(request):
    cart = get_cart(request)
    cart_items = cart.items.select_related('product')
    
    if cart_items.count() == 0:
        messages.warning(request, 'Your cart is empty')
        return redirect('cart')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.user = request.user if request.user.is_authenticated else None
            
            # Calculate total with discount
            total_amount = cart.total_price
            coupon_code = request.POST.get('coupon_code')
            discount_amount = float(request.POST.get('discount_amount', 0))
            
            if coupon_code and discount_amount > 0:
                try:
                    coupon = Coupon.objects.get(code=coupon_code)
                    if coupon.is_valid():
                        total_amount -= discount_amount
                        coupon.used_count += 1
                        coupon.save()
                except Coupon.DoesNotExist:
                    pass
            
            order.total_amount = total_amount
            
            # Generate order number
            import uuid
            order.order_number = str(uuid.uuid4())[:20]
            
            order.save()
            
            # Create order items
            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=cart_item.product,
                    quantity=cart_item.quantity,
                    price=cart_item.product.discount_price if cart_item.product.is_on_sale else cart_item.product.price
                )
            
            # Clear cart
            cart.items.all().delete()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_number=order.order_number)
    else:
        # Pre-fill form with user data if available
        initial_data = {}
        if request.user.is_authenticated:
            initial_data = {
                'full_name': request.user.get_full_name(),
                'email': request.user.email,
            }
        form = OrderForm(initial=initial_data)
    
    context = {
        'cart': cart,
        'cart_items': cart_items,
        'form': form,
    }
    return render(request, 'checkout/checkout.html', context)

def order_confirmation(request, order_number):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, order_number=order_number, user=request.user)
    else:
        order = get_object_or_404(Order, order_number=order_number, user=None)
    context = {
        'order': order,
    }
    return render(request, 'checkout/confirmation.html', context)

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                
                # Merge anonymous cart with user cart
                session_key = request.session.session_key
                if session_key:
                    try:
                        anonymous_cart = Cart.objects.get(session_key=session_key)
                        user_cart, created = Cart.objects.get_or_create(user=user)
                        
                        for item in anonymous_cart.items.all():
                            user_item, created = CartItem.objects.get_or_create(
                                cart=user_cart,
                                product=item.product,
                                defaults={'quantity': item.quantity}
                            )
                            if not created:
                                user_item.quantity += item.quantity
                                user_item.save()
                        
                        anonymous_cart.delete()
                    except Cart.DoesNotExist:
                        pass
                
                messages.success(request, 'Logged in successfully!')
                return redirect('home')
    else:
        form = LoginForm()
    
    context = {
        'form': form,
    }
    return render(request, 'auth/login.html', context)

def quick_view(request, product_id):
    product = get_object_or_404(Product, id=product_id, is_active=True)
    
    context = {
        'product': product,
    }
    return render(request, 'products/quick_view.html', context)


# views.py - Add these imports at the top
from django.contrib.auth.forms import UserCreationForm
from .forms import LoginForm, OrderForm, UserProfileForm

# Add these views at the bottom of views.py
@login_required
def user_dashboard(request):
    # Get recent orders
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    
    context = {
        'recent_orders': recent_orders,
    }
    return render(request, 'user/dashboard.html', context)

@login_required
def user_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    context = {
        'orders': orders,
    }
    return render(request, 'user/orders.html', context)

@login_required
def user_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('user_profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'user/profile.html', context)

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully!')
            return redirect('home')
    else:
        form = UserCreationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'auth/register.html', context)

@require_POST
def track_search(request):
    """Track search queries for trending searches"""
    try:
        data = json.loads(request.body)
        query = data.get('query', '').strip()
        
        if query:
            search_obj, created = SearchQuery.objects.get_or_create(
                query=query,
                defaults={'count': 1}
            )
            if not created:
                search_obj.count += 1
                search_obj.save()
        
        return JsonResponse({'success': True})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})

@require_POST
def apply_coupon(request):
    """Apply coupon code to cart"""
    try:
        data = json.loads(request.body)
        coupon_code = data.get('coupon_code', '').strip()
        cart_total = float(data.get('cart_total', 0))
        
        if not coupon_code:
            return JsonResponse({'success': False, 'message': 'Coupon code is required'})
        
        try:
            coupon = Coupon.objects.get(code=coupon_code)
        except Coupon.DoesNotExist:
            return JsonResponse({'success': False, 'message': 'Invalid coupon code'})
        
        if not coupon.is_valid():
            return JsonResponse({'success': False, 'message': 'Coupon has expired or is not active'})
        
        if cart_total < coupon.minimum_amount:
            return JsonResponse({
                'success': False, 
                'message': f'Minimum order amount is ৳{coupon.minimum_amount}'
            })
        
        discount_amount = coupon.calculate_discount(cart_total)
        
        return JsonResponse({
            'success': True,
            'discount_amount': float(discount_amount),
            'coupon_code': coupon_code,
            'message': f'Coupon applied successfully! You saved ৳{float(discount_amount):.2f}'
        })
        
    except Exception as e:
        # Log the actual error for debugging
        import logging
        logger = logging.getLogger(__name__)
        logger.error(f"Error applying coupon: {str(e)}")
        return JsonResponse({'success': False, 'message': 'Error applying coupon. Please try again.'})

def home(request):
    categories = Category.objects.filter(is_active=True)[:10]
    featured_products = Product.objects.filter(is_active=True)[:12]
    hero_sliders = HeroSlider.objects.filter(is_active=True)
    promotions = Promotion.objects.filter(is_active=True)[:3]
    
    context = {
        'categories': categories,
        'featured_products': featured_products,
        'hero_sliders': hero_sliders,
        'promotions': promotions,
    }
    return render(request, 'home.html', context)

def about_us(request):
    """About Us page"""
    context = {
        'page_title': 'আমাদের সম্পর্কে',
    }
    return render(request, 'pages/about_us.html', context)

def contact_us(request):
    """Contact Us page"""
    if request.method == 'POST':
        # Handle contact form submission
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        # Here you can add logic to save the contact form or send email
        # For now, just show a success message
        messages.success(request, 'আপনার বার্তা সফলভাবে পাঠানো হয়েছে। আমরা শীঘ্রই আপনার সাথে যোগাযোগ করব।')
        return redirect('contact_us')
    
    context = {
        'page_title': 'যোগাযোগ',
    }
    return render(request, 'pages/contact_us.html', context)

def offers(request):
    """Offers page"""
    # Get active promotions and special offers
    promotions = Promotion.objects.filter(is_active=True)
    special_offers = SpecialOffer.objects.filter(is_active=True)
    active_coupons = Coupon.objects.filter(is_active=True)
    
    # Get discounted products
    discounted_products = Product.objects.filter(
        is_active=True,
        discount_price__isnull=False
    ).exclude(discount_price__gte=models.F('price'))[:20]
    
    context = {
        'page_title': 'অফার',
        'promotions': promotions,
        'special_offers': special_offers,
        'active_coupons': active_coupons,
        'discounted_products': discounted_products,
    }
    return render(request, 'pages/offers.html', context)

def load_more_products(request):
    """AJAX endpoint for loading more products"""
    if request.method != 'GET':
        return JsonResponse({'success': False, 'message': 'Invalid request method'})
    
    try:
        offset = int(request.GET.get('offset', 0))
        products_per_page = int(request.GET.get('per_page', 12))
        
        # Get all filter parameters
        category_slug = request.GET.get('category')
        search_query = request.GET.get('search')
        sort_by = request.GET.get('sort')
        min_price = request.GET.get('min_price')
        max_price = request.GET.get('max_price')
        price_range = request.GET.get('price_range')
        in_stock = request.GET.get('in_stock')
        on_sale = request.GET.get('on_sale')
        brand = request.GET.get('brand')
        
        products = Product.objects.filter(is_active=True)
        
        # Apply same filters as in product_list view
        if category_slug:
            products = products.filter(category__slug=category_slug)
        
        if search_query:
            products = products.filter(
                models.Q(name__icontains=search_query) |
                models.Q(description__icontains=search_query) |
                models.Q(meta_keywords__icontains=search_query)
            )
        
        # Price range filters
        if price_range:
            if price_range == '0-500':
                products = products.filter(price__lte=500)
            elif price_range == '500-1000':
                products = products.filter(price__gte=500, price__lte=1000)
            elif price_range == '1000-2000':
                products = products.filter(price__gte=1000, price__lte=2000)
            elif price_range == '2000+':
                products = products.filter(price__gte=2000)
        
        # Custom price range
        if min_price:
            try:
                products = products.filter(price__gte=float(min_price))
            except ValueError:
                pass
        
        if max_price:
            try:
                products = products.filter(price__lte=float(max_price))
            except ValueError:
                pass
        
        # Stock filter
        if in_stock == 'true':
            products = products.filter(stock__gt=0)
        
        # Sale filter
        if on_sale == 'true':
            products = products.filter(discount_price__isnull=False).exclude(
                discount_price__gte=models.F('price')
            )
        
        # Brand filter
        if brand:
            products = products.filter(brand__icontains=brand)
        
        # Sorting
        if sort_by:
            if sort_by == 'name':
                products = products.order_by('name')
            elif sort_by == 'price_low':
                products = products.extra(
                    select={'effective_price': 'COALESCE(discount_price, price)'}
                ).order_by('effective_price')
            elif sort_by == 'price_high':
                products = products.extra(
                    select={'effective_price': 'COALESCE(discount_price, price)'}
                ).order_by('-effective_price')
            elif sort_by == 'newest':
                products = products.order_by('-created_at')
            elif sort_by == 'popular':
                products = products.order_by('-stock')
            elif sort_by == 'discount':
                products = products.filter(discount_price__isnull=False).extra(
                    select={'discount_percent': '((price - discount_price) / price) * 100'}
                ).order_by('-discount_percent')
        else:
            products = products.order_by('-created_at')
        
        # Get the next batch of products
        next_products = products[offset:offset + products_per_page]
        has_more = products.count() > (offset + products_per_page)
        
        # Render the products HTML
        products_html = render_to_string('products/product_grid.html', {
            'products': next_products
        })
        
        return JsonResponse({
            'success': True,
            'products_html': products_html,
            'has_more': has_more,
            'loaded_count': len(next_products)
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

def robots_txt(request):
    """Generate robots.txt"""
    from django.http import HttpResponse
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /cart/",
        "Disallow: /checkout/",
        "Disallow: /user/",
        "Disallow: /auth/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")