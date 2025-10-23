# insert_bangla_products.py

import os
import django
import sys

# Django setup
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from ecommerce.models import Product, Category
from django.utils.text import slugify

def create_categories():
    """Create categories if they don't exist"""
    categories_data = [
        {'name': 'বাদাম', 'slug': 'nuts'},
        {'name': 'শুকনো ফল', 'slug': 'dry-fruits'},
        {'name': 'মসলা', 'slug': 'spices'},
        {'name': 'চা ও কফি', 'slug': 'tea-coffee'},
        {'name': 'স্ন্যাকস', 'slug': 'snacks'},
    ]
    
    for cat_data in categories_data:
        category, created = Category.objects.get_or_create(
            slug=cat_data['slug'],
            defaults={
                'name': cat_data['name'],
                'serial': categories_data.index(cat_data),
                'is_active': True
            }
        )
        if created:
            print(f'Created category: {category.name}')

def insert_bangla_products():
    """Insert Bengali product data"""
    
    products_data = [
        {
            'name': 'কাজু বাদাম',
            'slug': 'cashew-nuts',
            'description': 'প্রিমিয়াম কোয়ালিটির তাজা কাজু বাদাম, স্বাস্থ্যের জন্য অত্যন্ত উপকারী। প্রোটিন, ভিটামিন এবং মিনারেলে ভরপুর।',
            'price': 1200.00,
            'discount_price': 999.00,
            'category_slug': 'nuts',
            'stock': 50,
            'short_description': 'তাজা প্রিমিয়াম কাজু বাদাম',
            'features': '১০০% অর্গানিক\nভিটামিন ই সমৃদ্ধ\nকোলেস্টেরল মুক্ত\nপ্রোটিনের ভালো উৎস',
            'brand': 'প্রিমিয়াম নাটস',
            'weight': '৫০০ গ্রাম',
        },
        {
            'name': 'কিসমিস',
            'slug': 'raisins',
            'description': 'সুগন্ধি ও মিষ্টি কিসমিস, রান্না এবং স্ন্যাকস হিসেবে ব্যবহারের জন্য উপযুক্ত। আয়রন এবং ফাইবার সমৃদ্ধ।',
            'price': 450.00,
            'discount_price': 399.00,
            'category_slug': 'dry-fruits',
            'stock': 100,
            'short_description': 'সুগন্ধি মিষ্টি কিসমিস',
            'features': 'প্রাকৃতিক মিষ্টি\nআয়রন সমৃদ্ধ\nএনার্জি বুস্টার\nকোলেস্টেরল মুক্ত',
            'brand': 'ফ্রেশ ফ্রুটস',
            'weight': '২৫০ গ্রাম',
        },
        {
            'name': 'আখরোট',
            'slug': 'walnuts',
            'description': 'তাজা আখরোট ওমেগা-৩ ফ্যাটি অ্যাসিড সমৃদ্ধ, মস্তিষ্কের স্বাস্থ্যের জন্য খুবই ভালো।',
            'price': 850.00,
            'discount_price': 749.00,
            'category_slug': 'nuts',
            'stock': 30,
            'short_description': 'ওমেগা-৩ সমৃদ্ধ আখরোট',
            'features': 'ওমেগা-৩ ফ্যাটি অ্যাসিড\nমস্তিষ্কের জন্য উপকারী\nঅ্যান্টিঅক্সিডেন্ট সমৃদ্ধ\nহার্টের জন্য ভালো',
            'brand': 'হেলথি নাটস',
            'weight': '২৫০ গ্রাম',
        },
        {
            'name': 'বাদাম',
            'slug': 'almonds',
            'description': 'ক্যালিফোর্নিয়ান বাদাম, ভিটামিন ই এবং প্রোটিনে ভরপুর। স্বাস্থ্যকর স্ন্যাকিং এর জন্য আদর্শ।',
            'price': 950.00,
            'discount_price': 799.00,
            'category_slug': 'nuts',
            'stock': 75,
            'short_description': 'ক্যালিফোর্নিয়ান বাদাম',
            'features': 'ভিটামিন ই সমৃদ্ধ\nত্বকের জন্য ভালো\nপ্রোটিনের উৎস\nকোলেস্টেরল মুক্ত',
            'brand': 'ক্যালিফোর্নিয়া নাটস',
            'weight': '৫০০ গ্রাম',
        },
        {
            'name': 'পেস্তা বাদাম',
            'slug': 'pista-nuts',
            'description': 'উচ্চমানের পেস্তা বাদাম, ফাইবার এবং প্রোটিন সমৃদ্ধ। স্বাদে এবং পুষ্টিতে অতুলনীয়।',
            'price': 1500.00,
            'discount_price': 1299.00,
            'category_slug': 'nuts',
            'stock': 25,
            'short_description': 'উচ্চমানের পেস্তা বাদাম',
            'features': 'ফাইবার সমৃদ্ধ\nপ্রোটিনের ভালো উৎস\nহার্টের জন্য উপকারী\nঅ্যান্টিঅক্সিডেন্ট',
            'brand': 'প্রিমিয়াম নাটস',
            'weight': '২৫০ গ্রাম',
        },
        {
            'name': 'খেজুর',
            'slug': 'dates',
            'description': 'তাজা মিষ্টি খেজুর, প্রাকৃতিক শক্তির উৎস। আয়রন এবং ফাইবারে ভরপুর।',
            'price': 600.00,
            'discount_price': 499.00,
            'category_slug': 'dry-fruits',
            'stock': 60,
            'short_description': 'তাজা মিষ্টি খেজুর',
            'features': 'প্রাকৃতিক শক্তির উৎস\nআয়রন সমৃদ্ধ\nফাইবারে ভরপুর\nকোলেস্টেরল মুক্ত',
            'brand': 'ডেটস কিংডম',
            'weight': '৫০০ গ্রাম',
        },
        {
            'name': 'চিনা বাদাম',
            'slug': 'peanuts',
            'description': 'তাজা ভাজা চিনা বাদাম, প্রোটিন এবং স্বাস্থ্যকর ফ্যাট সমৃদ্ধ। স্ন্যাকস হিসেবে জনপ্রিয়।',
            'price': 300.00,
            'discount_price': 249.00,
            'category_slug': 'nuts',
            'stock': 120,
            'short_description': 'তাজা ভাজা চিনা বাদাম',
            'features': 'প্রোটিন সমৃদ্ধ\nসস্তায় পুষ্টি\nএনার্জি বুস্টার\nস্ন্যাকস হিসেবে আদর্শ',
            'brand': 'লোকাল ফার্মস',
            'weight': '৫০০ গ্রাম',
        },
        {
            'name': 'হলুদ গুঁড়া',
            'slug': 'turmeric-powder',
            'description': 'শুদ্ধ হলুদ গুঁড়া, রান্না এবং আয়ুর্বেদিক ঔষধি হিসেবে ব্যবহার্য। অ্যান্টি-ইনফ্লেমেটরি গুণাবলী সম্পন্ন।',
            'price': 200.00,
            'discount_price': 179.00,
            'category_slug': 'spices',
            'stock': 80,
            'short_description': 'শুদ্ধ হলুদ গুঁড়া',
            'features': 'অ্যান্টি-ইনফ্লেমেটরি\nপ্রাকৃতিক অ্যান্টিসেপটিক\nহজমে সাহায্যকারী\n১০০% শুদ্ধ',
            'brand': 'পুরান ঢাকা মসলা',
            'weight': '১০০ গ্রাম',
        },
        {
            'name': 'দারচিনি',
            'slug': 'cinnamon',
            'description': 'উচ্চমানের দারচিনি, সুগন্ধি এবং ঔষধি গুণাবলী সম্পন্ন। ব্লাড সুগার নিয়ন্ত্রণে সহায়ক।',
            'price': 180.00,
            'discount_price': 149.00,
            'category_slug': 'spices',
            'stock': 45,
            'short_description': 'উচ্চমানের দারচিনি',
            'features': 'ব্লাড সুগার কন্ট্রোল\nঅ্যান্টিঅক্সিডেন্ট সমৃদ্ধ\nসুগন্ধি\nপ্রাকৃতিক প্রিজারভেটিভ',
            'brand': 'স্পাইস কিং',
            'weight': '৫০ গ্রাম',
        },
        {
            'name': 'গ্রিন টি',
            'slug': 'green-tea',
            'description': 'প্রিমিয়াম কোয়ালিটি গ্রিন টি, মেটাবলিজম বুস্টার এবং ওজন কমানোর জন্য কার্যকরী।',
            'price': 350.00,
            'discount_price': 299.00,
            'category_slug': 'tea-coffee',
            'stock': 90,
            'short_description': 'প্রিমিয়াম গ্রিন টি',
            'features': 'মেটাবলিজম বুস্টার\nঅ্যান্টিঅক্সিডেন্ট সমৃদ্ধ\nওজন কন্ট্রোল\nএনার্জি বুস্টার',
            'brand': 'টি গার্ডেন',
            'weight': '১০০ গ্রাম',
        }
    ]

    created_count = 0
    updated_count = 0

    for product_data in products_data:
        try:
            category = Category.objects.get(slug=product_data['category_slug'])
            
            # Remove category_slug from product data
            category_slug = product_data.pop('category_slug')
            
            product, created = Product.objects.update_or_create(
                slug=product_data['slug'],
                defaults={
                    **product_data,
                    'category': category,
                    'is_active': True
                }
            )
            
            if created:
                print(f'✅ Created: {product.name}')
                created_count += 1
            else:
                print(f'🔄 Updated: {product.name}')
                updated_count += 1
                
        except Category.DoesNotExist:
            print(f'❌ Category not found: {product_data["category_slug"]}')
        except Exception as e:
            print(f'❌ Error inserting {product_data["name"]}: {str(e)}')

    print(f'\n🎉 Data insertion completed!')
    print(f'📦 Created: {created_count} products')
    print(f'✏️ Updated: {updated_count} products')

if __name__ == '__main__':
    print('🚀 Starting Bengali product data insertion...\n')
    
    # First create categories
    print('📁 Creating categories...')
    create_categories()
    
    print('\n📦 Inserting products...')
    insert_bangla_products()
    
    print('\n✅ All done!')