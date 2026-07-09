from django.db import models
from django.conf import settings  # Use this for lazy model references
from django.core.validators import URLValidator
import uuid

# REMOVED: from django.contrib.auth import get_user_model
# REMOVED: User = get_user_model()

class Company(models.Model):
    class FundingStage(models.TextChoices):
        PRE_SEED = 'pre_seed', 'Pre-seed'
        SEED = 'seed', 'Seed'
        SERIES_A = 'series_a', 'Series A'
        SERIES_B = 'series_b', 'Series B'
        SERIES_C = 'series_c', 'Series C'
        IPO = 'ipo', 'IPO'
        BOOTSTRAPPED = 'bootstrapped', 'Bootstrapped'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    tagline = models.CharField(max_length=200, blank=True)
    description = models.TextField()
    logo = models.ImageField(upload_to='companies/logos/')
    cover_image = models.ImageField(upload_to='companies/covers/', blank=True)
    website = models.URLField(blank=True, validators=[URLValidator()])
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    country = models.CharField(max_length=100, default='Zimbabwe')
    city = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    industry = models.CharField(max_length=100, blank=True)
    company_size = models.CharField(max_length=50, blank=True, choices=[('1-10','1-10 employees'),('11-50','11-50 employees'),('51-200','51-200 employees'),('201-500','201-500 employees'),('500+','500+ employees')])
    founded_year = models.PositiveIntegerField(null=True, blank=True)
    funding_stage = models.CharField(max_length=20, choices=FundingStage.choices, blank=True)
    tech_stack = models.JSONField(default=list, blank=True)
    linkedin_url = models.URLField(blank=True)
    twitter_url = models.URLField(blank=True)
    github_url = models.URLField(blank=True)
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    founders = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='founded_companies', 
        blank=True
    )
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    team_members = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='companies', 
        blank=True
    )
    
    follower_count = models.PositiveIntegerField(default=0)
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Companies'
        ordering = ['-created_at']

    def __str__(self):
        return self.name