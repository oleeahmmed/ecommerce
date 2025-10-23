from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin, TabularInline
from unfold.contrib.filters.admin import (
    RangeDateFilter,
    RangeDateTimeFilter,
    RangeNumericFilter,
    SingleNumericFilter,
    SliderNumericFilter,
)
from unfold.contrib.forms.widgets import ArrayWidget, WysiwygWidget
from unfold.decorators import display
from .models import (
    Category, Product, Cart, CartItem, Order, OrderItem, 
    Coupon, Promotion, HeroSlider, SearchQuery, StoreSettings, SpecialOffer, ContactMessage
)

# Dashboard callback function
def dashboard_callback(request, context):
    """
    Callback to prepare extra context for the dashboard template.
    """
    from django.db.models import Sum, Count, Q
    from django.utils import timezone
    from datetime import timedelta
    import json
    
    # Get statistics
    total_products = Product.objects.filter(is_active=True).count()
    total_orders = Order.objects.count()
    total_revenue = Order.objects.filter(
        status__in=['confirmed', 'shipped', 'delivered']
    ).aggregate(total=Sum('total_amount'))['total'] or 0
    
    # Recent orders (last 7 days)
    week_ago = timezone.now() - timedelta(days=7)
    recent_orders = Order.objects.filter(created_at__gte=week_ago).count()
    
    # Low stock products
    low_stock_products = Product.objects.filter(stock__lte=10, is_active=True).count()
    
    # Pending orders
    pending_orders = Order.objects.filter(status='pending').count()
    
    # Top selling products (last 30 days)
    month_ago = timezone.now() - timedelta(days=30)
    top_products = OrderItem.objects.filter(
        order__created_at__gte=month_ago,
        order__status__in=['confirmed', 'shipped', 'delivered']
    ).values('product__name').annotate(
        total_sold=Sum('quantity')
    ).order_by('-total_sold')[:5]
    
    # Recent search queries
    recent_searches = SearchQuery.objects.order_by('-last_searched')[:10]
    
    # Chart Data - Sales over last 7 days
    sales_data = []
    labels = []
    for i in range(6, -1, -1):
        date = timezone.now() - timedelta(days=i)
        day_sales = Order.objects.filter(
            created_at__date=date.date(),
            status__in=['confirmed', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        sales_data.append(float(day_sales))
        labels.append(date.strftime('%m/%d'))
    
    # Order Status Distribution
    order_status_data = []
    order_status_labels = []
    statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    status_colors = ['#f59e0b', '#3b82f6', '#8b5cf6', '#10b981', '#ef4444']
    
    for status in statuses:
        count = Order.objects.filter(status=status).count()
        if count > 0:
            order_status_data.append(count)
            order_status_labels.append(status.title())
    
    # Top Categories by Sales
    category_sales = OrderItem.objects.filter(
        order__created_at__gte=month_ago,
        order__status__in=['confirmed', 'shipped', 'delivered']
    ).values('product__category__name').annotate(
        total_sales=Sum('quantity')
    ).order_by('-total_sales')[:5]
    
    category_labels = [item['product__category__name'] or 'Uncategorized' for item in category_sales]
    category_data = [item['total_sales'] for item in category_sales]
    
    # Monthly Revenue (last 6 months)
    monthly_revenue_data = []
    monthly_labels = []
    for i in range(5, -1, -1):
        date = timezone.now() - timedelta(days=30*i)
        month_revenue = Order.objects.filter(
            created_at__month=date.month,
            created_at__year=date.year,
            status__in=['confirmed', 'shipped', 'delivered']
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        monthly_revenue_data.append(float(month_revenue))
        monthly_labels.append(date.strftime('%b %Y'))
    
    context.update({
        "total_products": total_products,
        "total_orders": total_orders,
        "total_revenue": total_revenue,
        "recent_orders": recent_orders,
        "low_stock_products": low_stock_products,
        "pending_orders": pending_orders,
        "top_products": top_products,
        "recent_searches": recent_searches,
        
        # Chart data
        "sales_chart_data": json.dumps(sales_data),
        "sales_chart_labels": json.dumps(labels),
        "order_status_data": json.dumps(order_status_data),
        "order_status_labels": json.dumps(order_status_labels),
        "category_chart_data": json.dumps(category_data),
        "category_chart_labels": json.dumps(category_labels),
        "monthly_revenue_data": json.dumps(monthly_revenue_data),
        "monthly_revenue_labels": json.dumps(monthly_labels),
    })
    return context

# Inline admins - Define these before the main admin classes that use them
class CartItemInline(TabularInline):
    model = CartItem
    extra = 0

class OrderItemInline(TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ['product', 'quantity', 'price']

@admin.register(Category)
class CategoryAdmin(ModelAdmin):
    list_display = ['name', 'slug', 'display_image', 'serial', 'is_active', 'product_count']
    list_editable = ['serial', 'is_active']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['serial', 'name']
    search_fields = ['name', 'meta_title', 'meta_description']
    list_filter = ['is_active']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'image', 'serial', 'is_active')
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )
    
    @display(description="Image", label=True)
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"
    
    @display(description="Products", label=True)
    def product_count(self, obj):
        count = obj.product_set.count()
        if count > 0:
            url = reverse('admin:ecommerce_product_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} products</a>', url, count)
        return "0 products"

@admin.register(Product)
class ProductAdmin(ModelAdmin):
    list_display = ['display_image', 'name', 'category', 'display_price', 'stock_status', 'is_active', 'created_at']
    list_filter = [
        'category', 
        'is_active', 
        ('created_at', RangeDateTimeFilter),
        'brand',
        ('stock', RangeNumericFilter),
        ('price', RangeNumericFilter),
    ]
    search_fields = ['name', 'description', 'meta_keywords', 'brand', 'slug']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['is_active']
    date_hierarchy = 'created_at'
    list_per_page = 25
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description', 'short_description', 'image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock', 'is_active')
        }),
        ('Product Details', {
            'fields': ('brand', 'model_number', 'weight', 'dimensions', 'features'),
            'classes': ('collapse',)
        }),
        ('SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        ('Social Media', {
            'fields': ('og_title', 'og_description', 'og_image'),
            'classes': ('collapse',)
        }),
    )
    
    @display(description="Image", label=True)
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 60px; object-fit: cover; border-radius: 8px;" />',
                obj.image.url
            )
        return "No image"
    
    @display(description="Price", label=True)
    def display_price(self, obj):
        if obj.is_on_sale:
            return format_html(
                '<span style="color: #ef4444; font-weight: bold;">৳{}</span><br>'
                '<span style="color: #6b7280; text-decoration: line-through; font-size: 12px;">৳{}</span>',
                obj.discount_price, obj.price
            )
        return format_html('<span style="font-weight: bold;">৳{}</span>', obj.price)
    
    @display(description="Stock", label=True)
    def stock_status(self, obj):
        if obj.stock == 0:
            return format_html('<span style="color: #ef4444; font-weight: bold;">Out of Stock</span>')
        elif obj.stock <= 10:
            return format_html('<span style="color: #f59e0b; font-weight: bold;">{} (Low)</span>', obj.stock)
        else:
            return format_html('<span style="color: #10b981; font-weight: bold;">{}</span>', obj.stock)

