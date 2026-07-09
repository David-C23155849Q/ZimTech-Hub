"""
Reviews models for ZimTechHub.
"""

from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator



class Review(models.Model):

    developer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="received_reviews"
    )


    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="given_reviews"
    )


    rating = models.PositiveIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )


    comment = models.TextField(
        blank=True
    )


    is_verified = models.BooleanField(
        default=False
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


        unique_together = [
            "developer",
            "reviewer"
        ]



    def __str__(self):

        return f"{self.reviewer} → {self.developer} ({self.rating}/5)"