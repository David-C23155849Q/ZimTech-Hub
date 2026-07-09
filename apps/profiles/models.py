from django.db import models
from django.contrib.auth import get_user_model
from django.core.validators import URLValidator
from django.utils import timezone
import uuid
from django.conf import settings
from django.core.validators import URLValidator

# User = get_user_model()

class Profile(models.Model):
    class VerificationStatus(models.TextChoices):
        UNVERIFIED = 'unverified', 'Unverified'
        PENDING = 'pending', 'Pending'
        VERIFIED = 'verified', 'Verified'
        REJECTED = 'rejected', 'Rejected'

    class AvailabilityStatus(models.TextChoices):
        AVAILABLE = 'available', 'Available for work'
        BUSY = 'busy', 'Busy'
        OPEN = 'open', 'Open to offers'
        NOT_LOOKING = 'not_looking', 'Not looking'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # Use settings.AUTH_USER_MODEL here to fix the LookupError/ImproperlyConfigured crash
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='profile'
    )
    
    avatar = models.ImageField(upload_to='avatars/', blank=True, default='avatars/default.png')
    cover_image = models.ImageField(upload_to='covers/', blank=True)
    bio = models.TextField(max_length=500, blank=True)
    headline = models.CharField(max_length=150, blank=True)
    country = models.CharField(max_length=100, blank=True, default='Zimbabwe')
    city = models.CharField(max_length=100, blank=True)
    user_timezone = models.CharField(max_length=50, default='Africa/Harare')
    skills = models.JSONField(default=list, blank=True)
    programming_languages = models.JSONField(default=list, blank=True)
    frameworks = models.JSONField(default=list, blank=True)
    experience_level = models.CharField(
        max_length=20, 
        choices=[('beginner','Beginner'),('intermediate','Intermediate'),('advanced','Advanced'),('expert','Expert')], 
        default='beginner'
    )
    github_url = models.URLField(blank=True, validators=[URLValidator()])
    linkedin_url = models.URLField(blank=True, validators=[URLValidator()])
    portfolio_url = models.URLField(blank=True, validators=[URLValidator()])
    website_url = models.URLField(blank=True, validators=[URLValidator()])
    twitter_url = models.URLField(blank=True, validators=[URLValidator()])
    cv = models.FileField(upload_to='cvs/', blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True)
    availability = models.CharField(max_length=20, choices=AvailabilityStatus.choices, default=AvailabilityStatus.AVAILABLE)
    verification_status = models.CharField(max_length=20, choices=VerificationStatus.choices, default=VerificationStatus.UNVERIFIED)
    reputation_score = models.PositiveIntegerField(default=0)
    total_sales = models.PositiveIntegerField(default=0)
    total_reviews = models.PositiveIntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    follower_count = models.PositiveIntegerField(default=0)
    following_count = models.PositiveIntegerField(default=0)
    project_count = models.PositiveIntegerField(default=0)
    product_count = models.PositiveIntegerField(default=0)
    last_seen = models.DateTimeField(default=timezone.now)
    is_public = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    class Meta:
        ordering = ['-reputation_score']

    def __str__(self):
        return f"{self.user.username}'s Profile"
    

# ... (Profile model remains as you corrected it)

class Follow(models.Model):
    # Use settings.AUTH_USER_MODEL instead of User
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='following_set')
    following = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='followers_set')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['follower', 'following']

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/')
    color = models.CharField(max_length=7, default='#FFD700')
    criteria = models.TextField()
    is_active = models.BooleanField(default=True)

class UserBadge(models.Model):
    # Use settings.AUTH_USER_MODEL instead of User
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='badges')
    badge = models.ForeignKey(Badge, on_delete=models.CASCADE)
    awarded_at = models.DateTimeField(auto_now_add=True)
    # Use settings.AUTH_USER_MODEL instead of User
    awarded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='awarded_badges')
    reason = models.TextField(blank=True)

    class Meta:
        unique_together = ['user', 'badge']


import uuid

def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('avatars/', filename)

# Update your model field:
avatar = models.ImageField(upload_to=get_file_path, blank=True)       