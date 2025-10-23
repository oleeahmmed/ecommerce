from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.test import RequestFactory
from ecommerce.admin import dashboard_callback


class Command(BaseCommand):
    help = 'Test dashboard callback function'

    def handle(self, *args, **options):
        # Create a mock request
        factory = RequestFactory()
        request = factory.get('/admin/')
        
        # Create a mock user (admin)
        try:
            user = User.objects.filter(is_superuser=True).first()
            if not user:
                user = User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        except:
            user = None
            
        request.user = user
        
        # Test dashboard callback
        context = {}
        result = dashboard_callback(request, context)
        
        self.stdout.write(self.style.SUCCESS('Dashboard callback test results:'))
        for key, value in context.items():
            self.stdout.write(f'{key}: {value}')