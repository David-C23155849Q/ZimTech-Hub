"""
Core models for ZimTechHub
Contains base models and shared functionality.
"""
from django.db import models
from django.conf import settings  # Use this to access AUTH_USER_MODEL
from django.utils import timezone
import uuid

# Removed: from django.contrib.auth import get_user_model
# Removed: User = get_user_model() 

class TimeStampedModel(models.Model):
    """
    Abstract base model that provides self-updating
    'created_at' and 'updated_at' fields.
    """
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class UUIDModel(models.Model):
    """
    Abstract base model that provides a UUID primary key.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    class Meta:
        abstract = True


class SoftDeleteModel(models.Model):
    """
    Abstract base model that provides soft deletion functionality.
    """
    is_deleted = models.BooleanField(default=False, db_index=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

    def soft_delete(self):
        self.is_deleted = True
        self.deleted_at = timezone.now()
        self.save(update_fields=['is_deleted', 'deleted_at'])

    def restore(self):
        self.is_deleted = False
        self.deleted_at = None
        self.save(update_fields=['is_deleted', 'deleted_at'])


class BaseModel(TimeStampedModel, UUIDModel, SoftDeleteModel):
    """
    Comprehensive base model combining timestamp, UUID, and soft delete.
    """
    class Meta:
        abstract = True


class Category(models.Model):
    """
    Global categories for products, projects, jobs, etc.
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Font awesome or similar icon class")
    color = models.CharField(max_length=7, default="#3B82F6", help_text="Hex color code")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['sort_order', 'name']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    Global tags for content categorization.
    """
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    usage_count = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['-usage_count', 'name']

    def __str__(self):
        return self.name


class SiteSettings(models.Model):
    """
    Global site configuration.
    """
    site_name = models.CharField(max_length=100, default='ZimTechHub')
    site_tagline = models.CharField(max_length=200, default="Zimbabwe's Premier Tech Marketplace")
    site_logo = models.ImageField(upload_to='site/', blank=True)
    site_favicon = models.ImageField(upload_to='site/', blank=True)
    maintenance_mode = models.BooleanField(default=False)
    allow_registration = models.BooleanField(default=True)
    default_currency = models.CharField(max_length=3, default='USD')
    contact_email = models.EmailField(default='support@zimtechhub.co.zw')
    support_phone = models.CharField(max_length=20, blank=True)
    social_links = models.JSONField(default=dict, blank=True)
    seo_description = models.TextField(blank=True)
    seo_keywords = models.CharField(max_length=500, blank=True)
    google_analytics_id = models.CharField(max_length=50, blank=True)
    custom_css = models.TextField(blank=True)
    custom_js = models.TextField(blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'Site Setting'
        verbose_name_plural = 'Site Settings'

    def __str__(self):
        return self.site_name

    def save(self, *args, **kwargs):
        self.pk = 1  # Ensure only one instance exists
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class AuditLog(models.Model):
    """
    Audit log for tracking important actions.
    """
    ACTION_CHOICES = [
        ('CREATE', 'Create'),
        ('UPDATE', 'Update'),
        ('DELETE', 'Delete'),
        ('LOGIN', 'Login'),
        ('LOGOUT', 'Logout'),
        ('DOWNLOAD', 'Download'),
        ('PURCHASE', 'Purchase'),
        ('REVIEW', 'Review'),
        ('REPORT', 'Report'),
        ('BAN', 'Ban'),
        ('UNBAN', 'Unban'),
    ]

    # Use the lazy string reference to settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    model_name = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    object_repr = models.CharField(max_length=200)
    changes = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['user', 'action']),
            models.Index(fields=['model_name', 'object_id']),
        ]

    def __str__(self):
        return f"{self.user} - {self.action} - {self.model_name}"