from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    image = models.ImageField(upload_to='categories/', null=True, blank=True)
    serial = models.PositiveIntegerField(default=0, help_text="Display order")
    is_active = models.BooleanField(default=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (max 60 characters)")
    meta_description = models.TextField(max_length=160, blank=True, help_text="SEO description (max 160 characters)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma separated)")
    og_title = models.CharField(max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.TextField(max_length=160, blank=True, help_text="Open Graph description")
    og_image = models.ImageField(upload_to='seo/categories/', null=True, blank=True, help_text="Open Graph image (1200x630px)")
    
    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['serial', 'name']
    
    def __str__(self):
        return self.name
    
    def get_meta_title(self):
        return self.meta_title or f"{self.name} - আমার ফ্রেশ বিডি"
    
    def get_meta_description(self):
        return self.meta_description or f"{self.name} ক্যাটাগরির সেরা পণ্য কিনুন আমার ফ্রেশ বিডি থেকে। তাজা এবং মানসম্পন্ন পণ্য, দ্রুত ডেলিভারি।"
    
    def get_og_image(self):
        if self.og_image:
            return self.og_image.url
        elif self.image:
            return self.image.url
        else:
            return None

class Product(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='products/')
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=60, blank=True, help_text="SEO title (max 60 characters)")
    meta_description = models.TextField(max_length=160, blank=True, help_text="SEO description (max 160 characters)")
    meta_keywords = models.CharField(max_length=255, blank=True, help_text="SEO keywords (comma separated)")
    og_title = models.CharField(max_length=60, blank=True, help_text="Open Graph title")
    og_description = models.TextField(max_length=160, blank=True, help_text="Open Graph description")
    og_image = models.ImageField(upload_to='seo/products/', null=True, blank=True, help_text="Open Graph image (1200x630px)")
    
    # Additional SEO fields
    short_description = models.CharField(max_length=255, blank=True, help_text="Short description for listings")
    features = models.TextField(blank=True, help_text="Product features (one per line)")
    brand = models.CharField(max_length=100, blank=True)
    model_number = models.CharField(max_length=100, blank=True)
    weight = models.CharField(max_length=50, blank=True, help_text="Product weight (e.g., 1kg, 500g)")
    dimensions = models.CharField(max_length=100, blank=True, help_text="Product dimensions")
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.name
    
    @property
    def is_on_sale(self):
        return self.discount_price is not None and self.discount_price < self.price
    
    @property
    def sale_percentage(self):
        if self.is_on_sale:
            return int(((self.price - self.discount_price) / self.price) * 100)
        return 0
    
    def get_meta_title(self):
        if self.meta_title:
            return self.meta_title
        price_text = f"৳{self.discount_price}" if self.is_on_sale else f"৳{self.price}"
        return f"{self.name} - {price_text} | আমার ফ্রেশ বিডি"
    
    def get_meta_description(self):
        if self.meta_description:
            return self.meta_description
        price_text = f"মাত্র ৳{self.discount_price}" if self.is_on_sale else f"৳{self.price}"
        return f"{self.name} {price_text} দামে কিনুন আমার ফ্রেশ বিডি থেকে। {self.short_description or self.description[:100]}... দ্রুত ডেলিভারি।"
    
    def get_og_image(self):
        if self.og_image:
            return self.og_image.url
        elif self.image:
            return self.image.url
        else:
            return None
    
    def get_absolute_url(self):
        return f"/products/{self.slug}/"
    
    def get_structured_data(self):
        """Generate JSON-LD structured data for the product"""
        import json
        data = {
            "@context": "https://schema.org/",
            "@type": "Product",
            "name": self.name,
            "description": self.description,
            "image": self.get_og_image(),
            "brand": {
                "@type": "Brand",
                "name": self.brand or "আমার ফ্রেশ বিডি"
            },
            "offers": {
                "@type": "Offer",
                "price": str(self.discount_price if self.is_on_sale else self.price),
                "priceCurrency": "BDT",
                "availability": "https://schema.org/InStock" if self.stock > 0 else "https://schema.org/OutOfStock",
                "seller": {
                    "@type": "Organization",
                    "name": "আমার ফ্রেশ বিডি"
                }
            },
            "category": self.category.name,
            "sku": str(self.id),
            "url": self.get_absolute_url()
        }
        return json.dumps(data, ensure_ascii=False)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        if self.user:
            return f"Cart - {self.user.username}"
        return f"Cart - {self.session_key}"
    
    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())
    
    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1)])
    
    class Meta:
        unique_together = ['cart', 'product']
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"
    
    @property
    def total_price(self):
        if self.product.is_on_sale:
            return self.product.discount_price * self.quantity
        return self.product.price * self.quantity

