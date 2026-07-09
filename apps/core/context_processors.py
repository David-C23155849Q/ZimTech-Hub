"""
Core context processors
"""
from .models import SiteSettings


def site_settings(request):
    """
    Add site settings to template context.
    """
    try:
        settings = SiteSettings.get_settings()
    except:
        settings = None

    return {
        'site_settings': settings,
    }


def notifications(request):
    """
    Add unread notification count to template context.
    """
    if request.user.is_authenticated:
        try:
            unread_count = request.user.notifications.filter(is_read=False).count()
        except:
            unread_count = 0
        return {'unread_notifications': unread_count}
    return {'unread_notifications': 0}
