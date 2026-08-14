"""Django admin for the ``[events]`` extra."""

from __future__ import annotations

from django.contrib import admin

from blog_core.extras.events.models import ArticleEvent


@admin.register(ArticleEvent)
class ArticleEventAdmin(admin.ModelAdmin):
    list_display = ("article", "source", "source_id", "label", "occurred_at")
    list_filter = ("source",)
    search_fields = ("source", "source_id", "label", "body")
    autocomplete_fields = ("article",)
    date_hierarchy = "occurred_at"
    readonly_fields = ("created_at",)
