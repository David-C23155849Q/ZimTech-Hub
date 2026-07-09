from django.contrib import admin
from .models import Profile, Follow, Badge, UserBadge

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'headline', 'country', 'verification_status', 'reputation_score']
    list_filter = ['verification_status', 'availability', 'experience_level']
    search_fields = ['user__username', 'bio', 'headline']

@admin.register(Follow)
class FollowAdmin(admin.ModelAdmin):
    list_display = ['follower', 'following', 'created_at']

@admin.register(Badge)
class BadgeAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']

@admin.register(UserBadge)
class UserBadgeAdmin(admin.ModelAdmin):
    list_display = ['user', 'badge', 'awarded_at']
