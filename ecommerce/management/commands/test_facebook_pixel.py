from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Test Facebook Pixel configuration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Facebook Pixel Configuration Test ==='))
        
        # Check if Facebook Pixel ID is set
        pixel_id = getattr(settings, 'FACEBOOK_PIXEL_ID', None)
        if pixel_id:
            self.stdout.write(
                self.style.SUCCESS(f'✓ Facebook Pixel ID: {pixel_id}')
            )
        else:
            self.stdout.write(
                self.style.ERROR('✗ Facebook Pixel ID not set in settings')
            )
        
        # Check if Facebook Pixel is enabled
        pixel_enabled = getattr(settings, 'FACEBOOK_PIXEL_ENABLED', True)
        if pixel_enabled:
            self.stdout.write(
                self.style.SUCCESS('✓ Facebook Pixel is enabled')
            )
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Facebook Pixel is disabled')
            )
        
        # Check debug mode
        pixel_debug = getattr(settings, 'FACEBOOK_PIXEL_DEBUG', False)
        if pixel_debug:
            self.stdout.write(
                self.style.WARNING('⚠ Facebook Pixel debug mode is ON')
            )
        else:
            self.stdout.write(
                self.style.SUCCESS('✓ Facebook Pixel debug mode is OFF')
            )
        
        # Check context processor
        context_processors = settings.TEMPLATES[0]['OPTIONS']['context_processors']
        if 'ecommerce.context_processors.facebook_pixel' in context_processors:
            self.stdout.write(
                self.style.SUCCESS('✓ Facebook Pixel context processor is registered')
            )
        else:
            self.stdout.write(
                self.style.ERROR('✗ Facebook Pixel context processor not found')
            )
        
        self.stdout.write(self.style.SUCCESS('\n=== Configuration Summary ==='))
        self.stdout.write(f'Pixel ID: {pixel_id}')
        self.stdout.write(f'Enabled: {pixel_enabled}')
        self.stdout.write(f'Debug: {pixel_debug}')
        
        if pixel_id and pixel_enabled:
            self.stdout.write(
                self.style.SUCCESS('\n✓ Facebook Pixel is properly configured!')
            )
            self.stdout.write('You can now track the following events:')
            self.stdout.write('  • PageView (automatic)')
            self.stdout.write('  • ViewContent (product pages)')
            self.stdout.write('  • AddToCart (add to cart buttons)')
            self.stdout.write('  • InitiateCheckout (checkout page)')
            self.stdout.write('  • Purchase (order confirmation)')
            self.stdout.write('  • Search (search functionality)')
            self.stdout.write('  • Lead (contact forms, newsletter)')
        else:
            self.stdout.write(
                self.style.ERROR('\n✗ Facebook Pixel configuration incomplete')
            )