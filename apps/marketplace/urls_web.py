"""
Marketplace web URL patterns.
"""
from django.urls import path
from . import views

app_name = "marketplace"

urlpatterns = [
    path("", views.ProductListView.as_view(), name="product-list"),
]