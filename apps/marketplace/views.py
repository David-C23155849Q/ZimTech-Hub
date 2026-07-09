"""
Marketplace web views.
"""
from django.views.generic import ListView
from apps.products.models import Product


class ProductListView(ListView):
    model = Product
    template_name = "marketplace/product_list.html"
    context_object_name = "products"
    paginate_by = 20
    
    def get_queryset(self):
        return Product.objects.filter(status="active", is_active=True).select_related("seller", "category")