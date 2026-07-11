================================================================================
FILE: apps/accounts/urls.py
================================================================================
"""
Accounts URL patterns
"""
from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    path('verify/<uidb64>/<token>/', views.EmailVerificationView.as_view(), name='verify_email'),
    path('settings/', views.SettingsView.as_view(), name='settings'),
    path('settings/change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('profile/', views.ProfileRedirectView.as_view(), name='profile_redirect'),
]


================================================================================


================================================================================
FILE: apps/analytics/urls.py
================================================================================
"""
Analytics URL patterns
"""
from django.urls import path
from . import views

app_name = 'analytics'

urlpatterns = [
    path('', views.AnalyticsOverviewView.as_view(), name='overview'),
    path('platform/', views.PlatformAnalyticsView.as_view(), name='platform'),
    path('revenue/', views.RevenueAnalyticsView.as_view(), name='revenue'),
    path('users/', views.UserAnalyticsView.as_view(), name='users'),
    path('products/', views.ProductAnalyticsView.as_view(), name='products'),
    path('traffic/', views.TrafficAnalyticsView.as_view(), name='traffic'),
    path('export/<str:report_type>/', views.ExportReportView.as_view(), name='export'),
    path('reports/scheduled/', views.ScheduledReportsView.as_view(), name='scheduled_reports'),
    path('reports/create/', views.CreateReportView.as_view(), name='create_report'),
]


================================================================================