class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    order_number = models.CharField(max_length=20, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Customer information
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    special_instructions = models.TextField(blank=True)
    
    def __str__(self):
        return self.order_number

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

class Coupon(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_type = models.CharField(max_length=20, choices=[
        ('percentage', 'Percentage'),
        ('fixed', 'Fixed Amount')
    ], default='percentage')
    discount_value = models.DecimalField(max_digits=10, decimal_places=2)
    minimum_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    maximum_discount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    valid_from = models.DateTimeField()
    valid_to = models.DateTimeField()
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    used_count = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.code
    
    def is_valid(self):
        now = timezone.now()
        return (self.is_active and 
                self.valid_from <= now <= self.valid_to and
                (self.usage_limit is None or self.used_count < self.usage_limit))
    
    def calculate_discount(self, amount):
        from decimal import Decimal
        
        # Convert amount to Decimal to ensure consistent types
        if isinstance(amount, (int, float)):
            amount = Decimal(str(amount))
        
        if not self.is_valid() or amount < self.minimum_amount:
            return Decimal('0')
        
        if self.discount_type == 'percentage':
            discount = amount * (self.discount_value / Decimal('100'))
            if self.maximum_discount:
                discount = min(discount, self.maximum_discount)
        else:
            discount = self.discount_value
        
        return min(discount, amount)

class Promotion(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='promotions/')
    link_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    serial = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['serial', '-start_date']
    
    def __str__(self):
        return self.title
    
    def is_valid(self):
        now = timezone.now()
        return self.is_active and self.start_date <= now <= self.end_date

class HeroSlider(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='hero_sliders/')
    button_text = models.CharField(max_length=50, default='Shop Now')
    button_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    serial = models.PositiveIntegerField(default=0)
    
    class Meta:
        ordering = ['serial']
    
    def __str__(self):
        return self.title

class SearchQuery(models.Model):
    query = models.CharField(max_length=200)
    count = models.PositiveIntegerField(default=1)
    last_searched = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-count', '-last_searched']
    
    def __str__(self):
        return f"{self.query} ({self.count})"

class SpecialOffer(models.Model):
    title = models.CharField(max_length=200)
    subtitle = models.CharField(max_length=300, blank=True)
    description = models.TextField(blank=True)
    discount_percentage = models.PositiveIntegerField(null=True, blank=True)
    background_color = models.CharField(max_length=50, default='bg-gradient-to-r from-orange-400 to-red-500')
    button_text = models.CharField(max_length=50, default='এখনই কিনুন')
    button_link = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    serial = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['serial', '-created_at']
    
    def __str__(self):
        return self.title

class StoreSettings(models.Model):
    store_name = models.CharField(max_length=200, default='🌿 আমার ফ্রেশ বিডি')
    logo = models.ImageField(upload_to='store/', null=True, blank=True)
    logo_dark = models.ImageField(upload_to='store/', null=True, blank=True)
    favicon = models.ImageField(upload_to='store/', null=True, blank=True)
    contact_email = models.EmailField(default='nabihaenterprise453@gmail.com')
    contact_phone = models.CharField(max_length=20, default='01337-343737')
    address = models.TextField(default='Bosila, Mohammadpur, Dhaka', blank=True)
    facebook_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    instagram_url = models.URLField(blank=True)
    linkedin_url = models.URLField(blank=True)
    
    # SEO Fields
    meta_title = models.CharField(max_length=200, default='আমার ফ্রেশ বিডি - Premium Quality Nuts & Dry Foods', blank=True)
    meta_description = models.TextField(default='আমার ফ্রেশ বিডি - আপনার বিশ্বস্ত প্রিমিয়াম মানের বাদাম এবং শুকনো খাবারের উৎস। তাজা, স্বাস্থ্যকর এবং পুষ্টিতে ভরপুর। Bosila, Mohammadpur, Dhaka থেকে দ্রুত ডেলিভারি।', blank=True)
    meta_keywords = models.TextField(default='আমার ফ্রেশ বিডি, বাদাম, শুকনো খাবার, স্বাস্থ্যকর খাবার, প্রিমিয়াম কোয়ালিটি, অর্গানিক, ঢাকা ডেলিভারি', blank=True)
    
    # Store Policies
    shipping_policy = models.TextField(blank=True)
    return_policy = models.TextField(blank=True)
    privacy_policy = models.TextField(blank=True)
    terms_conditions = models.TextField(blank=True)
    
    # Store Configuration
    currency = models.CharField(max_length=10, default='BDT')
    currency_symbol = models.CharField(max_length=5, default='৳')
    maintenance_mode = models.BooleanField(default=False)
    
    # Store Info
    store_description = models.TextField(
        default='Welcome to Amar Fresh ',
        blank=True
    )
    
    class Meta:
        verbose_name_plural = "Store Settings"
    
    def __str__(self):
        return self.store_name
    
    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and StoreSettings.objects.exists():
            existing = StoreSettings.objects.first()
            self.pk = existing.pk
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create store settings singleton"""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj

class ContactMessage(models.Model):
    """Model to store contact form submissions"""
    name = models.CharField(max_length=100, verbose_name='নাম')
    email = models.EmailField(verbose_name='ইমেইল')
    phone = models.CharField(max_length=20, blank=True, verbose_name='ফোন নম্বর')
    subject = models.CharField(max_length=200, verbose_name='বিষয়')
    message = models.TextField(verbose_name='বার্তা')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='তারিখ')
    is_read = models.BooleanField(default=False, verbose_name='পড়া হয়েছে')
    replied = models.BooleanField(default=False, verbose_name='উত্তর দেওয়া হয়েছে')
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'যোগাযোগ বার্তা'
        verbose_name_plural = 'যোগাযোগ বার্তা'
    
    def __str__(self):
        return f"{self.name} - {self.subject}"