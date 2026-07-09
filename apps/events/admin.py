from django.contrib import admin
from .models import Event

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'event_type', 'venue', 'start_date', 'is_published', 'is_featured']
    list_filter = ['event_type', 'is_published', 'is_featured']
    search_fields = ['title', 'description', 'venue']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['attendees']
