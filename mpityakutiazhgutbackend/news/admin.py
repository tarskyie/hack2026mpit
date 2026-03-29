from django.contrib import admin
from .models import News

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("title", "created_at", "author")
    search_fields = ("title", "content")
    list_filter = ("created_at",)