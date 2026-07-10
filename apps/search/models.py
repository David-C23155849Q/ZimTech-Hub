"""
Search models for ZimTechHub.
"""

from django.conf import settings
from django.db import models


class SearchHistory(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="search_history",
    )

    query = models.CharField(max_length=255)

    searched_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-searched_at"]

    def __str__(self):
        return f"{self.user} - {self.query}"


class TrendingSearch(models.Model):
    query = models.CharField(
        max_length=100,
        unique=True,
    )

    count = models.PositiveIntegerField(
        default=1
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-count"]

    def __str__(self):
        return self.query