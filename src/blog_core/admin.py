"""Django admin for Blog, Section, and Article."""

from __future__ import annotations

from django.contrib import admin, messages
from django.utils import timezone
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _

from blog_core.models import Article, Blog, Section


class SectionInline(admin.TabularInline):
    model = Section
    extra = 0
    fields = ("name", "slug", "sort_order")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "updated_at")
    list_filter = ("is_active",)
    search_fields = ("name", "slug", "description")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [SectionInline]


@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
    list_display = ("name", "blog", "slug", "sort_order")
    list_filter = ("blog",)
    search_fields = ("name", "slug")
    prepopulated_fields = {"slug": ("name",)}


@admin.action(description=_("Publish selected articles now"))
def publish_now(modeladmin, request, queryset):
    updated = queryset.update(
        state=Article.STATE_PUBLISHED, publish_at=timezone.now()
    )
    modeladmin.message_user(
        request,
        _("%(count)d article(s) published.") % {"count": updated},
        messages.SUCCESS,
    )


@admin.action(description=_("Mark selected as draft"))
def mark_draft(modeladmin, request, queryset):
    updated = queryset.update(state=Article.STATE_DRAFT)
    modeladmin.message_user(
        request,
        _("%(count)d article(s) set to draft.") % {"count": updated},
        messages.SUCCESS,
    )


@admin.action(description=_("Archive selected articles"))
def archive_articles(modeladmin, request, queryset):
    updated = queryset.update(state=Article.STATE_ARCHIVED)
    modeladmin.message_user(
        request,
        _("%(count)d article(s) archived.") % {"count": updated},
        messages.SUCCESS,
    )


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "blog",
        "state",
        "publish_at",
        "author",
        "body_format",
        "view_count",
        "preview_link",
    )
    list_filter = ("state", "body_format", "blog", "section")
    search_fields = ("title", "slug", "teaser", "body")
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_at"
    autocomplete_fields = ("blog", "section", "author")
    readonly_fields = ("secret_key", "view_count", "created_at", "updated_at")
    actions = [publish_now, mark_draft, archive_articles]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "blog",
                    "section",
                    "title",
                    "slug",
                    "teaser",
                    "body",
                    "body_format",
                )
            },
        ),
        (
            _("Publishing"),
            {"fields": ("state", "publish_at", "author")},
        ),
        (
            _("Preview & metadata"),
            {
                "classes": ("collapse",),
                "fields": (
                    "secret_key",
                    "view_count",
                    "metadata",
                    "created_at",
                    "updated_at",
                ),
            },
        ),
    )

    @admin.display(description=_("Preview"))
    def preview_link(self, obj: Article):
        url = obj.get_preview_url()
        if not url:
            return "—"
        return format_html('<a href="{}" target="_blank">{}</a>', url, _("Open"))
