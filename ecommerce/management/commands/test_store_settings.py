from django.core.management.base import BaseCommand
from django.template import Context, Template
from ecommerce.context_processors import store_settings
from ecommerce.models import StoreSettings


class Command(BaseCommand):
    help = 'Test store settings integration'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('=== Store Settings Integration Test ==='))
        
        # Test context processor
        class MockRequest:
            pass
        
        request = MockRequest()
        context_data = store_settings(request)
        
        if context_data['store_settings']:
            self.stdout.write(
                self.style.SUCCESS('✓ Store settings loaded successfully')
            )
            settings = context_data['store_settings']
            self.stdout.write(f'Store Name: {settings.store_name}')
            self.stdout.write(f'Contact Email: {settings.contact_email}')
            self.stdout.write(f'Contact Phone: {settings.contact_phone}')
            self.stdout.write(f'Address: {settings.address}')
            
            if settings.logo:
                self.stdout.write(f'Logo: {settings.logo.url}')
            else:
                self.stdout.write('Logo: Not set')
                
            # Test social media links
            social_links = []
            if settings.facebook_url:
                social_links.append(f'Facebook: {settings.facebook_url}')
            if settings.twitter_url:
                social_links.append(f'Twitter: {settings.twitter_url}')
            if settings.instagram_url:
                social_links.append(f'Instagram: {settings.instagram_url}')
            if settings.linkedin_url:
                social_links.append(f'LinkedIn: {settings.linkedin_url}')
                
            if social_links:
                self.stdout.write('Social Media Links:')
                for link in social_links:
                    self.stdout.write(f'  - {link}')
            else:
                self.stdout.write('Social Media Links: None set')
                
        else:
            self.stdout.write(
                self.style.WARNING('⚠ Store settings not found or not loaded')
            )
            
            # Check if StoreSettings exists
            if StoreSettings.objects.exists():
                self.stdout.write('Store settings exist in database but context processor failed')
            else:
                self.stdout.write('No store settings found in database')
                self.stdout.write('Creating default store settings...')
                
                # Create default settings
                settings = StoreSettings.objects.create()
                self.stdout.write(
                    self.style.SUCCESS('✓ Default store settings created')
                )
        
        # Test template rendering
        self.stdout.write('\n=== Template Rendering Test ===')
        template_content = """
        Store Name: {{ store_settings.store_name|default:'Default Store' }}
        Contact Email: {{ store_settings.contact_email|default:'default@email.com' }}
        Contact Phone: {{ store_settings.contact_phone|default:'000-000-0000' }}
        """
        
        template = Template(template_content)
        context = Context(context_data)
        rendered = template.render(context)
        
        self.stdout.write('Rendered template:')
        self.stdout.write(rendered)
        
        self.stdout.write(self.style.SUCCESS('\n✓ Store settings integration test completed!'))