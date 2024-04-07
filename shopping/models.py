import base64
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='products/', blank=True , default='products/face_wash.webp')  # Optional image field
    original_price = models.DecimalField(max_digits=10, decimal_places=2)
    discount_data = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)  # Discount as a decimal percentage
    image_base64 = models.TextField(blank=True, null=True)  # Field to store base64 encoded image

    def save(self, *args, **kwargs):
        if self.image: 
            self.image_base64 = base64.b64encode(self.image.file.read()).decode('utf-8')
        super().save(*args, **kwargs)
 
