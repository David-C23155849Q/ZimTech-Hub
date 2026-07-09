from django.db import models
from django.conf import settings  # Use this instead of get_user_model
from django.utils import timezone
import uuid

# REMOVED: from django.contrib.auth import get_user_model
# REMOVED: User = get_user_model()

class Event(models.Model):
    class EventType(models.TextChoices):
        MEETUP = 'meetup', 'Meetup'
        HACKATHON = 'hackathon', 'Hackathon'
        TECH_TALK = 'tech_talk', 'Tech Talk'
        BOOTCAMP = 'bootcamp', 'Bootcamp'
        WORKSHOP = 'workshop', 'Workshop'
        CONFERENCE = 'conference', 'Conference'

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    organizer = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='organized_events'
    )
    
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, max_length=250)
    description = models.TextField()
    event_type = models.CharField(max_length=20, choices=EventType.choices, default=EventType.MEETUP)
    banner = models.ImageField(upload_to='events/banners/')
    venue = models.CharField(max_length=300)
    address = models.TextField(blank=True)
    map_url = models.URLField(blank=True)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    registration_url = models.URLField(blank=True)
    max_attendees = models.PositiveIntegerField(null=True, blank=True)
    
    # CORRECTED: Use settings.AUTH_USER_MODEL
    attendees = models.ManyToManyField(
        settings.AUTH_USER_MODEL, 
        related_name='events_attending', 
        blank=True
    )
    
    speakers = models.JSONField(default=list, blank=True)
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    is_published = models.BooleanField(default=False)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date']

    def __str__(self):
        return self.title

    @property
    def is_upcoming(self):
        return self.start_date > timezone.now()

    @property
    def is_ongoing(self):
        now = timezone.now()
        return self.start_date <= now <= self.end_date

    @property
    def is_past(self):
        return self.end_date < timezone.now()