from django.contrib import admin
from .models import Post

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'title', 'post_type', 'likes_count', 'is_published', 'created_at']
    list_filter = ['post_type', 'is_published', 'is_pinned']
    search_fields = ['title', 'content', 'author__username']
