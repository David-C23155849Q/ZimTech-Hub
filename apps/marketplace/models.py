"""
Marketplace models for ZimTechHub.
"""

from django.db import models
from django.conf import settings



class Product(models.Model):

    PRODUCT_TYPES = (
        ("template", "Template"),
        ("software", "Software"),
        ("course", "Course"),
        ("plugin", "Plugin"),
        ("other", "Other"),
    )


    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="marketplace_products"
    )


    title = models.CharField(
        max_length=200
    )


    description = models.TextField()


    product_type = models.CharField(
        max_length=50,
        choices=PRODUCT_TYPES,
        default="software"
    )


    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0
    )


    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True
    )


    file = models.FileField(
        upload_to="product_files/",
        blank=True,
        null=True
    )


    sales = models.PositiveIntegerField(
        default=0
    )


    rating = models.DecimalField(
        max_digits=3,
        decimal_places=2,
        default=0
    )


    is_active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    def __str__(self):

        return self.title