import base64
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, get_object_or_404

from .models import Product  # Import your product model
from .serializers import ProductSerializer  # Import your product serializer
from django.core.paginator import Paginator

class ProductListAPIView(APIView):
    def get(self, request):
        products = Product.objects.all()  # Fetch all products
        serializer = ProductSerializer(products, many=True)  # Serialize data
        return Response(serializer.data)  # Return response with serialized data

# def product_list(request):
#     products = Product.objects.all().order_by('id')  # Fetch all products, order by ID
#     for product in products:
#         if product.discount_data:
#             discounted_price = product.original_price * (1 - product.discount_data)
#             product.discounted_price = discounted_price
#     context = {'products': products}
#     return render(request, 'shopping/product_list.html', context)

def product_list(request):
  products = Product.objects.all().order_by('id')
  for product in products:
    if product.discount_data:
      discounted_price = product.original_price * (1 - product.discount_data)
      product.discounted_price = discounted_price

  paginator = Paginator(products, 8)  # Set 8 products per page
  page_number = request.GET.get('page')  # Get current page from URL parameter
  page_obj = paginator.get_page(page_number)  # Get the requested page object

  context = {
      'products': page_obj,  # Pass paginated products for rendering
      'paginator': paginator,
  }
  return render(request, 'shopping/product_list.html', context)







def product_detail(request, product_id): # Accept 'product_id' as parameter
    product = get_object_or_404(Product, pk=product_id) # Use 'product_id' to retrieve the product
    return render(request, 'shopping/product_detail.html', {'product': product})

def reprocess_images():
    # Retrieve products with older images (where image_base64 is None or invalid)
    products = Product.objects.filter(image_base64__isnull=True)
    
    for product in products:
        try:
            # Read the original image file and encode it to base64
            with open(product.image.path, 'rb') as f:
                encoded_image = base64.b64encode(f.read()).decode('utf-8')
            
            # Update the image_base64 field for the product
            product.image_base64 = encoded_image
            product.save()
            
            print(f"Reprocessed image for product: {product.name}")
        except Exception as e:
            print(f"Error processing image for product {product.name}: {e}")

from django.shortcuts import render
from .models import Product  # Assuming you have a Product model in your shopping app

def search_products(request):
    query = request.GET.get('query', '')
    if query:
        # Filter products based on name (case-insensitive)
        filtered_products = Product.objects.filter(name__icontains=query)
    else:
        # If no query, display all products (optional)
        filtered_products = Product.objects.all()

    return render(request, 'shopping/product_list.html', {'products': filtered_products, 'query': query})

