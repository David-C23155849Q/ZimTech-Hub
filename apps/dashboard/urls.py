"""
Dashboard URL patterns.
"""

from django.urls import path
from . import views


app_name = "dashboard"


urlpatterns = [


path(
        "",
        views.DashboardView.as_view(),
        name="dashboard"
    ),
    # Main dashboard
    # path(
    #     "",
    #     views.DashboardView.as_view(),
    #     name="index"
    # ),


    # # Notifications
    # path(
    #     "notifications/",
    #     views.NotificationsView.as_view(),
    #     name="notifications"
    # ),


    # # Mark notification read
    # path(
    #     "notifications/<int:pk>/read/",
    #     views.MarkNotificationReadView.as_view(),
    #     name="notification_read"
    # ),


    # # Analytics
    # path(
    #     "analytics/",
    #     views.AnalyticsView.as_view(),
    #     name="analytics"
    # ),


    # # Quick actions

    # path(
    #     "create-post/",
    #     views.CreatePostView.as_view(),
    #     name="create_post"
    # ),


    # path(
    #     "create-project/",
    #     views.CreateProjectView.as_view(),
    #     name="create_project"
    # ),


]