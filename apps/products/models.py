from django.db import models
from django.conf import settings  # Required for AUTH_USER_MODEL
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils import timezone
import uuid

# REMOVED: from django.contrib.auth import get_user_model
# REMOVED: User = get_user_model()

class Product(models.Model):
    class Status(models.TextChoices):
        DRAFT = 'draft', 'Draft'
        PENDING = 'pending', 'Pending Review'
        ACTIVE = 'active', 'Active'
        INACTIVE = 'inactive', 'Inactive'
        SUSPENDED = 'suspended', 'Suspended'

    class LicenseType(models.TextChoices):
        MIT = 'mit', 'MIT License'
        GPL = 'gpl', 'GPL License'
        APACHE = 'apache', 'Apache 2.0'
        COMMERCIAL = 'commercial', 'Commercial'
        PERSONAL = 'personal', 'Personal Use'
        OTHER = 'other', 'Other'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # CORRECTED: Use settings.AUTH_USER_MODEL instead of the User variable
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='products'
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    short_description = models.CharField(max_length=300, blank=True)

    # Categorization
    category = models.ForeignKey('core.Category', on_delete=models.SET_NULL, null=True, related_name='products')
    tags = models.JSONField(default=list, blank=True)

    # Media
    thumbnail = models.ImageField(upload_to='products/thumbnails/')
    screenshots = models.JSONField(default=list, blank=True)
    preview_video = models.URLField(blank=True)

    # Pricing
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    original_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    discount_percentage = models.PositiveIntegerField(default=0, validators=[MaxValueValidator(100)])
    currency = models.CharField(max_length=3, default='USD')

    # Product File
    file = models.FileField(upload_to='products/files/')
    file_size = models.PositiveIntegerField(help_text='Size in bytes', default=0)
    version = models.CharField(max_length=20, default='1.0.0')

    # Details
    license = models.CharField(max_length=20, choices=LicenseType.choices, default=LicenseType.MIT)
    documentation = models.URLField(blank=True)
    release_notes = models.TextField(blank=True)
    requirements = models.TextField(blank=True)
    faq = models.JSONField(default=list, blank=True)
    support_email = models.EmailField(blank=True)

    # Stats
    view_count = models.PositiveIntegerField(default=0)
    download_count = models.PositiveIntegerField(default=0)
    sales_count = models.PositiveIntegerField(default=0)
    review_count = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)

    # Status
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT)
    is_featured = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    # SEO
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['status', 'is_active']),
            models.Index(fields=['seller', 'status']),
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['price', 'is_active']),
        ]

    def __str__(self):
        return self.title

    def get_discount_price(self):
        if self.discount_percentage > 0:
            return self.price * (1 - self.discount_percentage / 100)
        return self.price

    def publish(self):
        self.status = self.Status.ACTIVE
        self.published_at = timezone.now()
        self.save()