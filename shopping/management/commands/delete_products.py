# product_management/management/commands/delete_products.py
from django.core.management.base import BaseCommand
from your_app.models import Product

class Command(BaseCommand):
    help = 'Delete products'

    def handle(self, *args, **kwargs):
        # Fetch first 50 products (you might need to adjust this query)
        products_to_delete = Product.objects.all()[:50]

        # Delete the products
        for product in products_to_delete:
            product.delete()
            self.stdout.write(self.style.SUCCESS(f'Product {product.id} deleted'))
