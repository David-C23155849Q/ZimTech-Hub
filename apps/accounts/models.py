"""
Accounts models for ZimTechHub
Custom user model with role-based access control.
"""
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
import uuid
from django.db.models.signals import post_save
from django.dispatch import receiver

from .managers import UserManager


class User(AbstractBaseUser, PermissionsMixin):
    """
    Custom User model for ZimTechHub.
    Supports multiple roles and authentication methods.
    """

    # Role choices
    class Role(models.TextChoices):
        USER = 'user', _('User')
        SELLER = 'seller', _('Seller')
        RECRUITER = 'recruiter', _('Recruiter')
        COMPANY = 'company', _('Company')
        MODERATOR = 'moderator', _('Moderator')
        ADMIN = 'admin', _('Administrator')

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message=_('Username can only contain letters, numbers, and underscores.')
            ),
        ],
        help_text=_('Required. 30 characters or fewer. Letters, digits and _ only.')
    )

    # Personal info
    first_name = models.CharField(_('first name'), max_length=150, blank=True)
    last_name = models.CharField(_('last name'), max_length=150, blank=True)

    # Role & Status
    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.USER,
        db_index=True
    )
    is_staff = models.BooleanField(_('staff status'), default=False)
    is_active = models.BooleanField(_('active'), default=True)
    is_verified = models.BooleanField(_('verified'), default=False)
    is_online = models.BooleanField(default=False)

    # Security
    two_factor_enabled = models.BooleanField(default=False)
    two_factor_secret = models.CharField(max_length=100, blank=True)
    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_until = models.DateTimeField(null=True, blank=True)

    # Email verification
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=100, blank=True)
    email_verification_sent_at = models.DateTimeField(null=True, blank=True)

    # Password reset
    password_reset_token = models.CharField(max_length=100, blank=True)
    password_reset_sent_at = models.DateTimeField(null=True, blank=True)

    # Timestamps
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    last_login = models.DateTimeField(_('last login'), blank=True, null=True)

    # Social auth fields
    github_id = models.CharField(max_length=100, blank=True, db_index=True)
    google_id = models.CharField(max_length=100, blank=True, db_index=True)
    linkedin_id = models.CharField(max_length=100, blank=True, db_index=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        indexes = [
            models.Index(fields=['email', 'is_active']),
            models.Index(fields=['username', 'is_active']),
            models.Index(fields=['role', 'is_verified']),
        ]

    def __str__(self):
        return self.username

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username

    @property
    def display_name(self):
        return self.full_name or self.username

    def get_initials(self):
        if self.first_name and self.last_name:
            return f"{self.first_name[0]}{self.last_name[0]}".upper()
        return self.username[:2].upper()

    def is_locked(self):
        if self.locked_until and self.locked_until > timezone.now():
            return True
        return False

    def unlock(self):
        self.failed_login_attempts = 0
        self.locked_until = None
        self.save(update_fields=['failed_login_attempts', 'locked_until'])

    def has_role(self, role):
        """Check if user has specific role or higher privileges."""
        role_hierarchy = {
            'user': 1,
            'seller': 2,
            'recruiter': 2,
            'company': 2,
            'moderator': 3,
            'admin': 4,
        }
        user_level = role_hierarchy.get(self.role, 1)
        required_level = role_hierarchy.get(role, 1)
        return user_level >= required_level


class UserSession(models.Model):
    """
    Track user sessions for security.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    session_key = models.CharField(max_length=100)
    ip_address = models.GenericIPAddressField()
    user_agent = models.TextField()
    device_info = models.CharField(max_length=200, blank=True)
    location = models.CharField(max_length=200, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    last_activity = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-last_activity']

        def __str__(self):
            return f"{self.user.username} - {self.ip_address}"
        
    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            from apps.profiles.models import Profile 
            Profile.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, created, **kwargs):
        if not created and hasattr(instance, 'profile'):
            instance.profile.save()
    

