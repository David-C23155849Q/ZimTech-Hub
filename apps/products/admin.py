from django.contrib import admin
from .models import Product

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'status', 'sales_count', 'is_featured', 'created_at']
    list_filter = ['status', 'is_active', 'is_featured', 'license', 'category']
    search_fields = ['title', 'description', 'seller__username']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['status', 'is_featured']
