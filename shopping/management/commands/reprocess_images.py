# myapp/management/commands/reprocess_images.py

from django.core.management.base import BaseCommand
from shopping.models import Product
import base64

class Command(BaseCommand):
    help = 'Reprocesses older images and updates the image_base64 field'

    def handle(self, *args, **options):
        products = Product.objects.filter(image_base64__isnull=True)
        
        for product in products:
            try:
                with open(product.image.path, 'rb') as f:
                    encoded_image = base64.b64encode(f.read()).decode('utf-8')
                
                product.image_base64 = encoded_image
                product.save()
                
                self.stdout.write(self.style.SUCCESS(f"Reprocessed image for product: {product.name}"))
            except Exception as e:
                self.stderr.write(self.style.ERROR(f"Error processing image for product {product.name}: {e}"))
