from django.core.management.base import BaseCommand
from django.core.files import File
from shopping.models import Product
import pandas as pd
import os

class Command(BaseCommand):
    help = 'Populate products'

    def handle(self, *args, **kwargs):
        excel_file = os.path.join(BASE_DIR, 'products', 'products.xlsx')  # Change this to your Excel file path
        df = pd.read_excel(excel_file)  # Read Excel file into a pandas DataFrame

        for index, row in df.iterrows():
            name = row['Name']
            description = row['Description']
            price = row['Price']
            image_filename = f"face_wash.webp"  # Assuming the same image for all products
            image_path = os.path.join("products", image_filename)

            if os.path.isfile(image_path):
                with open(image_path, 'rb') as f:
                    product = Product.objects.create(
                        name=name,
                        description=description,
                        image=File(f),
                        original_price=price
                    )
                    self.stdout.write(self.style.SUCCESS(f'Product {name} created with image: {image_path}'))
            else:
                product = Product.objects.create(
                    name=name,
                    description=description,
                    original_price=price
                )
                self.stdout.write(self.style.WARNING(f'Product {name} created without image: {image_path}'))
