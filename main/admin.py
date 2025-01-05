from django.contrib import admin

from .models import Post, WiseUser


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['author', 'publish', 'status', 'report', 'id']
    list_filter = ['status', 'created', 'publish', 'author']
    search_fields = ['text']
    raw_id_fields = ['author']
    date_hierarchy = 'publish'
    ordering = ['status', 'publish']

admin.site.register(WiseUser)
