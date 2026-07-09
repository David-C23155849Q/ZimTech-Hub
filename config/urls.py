"""
ZimTechHub URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.api.urls')),
    path('accounts/', include('apps.accounts.urls')),
    path('profiles/', include('apps.profiles.urls')),
    path('projects/', include('apps.projects.urls')),
    path('marketplace/', include('apps.marketplace.urls')),
    path('orders/', include('apps.orders.urls')),
    path('posts/', include('apps.posts.urls')),
    # path('jobs/', include('apps.jobs.urls')),
    path('services/', include('apps.services.urls')),
    path('companies/', include('apps.companies.urls')),
    path('events/', include('apps.events.urls')),
    path('learning/', include('apps.learning.urls')),
    path('messaging/', include('apps.messaging.urls')),
    path('notifications/', include('apps.notifications.urls')),
    path('wallet/', include('apps.wallet.urls')),
    path('reviews/', include('apps.reviews.urls')),
    path('search/', include('apps.search.urls')),
    path('moderation/', include('apps.moderation.urls')),
    path('products/', include('apps.products.urls', namespace='products')),
    path('jobs/', include('apps.jobs.urls', namespace='jobs')),
    path('', include('apps.core.urls')),
    path('dashboard/', include('apps.dashboard.urls', namespace='dashboard')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
