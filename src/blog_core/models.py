"""Core models: Blog, Section, Article."""

from __future__ import annotations

import secrets
import uuid

from django.conf import settings
from django.db import models
from django.urls import NoReverseMatch, reverse
from django.utils import timezone
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _

from blog_core.managers import ArticleManager


def _default_secret_key() -> str:
    return secrets.token_urlsafe(24)


class Blog(models.Model):
    """A named editorial stream (multi-blog support)."""

    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200, unique=True)
    description = models.TextField(_("description"), blank=True)
    is_active = models.BooleanField(_("active"), default=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = _("blog")
        verbose_name_plural = _("blogs")

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200] or uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)

    def get_absolute_url(self) -> str:
        from blog_core.conf import get_hookset

        return get_hookset().blog_absolute_url(self)


class Section(models.Model):
    """Optional grouping within a blog."""

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="sections",
        verbose_name=_("blog"),
    )
    name = models.CharField(_("name"), max_length=200)
    slug = models.SlugField(_("slug"), max_length=200)
    description = models.TextField(_("description"), blank=True)
    sort_order = models.PositiveIntegerField(_("sort order"), default=0)

    class Meta:
        ordering = ["sort_order", "name"]
        unique_together = [("blog", "slug")]
        verbose_name = _("section")
        verbose_name_plural = _("sections")

    def __str__(self) -> str:
        return f"{self.blog.slug}:{self.name}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)[:200] or uuid.uuid4().hex[:12]
        super().save(*args, **kwargs)


class Article(models.Model):
    """Editorial article belonging to a blog."""

    BODY_MARKDOWN = "markdown"
    BODY_HTML = "html"
    BODY_FORMAT_CHOICES = (
        (BODY_MARKDOWN, _("Markdown")),
        (BODY_HTML, _("HTML")),
    )

    STATE_DRAFT = "draft"
    STATE_SCHEDULED = "scheduled"
    STATE_PUBLISHED = "published"
    STATE_ARCHIVED = "archived"
    STATE_CHOICES = (
        (STATE_DRAFT, _("Draft")),
        (STATE_SCHEDULED, _("Scheduled")),
        (STATE_PUBLISHED, _("Published")),
        (STATE_ARCHIVED, _("Archived")),
    )

    blog = models.ForeignKey(
        Blog,
        on_delete=models.CASCADE,
        related_name="articles",
        verbose_name=_("blog"),
    )
    section = models.ForeignKey(
        Section,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="articles",
        verbose_name=_("section"),
    )
    title = models.CharField(_("title"), max_length=255)
    slug = models.SlugField(_("slug"), max_length=255)
    teaser = models.TextField(_("teaser"), blank=True)
    body = models.TextField(_("body"), blank=True)
    body_format = models.CharField(
        _("body format"),
        max_length=20,
        choices=BODY_FORMAT_CHOICES,
        default=BODY_MARKDOWN,
    )
    state = models.CharField(
        _("state"),
        max_length=20,
        choices=STATE_CHOICES,
        default=STATE_DRAFT,
        db_index=True,
    )
    publish_at = models.DateTimeField(
        _("publish at"),
        default=timezone.now,
        db_index=True,
        help_text=_(
            "Public visibility requires state=published and publish_at <= now."
        ),
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="blog_core_articles",
        verbose_name=_("author"),
    )
    secret_key = models.CharField(
        _("secret key"),
        max_length=64,
        default=_default_secret_key,
        editable=False,
        help_text=_("Opaque token for draft/scheduled preview URLs."),
    )
    view_count = models.PositiveIntegerField(_("view count"), default=0)
    metadata = models.JSONField(
        _("metadata"),
        default=dict,
        blank=True,
        help_text=_(
            "Forward-compatible attributes (e.g. future IP/fail2ban tags). "
            "Not used by core rendering."
        ),
    )
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)
    updated_at = models.DateTimeField(_("updated at"), auto_now=True)

    objects = ArticleManager()

    class Meta:
        ordering = ["-publish_at", "-pk"]
        unique_together = [("blog", "slug")]
        verbose_name = _("article")
        verbose_name_plural = _("articles")
        indexes = [
            models.Index(fields=["state", "publish_at"]),
        ]

    def __str__(self) -> str:
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)[:255] or uuid.uuid4().hex[:12]
        if not self.secret_key:
            self.secret_key = _default_secret_key()
        super().save(*args, **kwargs)

    @property
    def is_published(self) -> bool:
        return (
            self.state == self.STATE_PUBLISHED
            and self.publish_at is not None
            and self.publish_at <= timezone.now()
        )

    def get_absolute_url(self) -> str:
        from blog_core.conf import get_hookset

        return get_hookset().article_absolute_url(self)

    def get_preview_url(self) -> str:
        try:
            return reverse(
                "blog_core:article_preview",
                kwargs={
                    "blog_slug": self.blog.slug,
                    "slug": self.slug,
                    "secret_key": self.secret_key,
                },
            )
        except NoReverseMatch:
            return ""

    def render_body(self) -> str:
        from blog_core.conf import get_hookset

        return get_hookset().render_body(self)
