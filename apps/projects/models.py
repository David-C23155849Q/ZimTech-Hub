from django.db import models
from django.conf import settings  # Use this for AUTH_USER_MODEL
from django.core.validators import URLValidator
import uuid

# REMOVED: from django.contrib.auth import get_user_model
# REMOVED: User = get_user_model()

import uuid

from django.conf import settings
from django.core.validators import URLValidator
from django.db import models
from django.utils.text import slugify


class Project(models.Model):
    class Status(models.TextChoices):
        OPEN_SOURCE = "open_source", "Open Source"
        IN_DEVELOPMENT = "in_development", "In Development"
        COMPLETED = "completed", "Completed"
        ARCHIVED = "archived", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="projects",
    )

    title = models.CharField(max_length=200)

    slug = models.SlugField(
        max_length=250,
        unique=True,
        blank=True,
    )

    description = models.TextField()
    content = models.TextField(blank=True, help_text="Markdown supported")

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.IN_DEVELOPMENT,
    )

    github_url = models.URLField(blank=True, validators=[URLValidator()])
    live_demo_url = models.URLField(blank=True, validators=[URLValidator()])
    documentation_url = models.URLField(blank=True, validators=[URLValidator()])

    thumbnail = models.ImageField(
        upload_to="projects/thumbnails/",
        blank=True,
    )

    screenshots = models.JSONField(default=list, blank=True)

    video_url = models.URLField(blank=True)

    technologies = models.JSONField(default=list, blank=True)
    programming_languages = models.JSONField(default=list, blank=True)
    frameworks = models.JSONField(default=list, blank=True)

    stars = models.PositiveIntegerField(default=0)
    views = models.PositiveIntegerField(default=0)
    likes = models.PositiveIntegerField(default=0)
    bookmarks = models.PositiveIntegerField(default=0)

    version = models.CharField(max_length=20, blank=True)
    license = models.CharField(max_length=50, blank=True)

    is_public = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-stars", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title) or str(self.id)[:8]
            slug = base_slug
            counter = 1

            while Project.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = slug

        super().save(*args, **kwargs)

class ProjectStar(models.Model):
    # CORRECTED: Use settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='starred_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']

class ProjectBookmark(models.Model):
    # CORRECTED: Use settings.AUTH_USER_MODEL
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='bookmarked_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user', 'project']
        