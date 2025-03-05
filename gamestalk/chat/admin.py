from django.contrib import admin
from .models import Comment, Gamechat




@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['user', 'gamechat', 'created_on', 'is_active']
    list_filter = ['is_active', 'created_on', 'updated_on']
    search_fields = ['user', 'gamechat', 'body']


@admin.register(Gamechat)
class GamechatAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'author', 'created_on', 'status']
    list_filter = ['status', 'created_on', 'updated_on', 'author']
    search_fields = ['title', 'body']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_on'
    ordering = ['status', 'created_on']
    show_facets = admin.ShowFacets.ALWAYS