================================================================================
FILE: apps/api/urls.py
================================================================================
"""
API URL patterns
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

router = DefaultRouter()

urlpatterns = [
    path('', include(router.urls)),

    # JWT Authentication
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/token/verify/', TokenVerifyView.as_view(), name='token_verify'),

    # User endpoints
    path('users/', include([
        path('', views.UserListAPIView.as_view(), name='user_list'),
        path('me/', views.CurrentUserAPIView.as_view(), name='current_user'),
        path('<uuid:pk>/', views.UserDetailAPIView.as_view(), name='user_detail'),
        path('<uuid:pk>/profile/', views.UserProfileAPIView.as_view(), name='user_profile'),
        path('<uuid:pk>/followers/', views.UserFollowersAPIView.as_view(), name='user_followers'),
        path('<uuid:pk>/following/', views.UserFollowingAPIView.as_view(), name='user_following'),
        path('<uuid:pk>/follow/', views.FollowToggleAPIView.as_view(), name='follow_toggle'),
    ])),

    # Products endpoints
    path('products/', include([
        path('', views.ProductListAPIView.as_view(), name='api_product_list'),
        path('featured/', views.FeaturedProductsAPIView.as_view(), name='featured_products'),
        path('<uuid:pk>/', views.ProductDetailAPIView.as_view(), name='api_product_detail'),
        path('<uuid:pk>/reviews/', views.ProductReviewsAPIView.as_view(), name='api_product_reviews'),
    ])),

    # Projects endpoints
    path('projects/', include([
        path('', views.ProjectListAPIView.as_view(), name='api_project_list'),
        path('trending/', views.TrendingProjectsAPIView.as_view(), name='trending_projects'),
        path('<uuid:pk>/', views.ProjectDetailAPIView.as_view(), name='api_project_detail'),
        path('<uuid:pk>/star/', views.ProjectStarAPIView.as_view(), name='api_project_star'),
    ])),

    # Jobs endpoints
    path('jobs/', include([
        path('', views.JobListAPIView.as_view(), name='api_job_list'),
        path('<uuid:pk>/', views.JobDetailAPIView.as_view(), name='api_job_detail'),
        path('<uuid:pk>/apply/', views.JobApplyAPIView.as_view(), name='api_job_apply'),
    ])),

    # Posts endpoints
    path('posts/', include([
        path('', views.PostListAPIView.as_view(), name='api_post_list'),
        path('feed/', views.FeedAPIView.as_view(), name='api_feed'),
        path('<uuid:pk>/', views.PostDetailAPIView.as_view(), name='api_post_detail'),
        path('<uuid:pk>/like/', views.PostLikeAPIView.as_view(), name='api_post_like'),
    ])),

    # Search
    path('search/', views.GlobalSearchAPIView.as_view(), name='api_search'),

    # Notifications
    path('notifications/', include([
        path('', views.NotificationListAPIView.as_view(), name='api_notifications'),
        path('unread-count/', views.UnreadCountAPIView.as_view(), name='api_unread_count'),
        path('<uuid:pk>/read/', views.MarkReadAPIView.as_view(), name='api_mark_read'),
        path('mark-all-read/', views.MarkAllReadAPIView.as_view(), name='api_mark_all_read'),
    ])),

    # Messaging
    path('messages/', include([
        path('conversations/', views.ConversationListAPIView.as_view(), name='api_conversations'),
        path('conversations/<uuid:pk>/', views.ConversationDetailAPIView.as_view(), name='api_conversation'),
        path('conversations/<uuid:pk>/messages/', views.MessageListAPIView.as_view(), name='api_messages'),
        path('send/', views.SendMessageAPIView.as_view(), name='api_send_message'),
    ])),
]


================================================================================


================================================================================
FILE: apps/comments/urls.py
================================================================================
"""
Comments URL patterns
"""
from django.urls import path
from . import views

app_name = 'comments'

urlpatterns = [
    path('create/<str:app_label>/<str:model_name>/<uuid:object_id>/', 
         views.CommentCreateView.as_view(), name='create'),
    path('<uuid:pk>/', views.CommentDetailView.as_view(), name='detail'),
    path('<uuid:pk>/edit/', views.CommentUpdateView.as_view(), name='edit'),
    path('<uuid:pk>/delete/', views.CommentDeleteView.as_view(), name='delete'),
    path('<uuid:pk>/reply/', views.CommentReplyView.as_view(), name='reply'),
    path('<uuid:pk>/like/', views.CommentLikeToggleView.as_view(), name='like_toggle'),
]


================================================================================


================================================================================
FILE: apps/companies/urls.py
================================================================================
"""
Companies URL patterns
"""
from django.urls import path
from . import views

app_name = 'companies'

urlpatterns = [
    path('', views.CompanyListView.as_view(), name='list'),
    path('create/', views.CompanyCreateView.as_view(), name='create'),
    path('<slug:slug>/', views.CompanyDetailView.as_view(), name='detail'),
    path('<slug:slug>/edit/', views.CompanyUpdateView.as_view(), name='edit'),
    path('<slug:slug>/follow/', views.CompanyFollowToggleView.as_view(), name='follow_toggle'),
    path('<slug:slug>/jobs/', views.CompanyJobsView.as_view(), name='jobs'),
]


================================================================================


================================================================================
FILE: apps/core/urls.py
================================================================================
"""
Core URL patterns
"""
from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('terms/', views.TermsView.as_view(), name='terms'),
    path('privacy/', views.PrivacyView.as_view(), name='privacy'),
    path('search/', views.SearchView.as_view(), name='search'),
]


================================================================================


================================================================================
FILE: apps/dashboard/urls.py
================================================================================
"""
Dashboard URL patterns
"""
from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.DashboardView.as_view(), name='index'),
    path('analytics/', views.AnalyticsView.as_view(), name='analytics'),
    path('products/', views.DashboardProductsView.as_view(), name='products'),
    path('orders/', views.DashboardOrdersView.as_view(), name='orders'),
    path('sales/', views.SalesHistoryView.as_view(), name='sales'),
    path('earnings/', views.EarningsView.as_view(), name='earnings'),
    path('reviews/', views.DashboardReviewsView.as_view(), name='reviews'),
    path('settings/', views.DashboardSettingsView.as_view(), name='settings'),
]


================================================================================


================================================================================
FILE: apps/events/urls.py
================================================================================
"""
Events URL patterns
"""
from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.EventListView.as_view(), name='list'),
    path('crea<response clipped><NOTE>Result is longer than **10000 characters**, will be **truncated**.</NOTE>