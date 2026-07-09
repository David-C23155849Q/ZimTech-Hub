"""
ASGI config for ZimTechHub project.
"""

import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Import routing after Django setup
django_asgi_app = get_asgi_application()

from apps.messaging import routing as messaging_routing
from apps.notifications import routing as notifications_routing

application = ProtocolTypeRouter({
    'http': django_asgi_app,
    'websocket': AuthMiddlewareStack(
        URLRouter(
            messaging_routing.websocket_urlpatterns +
            notifications_routing.websocket_urlpatterns
        )
    ),
})
