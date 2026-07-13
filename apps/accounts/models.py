"""
Accounts models for ZimTechHub
Custom user model with role-based access control.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator
from django.db.models.signals import post_save
from django.dispatch import receiver

import uuid

from .managers import UserManager



# ==============================
# ROLE MODEL
# ==============================

class Role(models.Model):

    DEVELOPER = "developer"
    FREELANCER = "freelancer"
    COMPANY = "company"
    CLIENT = "client"
    RECRUITER = "recruiter"
    STUDENT = "student"

    ROLE_CHOICES = [
        (DEVELOPER, "Developer"),
        (FREELANCER, "Freelancer"),
        (COMPANY, "Company"),
        (CLIENT, "Client"),
        (RECRUITER, "Recruiter"),
        (STUDENT, "Student"),
    ]


    name = models.CharField(
        max_length=30,
        choices=ROLE_CHOICES,
        unique=True
    )

    description = models.TextField(
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return self.get_name_display()



# ==============================
# USER MODEL
# ==============================


class User(AbstractBaseUser, PermissionsMixin):


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


    email = models.EmailField(
        _('email address'),
        unique=True
    )


    username = models.CharField(
        _('username'),
        max_length=30,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message=_(
                    'Username can only contain letters, numbers, and underscores.'
                )
            )
        ]
    )


    first_name = models.CharField(
        max_length=150,
        blank=True
    )


    last_name = models.CharField(
        max_length=150,
        blank=True
    )


    # MANY TO MANY ROLES

    roles = models.ManyToManyField(
        Role,
        related_name="users",
        blank=True
    )


    # STATUS

    is_staff = models.BooleanField(default=False)

    is_active = models.BooleanField(default=True)

    is_verified = models.BooleanField(default=False)

    is_online = models.BooleanField(default=False)



    # SECURITY

    two_factor_enabled = models.BooleanField(default=False)

    two_factor_secret = models.CharField(
        max_length=100,
        blank=True
    )


    failed_login_attempts = models.PositiveIntegerField(
        default=0
    )


    locked_until = models.DateTimeField(
        null=True,
        blank=True
    )



    # EMAIL

    email_verified = models.BooleanField(
        default=False
    )


    email_verification_token = models.CharField(
        max_length=100,
        blank=True
    )



    # PASSWORD RESET

    password_reset_token = models.CharField(
        max_length=100,
        blank=True
    )


    password_reset_sent_at = models.DateTimeField(
        null=True,
        blank=True
    )



    # SOCIAL LOGIN

    github_id = models.CharField(
        max_length=100,
        blank=True
    )

    google_id = models.CharField(
        max_length=100,
        blank=True
    )

    linkedin_id = models.CharField(
        max_length=100,
        blank=True
    )



    date_joined = models.DateTimeField(
        default=timezone.now
    )


    objects = UserManager()



    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = [
        "username"
    ]



    class Meta:

        ordering = [
            "-date_joined"
        ]



    def __str__(self):

        return self.username



    @property
    def full_name(self):

        return (
            f"{self.first_name} {self.last_name}".strip()
            or self.username
        )



    @property
    def display_name(self):

        return self.full_name



    def get_initials(self):

        if self.first_name and self.last_name:

            return (
                self.first_name[0]
                +
                self.last_name[0]
            ).upper()


        return self.username[:2].upper()



    def is_locked(self):

        return (
            self.locked_until
            and self.locked_until > timezone.now()
        )



    def unlock(self):

        self.failed_login_attempts = 0
        self.locked_until = None

        self.save(
            update_fields=[
                "failed_login_attempts",
                "locked_until"
            ]
        )



    def has_role(self, role_name):

        """
        Check if user has a specific role.
        """

        return self.roles.filter(
            name=role_name
        ).exists()



    def add_role(self, role_name):

        role = Role.objects.get(
            name=role_name
        )

        self.roles.add(role)



# ==============================
# USER SESSIONS
# ==============================


class UserSession(models.Model):


    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="sessions"
    )


    session_key = models.CharField(
        max_length=100
    )


    ip_address = models.GenericIPAddressField()


    user_agent = models.TextField()


    device_info = models.CharField(
        max_length=200,
        blank=True
    )


    location = models.CharField(
        max_length=200,
        blank=True
    )


    is_active = models.BooleanField(
        default=True
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    last_activity = models.DateTimeField(
        auto_now=True
    )



    class Meta:

        ordering = [
            "-last_activity"
        ]



    def __str__(self):

        return f"{self.user.username} - {self.ip_address}"




# ==============================
# PROFILE SIGNALS
# ==============================


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):

    if created:

        from apps.profiles.models import Profile

        Profile.objects.create(
            user=instance
        )



@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):

    if hasattr(instance, "profile"):

        instance.profile.save()