@admin.register(HeroSlider)
class HeroSliderAdmin(ModelAdmin):
    list_display = ['title', 'display_image', 'serial', 'is_active']
    list_editable = ['serial', 'is_active']
    ordering = ['serial']
    
    @display(description="Image", label=True)
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 80px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"

@admin.register(Promotion)
class PromotionAdmin(ModelAdmin):
    list_display = ['title', 'display_image', 'serial', 'start_date', 'end_date', 'is_active']
    list_filter = ['is_active', ('start_date', RangeDateFilter), ('end_date', RangeDateFilter)]
    list_editable = ['serial', 'is_active']
    ordering = ['serial', '-start_date']
    
    @display(description="Image", label=True)
    def display_image(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="width: 60px; height: 40px; object-fit: cover; border-radius: 4px;" />',
                obj.image.url
            )
        return "No image"

@admin.register(Coupon)
class CouponAdmin(ModelAdmin):
    list_display = ['code', 'discount_display', 'validity_period', 'usage_stats', 'is_active']
    list_filter = [
        'discount_type', 
        'is_active', 
        ('valid_from', RangeDateFilter), 
        ('valid_to', RangeDateFilter),
        ('minimum_amount', RangeNumericFilter),
    ]
    search_fields = ['code', 'description']
    list_editable = ['is_active']
    
    @display(description="Discount", label=True)
    def discount_display(self, obj):
        if obj.discount_type == 'percentage':
            return format_html('<span style="color: #10b981; font-weight: bold;">{}%</span>', obj.discount_value)
        else:
            return format_html('<span style="color: #10b981; font-weight: bold;">৳{}</span>', obj.discount_value)
    
    @display(description="Validity", label=True)
    def validity_period(self, obj):
        return format_html(
            '<small>{}<br>to<br>{}</small>',
            obj.valid_from.strftime('%d %b %Y'),
            obj.valid_to.strftime('%d %b %Y')
        )
    
    @display(description="Usage", label=True)
    def usage_stats(self, obj):
        if obj.usage_limit:
            percentage = (obj.used_count / obj.usage_limit) * 100
            color = '#ef4444' if percentage > 80 else '#f59e0b' if percentage > 50 else '#10b981'
            return format_html(
                '<span style="color: {};">{}/{}</span>',
                color, obj.used_count, obj.usage_limit
            )
        return format_html('<span>{} times</span>', obj.used_count)

