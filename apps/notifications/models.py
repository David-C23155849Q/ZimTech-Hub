"""
Notifications models for ZimTechHub.
"""

from django.db import models
from django.conf import settings



class Notification(models.Model):

    class NotificationType(models.TextChoices):

        SYSTEM = "system", "System"
        MESSAGE = "message", "Message"
        PROJECT = "project", "Project"
        ORDER = "order", "Order"
        JOB = "job", "Job"
        REVIEW = "review", "Review"



    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )


    title = models.CharField(
        max_length=200
    )


    message = models.TextField()



    notification_type = models.CharField(
        max_length=20,
        choices=NotificationType.choices,
        default=NotificationType.SYSTEM
    )


    is_read = models.BooleanField(
        default=False
    )


    action_url = models.CharField(
        max_length=300,
        blank=True
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

        return f"{self.user.username} - {self.title}"