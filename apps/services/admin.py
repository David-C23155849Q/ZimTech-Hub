from django.contrib import admin
from .models import Service

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'freelancer', 'price', 'status', 'order_count', 'is_featured']
    list_filter = ['status', 'is_featured']
    search_fields = ['title', 'description', 'freelancer__username']
    prepopulated_fields = {'slug': ('title',)}
