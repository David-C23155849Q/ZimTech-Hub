from django.contrib import admin
from .models import Project, ProjectStar, ProjectBookmark

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'owner', 'status', 'stars', 'views', 'is_public', 'created_at']
    list_filter = ['status', 'is_public', 'is_featured']
    search_fields = ['title', 'description', 'owner__username']
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ProjectStar)
class ProjectStarAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'created_at']

@admin.register(ProjectBookmark)
class ProjectBookmarkAdmin(admin.ModelAdmin):
    list_display = ['user', 'project', 'created_at']
