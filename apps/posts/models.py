from django.db import models
from django.conf import settings
import uuid


class Post(models.Model):

    class PostType(models.TextChoices):

        TEXT = "text", "Text"
        IMAGE = "image", "Image"
        VIDEO = "video", "Video"
        LINK = "link", "Link"
        CODE = "code", "Code"
        POLL = "poll", "Poll"


    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="posts"
    )


    title = models.CharField(
        max_length=300,
        blank=True
    )


    content = models.TextField()


    post_type = models.CharField(
        max_length=20,
        choices=PostType.choices,
        default=PostType.TEXT
    )


    # Video upload
    video = models.FileField(
        upload_to="posts/videos/",
        blank=True,
        null=True
    )


    # Code posts
    code_snippet = models.TextField(
        blank=True
    )


    language = models.CharField(
        max_length=50,
        blank=True
    )


    # Links
    link_url = models.URLField(
        blank=True
    )


    link_title = models.CharField(
        max_length=200,
        blank=True
    )


    link_description = models.TextField(
        blank=True
    )


    link_image = models.URLField(
        blank=True
    )


    # Hashtags
    hashtags = models.JSONField(
        default=list,
        blank=True
    )


    mentions = models.JSONField(
        default=list,
        blank=True
    )


    # Engagement

    likes_count = models.PositiveIntegerField(
        default=0
    )


    comments_count = models.PositiveIntegerField(
        default=0
    )


    shares_count = models.PositiveIntegerField(
        default=0
    )


    bookmarks_count = models.PositiveIntegerField(
        default=0
    )


    is_published = models.BooleanField(
        default=True
    )


    is_pinned = models.BooleanField(
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


    def __str__(self):
        return f"{self.author.username} - {self.title}"



# Multiple images per post

class PostImage(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="images",
        on_delete=models.CASCADE
    )


    image = models.ImageField(
        upload_to="posts/images/"
    )


    uploaded_at = models.DateTimeField(
        auto_now_add=True
    )


    def __str__(self):
        return f"Image for {self.post}"



# Poll choices

class PollOption(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="poll_options"
    )

    text = models.CharField(
        max_length=200
    )


    def vote_count(self):
        return self.votes.count()


    def __str__(self):
        return self.text


# User votes

class PollVote(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    option = models.ForeignKey(
        PollOption,
        related_name="votes",
        on_delete=models.CASCADE
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = [
            "user",
            "option"
        ]