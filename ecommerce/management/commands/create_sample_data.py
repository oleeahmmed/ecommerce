from django.core.management.base import BaseCommand
from ecommerce.models import SpecialOffer, Coupon, Category, HeroSlider
from django.utils import timezone
from datetime import timedelta

class Command(BaseCommand):
    help = 'Create sample data for testing'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        
        # Create sample special offers
        special_offers = [
            {
                'title': 'গ্র্যান্ড সেল',
                'subtitle': 'সমস্ত পণ্যে ৫০% পর্যন্ত ছাড়',
                'description': 'সীমিত সময়ের জন্য সকল পণ্যে বিশেষ ছাড়',
                'discount_percentage': 50,
                'background_color': 'bg-gradient-to-r from-orange-400 to-red-500',
                'button_text': 'এখনই কিনুন',
                'button_link': '/products/',
                'is_active': True,
                'serial': 1
            },
            {
                'title': 'ফ্রি ডেলিভারি',
                'subtitle': '১০০০ টাকার উপর অর্ডারে ফ্রি হোম ডেলিভারি',
                'description': 'কোন অতিরিক্ত চার্জ নেই',
                'background_color': 'bg-gradient-to-r from-purple-400 to-pink-500',
                'button_text': 'শপিং করুন',
                'button_link': '/products/',
                'is_active': True,
                'serial': 2
            },
            {
                'title': 'নতুন গ্রাহক অফার',
                'subtitle': 'প্রথম অর্ডারে ২০% অতিরিক্ত ছাড়',
                'description': 'নতুন গ্রাহকদের জন্য বিশেষ সুবিধা',
                'discount_percentage': 20,
                'background_color': 'bg-gradient-to-r from-green-400 to-blue-500',
                'button_text': 'রেজিস্টার করুন',
                'button_link': '/auth/register/',
                'is_active': True,
                'serial': 3
            }
        ]
        
        for offer_data in special_offers:
            offer, created = SpecialOffer.objects.get_or_create(
                title=offer_data['title'],
                defaults=offer_data
            )
            if created:
                self.stdout.write(f'Created special offer: {offer.title}')
            else:
                self.stdout.write(f'Special offer already exists: {offer.title}')
        
        # Create sample coupons
        coupons = [
            {
                'code': 'NEW20',
                'discount_type': 'percentage',
                'discount_value': 20,
                'minimum_amount': 500,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=30),
                'usage_limit': 100,
                'is_active': True
            },
            {
                'code': 'SAVE50',
                'discount_type': 'fixed',
                'discount_value': 50,
                'minimum_amount': 1000,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=15),
                'usage_limit': 50,
                'is_active': True
            },
            {
                'code': 'MEGA30',
                'discount_type': 'percentage',
                'discount_value': 30,
                'minimum_amount': 2000,
                'maximum_discount': 500,
                'valid_from': timezone.now(),
                'valid_to': timezone.now() + timedelta(days=45),
                'usage_limit': 200,
                'is_active': True
            }
        ]
        
        for coupon_data in coupons:
            coupon, created = Coupon.objects.get_or_create(
                code=coupon_data['code'],
                defaults=coupon_data
            )
            if created:
                self.stdout.write(f'Created coupon: {coupon.code}')
            else:
                self.stdout.write(f'Coupon already exists: {coupon.code}')
        
        # Create sample categories
        categories = [
            {'name': 'ফল ও সবজি', 'slug': 'fruits-vegetables', 'serial': 1},
            {'name': 'দুগ্ধজাত পণ্য', 'slug': 'dairy-products', 'serial': 2},
            {'name': 'মাংস ও মাছ', 'slug': 'meat-fish', 'serial': 3},
            {'name': 'চাল ও ডাল', 'slug': 'rice-lentils', 'serial': 4},
            {'name': 'তেল ও মসলা', 'slug': 'oil-spices', 'serial': 5},
            {'name': 'বেকারি আইটেম', 'slug': 'bakery-items', 'serial': 6},
        ]
        
        for cat_data in categories:
            category, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
        
        self.stdout.write(self.style.SUCCESS('Sample data created successfully!'))