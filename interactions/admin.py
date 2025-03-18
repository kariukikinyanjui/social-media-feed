from django.contrib import admin
from .models import Comment, Like, Share


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'text', 'timestamp')


@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'timestamp')


@admin.register(Share)
class ShareAdmin(admin.ModelAdmin):
    list_display = ('post', 'user', 'timestamp')
