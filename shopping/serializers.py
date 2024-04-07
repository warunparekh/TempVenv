from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'image', 'original_price', 'discount_data')

    # Optionally, customize field representation (e.g., calculate discounted price)
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['discounted_price'] = instance.original_price * (1 - instance.discount_data)
        return representation

