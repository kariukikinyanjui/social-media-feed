from django.contrib import admin
from .models import Post


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'content', 'timestamp', 'likes_count', 'comments_count', 'shares_count')
    search_fields = ('author__username', 'content')