@admin.register(Order)
class OrderAdmin(ModelAdmin):
    list_display = ['order_number', 'customer_info', 'total_amount', 'status_display', 'created_at']
    list_filter = [
        'status', 
        ('created_at', RangeDateTimeFilter),
        ('total_amount', RangeNumericFilter),
    ]
    search_fields = ['order_number', 'full_name', 'email', 'phone']
    readonly_fields = ['order_number', 'created_at', 'updated_at']
    date_hierarchy = 'created_at'
    inlines = [OrderItemInline]
    
    @display(description="Customer", label=True)
    def customer_info(self, obj):
        user_info = f"<strong>{obj.full_name}</strong><br>"
        if obj.user:
            user_info += f"<small>User: {obj.user.username}</small><br>"
        user_info += f"<small>{obj.email}</small>"
        return format_html(user_info)
    
    @display(description="Status", label=True)
    def status_display(self, obj):
        colors = {
            'pending': '#f59e0b',
            'confirmed': '#3b82f6',
            'shipped': '#8b5cf6',
            'delivered': '#10b981',
            'cancelled': '#ef4444',
        }
        color = colors.get(obj.status, '#6b7280')
        return format_html(
            '<span style="color: {}; font-weight: bold; text-transform: capitalize;">{}</span>',
            color, obj.status
        )

@admin.register(SearchQuery)
class SearchQueryAdmin(ModelAdmin):
    list_display = ['query', 'count', 'last_searched']
    ordering = ['-count', '-last_searched']
    readonly_fields = ['query', 'count', 'last_searched']
    list_filter = [('last_searched', RangeDateTimeFilter)]

@admin.register(SpecialOffer)
class SpecialOfferAdmin(ModelAdmin):
    list_display = ['title', 'serial', 'discount_percentage', 'is_active', 'created_at']
    list_filter = ['is_active', ('created_at', RangeDateTimeFilter)]
    list_editable = ['serial', 'is_active']
    ordering = ['serial', '-created_at']

@admin.register(StoreSettings)
class StoreSettingsAdmin(ModelAdmin):
    list_display = ['store_name', 'contact_email', 'contact_phone', 'maintenance_mode']
    
    fieldsets = (
        ('🏪 Store Information', {
            'fields': ('store_name', 'store_description', 'currency', 'currency_symbol'),
            'description': 'Basic store information and configuration'
        }),
        ('🖼️ Branding & Media', {
            'fields': ('logo', 'logo_dark', 'favicon'),
            'description': 'Upload your store logos and branding assets'
        }),
        ('📞 Contact Information', {
            'fields': ('contact_email', 'contact_phone', 'address'),
            'description': 'Store contact details and address'
        }),
        ('🌐 Social Media Links', {
            'fields': ('facebook_url', 'twitter_url', 'instagram_url', 'linkedin_url'),
            'classes': ('collapse',),
            'description': 'Social media profile links'
        }),
        ('🔍 SEO Settings', {
            'fields': ('meta_title', 'meta_description', 'meta_keywords'),
            'classes': ('collapse',),
            'description': 'Search engine optimization settings'
        }),
        ('📋 Store Policies', {
            'fields': ('shipping_policy', 'return_policy', 'privacy_policy', 'terms_conditions'),
            'classes': ('collapse',),
            'description': 'Store policies and legal information'
        }),
        ('⚙️ System Settings', {
            'fields': ('maintenance_mode',),
            'description': 'System configuration and maintenance options'
        }),
    )
    
    def has_add_permission(self, request):
        # Only allow one instance
        return not StoreSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        # Don't allow deletion
        return False
    
    def changelist_view(self, request, extra_context=None):
        # If no settings exist, redirect to add form
        if not StoreSettings.objects.exists():
            from django.shortcuts import redirect
            return redirect('admin:ecommerce_storesettings_add')
        
        # If settings exist, redirect to change form
        settings = StoreSettings.objects.first()
        from django.shortcuts import redirect
        return redirect('admin:ecommerce_storesettings_change', settings.pk)
    
    def response_change(self, request, obj):
        # After saving, stay on the same page instead of going to changelist
        from django.shortcuts import redirect
        if '_save' in request.POST:
            return redirect('admin:ecommerce_storesettings_change', obj.pk)
        return super().response_change(request, obj)

@admin.register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ['user', 'session_key', 'total_items', 'total_price', 'created_at']
    inlines = [CartItemInline]
    readonly_fields = ['total_items', 'total_price']
    list_filter = [('created_at', RangeDateTimeFilter)]

@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ['name', 'email', 'subject', 'created_at', 'is_read']
    list_filter = ['is_read', ('created_at', RangeDateTimeFilter)]
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'phone', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Contact Information', {
            'fields': ('name', 'email', 'phone', 'created_at')
        }),
        ('Message Details', {
            'fields': ('subject', 'message')
        }),
        ('Status', {
            'fields': ('is_read',)
        }),
    )