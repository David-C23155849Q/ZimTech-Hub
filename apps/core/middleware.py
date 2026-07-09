"""
Core middleware for ZimTechHub
"""
from django.utils import timezone
from django.utils.deprecation import MiddlewareMixin


class TimezoneMiddleware(MiddlewareMixin):
    """
    Activate the user's preferred timezone.
    """
    def process_request(self, request):
        if request.user.is_authenticated and hasattr(request.user, 'profile'):
            
            tz = getattr(request.user.profile, 'user_timezone', 'Africa/Harare')
            timezone.activate(tz)
        else:
            timezone.deactivate()
    


class ActivityMiddleware(MiddlewareMixin):
    """
    Update user's last activity timestamp.
    """
    def process_request(self, request):
        if request.user.is_authenticated:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            # Update last seen every 5 minutes to avoid excessive DB writes
            if hasattr(request.user, 'profile'):
                profile = request.user.profile
                if not profile.last_seen or (timezone.now() - profile.last_seen).seconds > 300:
                    profile.last_seen = timezone.now()
                    profile.save(update_fields=['last_seen'])
