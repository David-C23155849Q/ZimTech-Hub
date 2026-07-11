# posts/models.py
from django.db import models
from django.conf import settings
import uuid
from taggit.managers import TaggableManager
from django.utils.text import slugify


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
    tags = TaggableManager(
        blank=True,
        help_text="Add hashtags like python, django, coding"
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

        indexes = [
            models.Index(fields=["created_at"]),
            models.Index(fields=["post_type"]),
            models.Index(fields=["author"]),
            models.Index(fields=["is_published"]),
        ]


    slug = models.SlugField(
    max_length=350,
    unique=True,
    blank=True,
    null=True
)


    def save(self, *args, **kwargs):

        if not self.slug:

            base_slug = slugify(
                self.title if self.title else str(self.id)
            )

            slug = base_slug
            counter = 1


            while Post.objects.filter(slug=slug).exists():

                slug = f"{base_slug}-{counter}"
                counter += 1


            self.slug = slug


        super().save(*args, **kwargs)



    def __str__(self):

        return f"{self.author.username} - {self.title}"
    
# Mentions model to track which users are mentioned in a post

class PostMention(models.Model):

    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="mentions"
    )


    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="mentions"
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = [
            "post",
            "user"
        ]


    def __str__(self):
        return f"{self.user.username} mentioned in {self.post.id}"

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

        constraints = [
            models.UniqueConstraint(
                fields=[
                    "user",
                    "option"
                ],
                name="unique_user_option_vote"
            )
        ]

class PostLike(models.Model):

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    post = models.ForeignKey(
        Post,
        related_name="likes",
        on_delete=models.CASCADE
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )


    class Meta:
        unique_together = [
            "user",
            "post"
        ]

class Comment(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="comments",
        on_delete=models.CASCADE
    )


    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )


    content = models.TextField()


    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        related_name="replies",
        on_delete=models.CASCADE
    )


    created_at = models.DateTimeField(
        auto_now_add=True
    )


class PostEditHistory(models.Model):

    post = models.ForeignKey(
        Post,
        related_name="edit_history",
        on_delete=models.CASCADE
    )

    old_content = models.TextField()

    edited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    edited_at = models.DateTimeField(
        auto_now_add=True
    )