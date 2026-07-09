"""
Orders models for ZimTechHub.
"""

from django.db import models
from django.conf import settings
from apps.marketplace.models import Product



class Order(models.Model):

    class Status(models.TextChoices):

        PENDING = "pending", "Pending"

        COMPLETED = "completed", "Completed"

        CANCELLED = "cancelled", "Cancelled"

        REFUNDED = "refunded", "Refunded"



    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="orders"
    )


    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="orders"
    )


    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )


    currency = models.CharField(
        max_length=3,
        default="USD"
    )


    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING
    )


    transaction_id = models.CharField(
        max_length=200,
        blank=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    updated_at = models.DateTimeField(
        auto_now=True
    )


    class Meta:

        ordering = [
            "-created_at"
        ]



    def __str__(self):

        return f"{self.buyer} - {self.product}"