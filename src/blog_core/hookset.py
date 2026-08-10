"""Pluggable hookset for URLs, render, and permissions.

Consumers subclass :class:`DefaultBlogHookSet` and point
``BLOG_CORE_HOOKSET`` (or ``BLOG_CORE["HOOKSET"]``) at the subclass.

Security contract: hookset methods must **not** widen the public queryset
beyond ``Article.objects.published()`` or bypass authentication checks for
draft/scheduled content.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from django.http import HttpRequest
from django.urls import NoReverseMatch, reverse

from blog_core import conf
from blog_core.render import render_article_body

if TYPE_CHECKING:
    from blog_core.models import Article, Blog


class DefaultBlogHookSet:
    """Default URL, render, and permission behaviour."""

    def blog_absolute_url(self, blog: "Blog") -> str:
        try:
            return reverse(
                "blog_core:article_list", kwargs={"blog_slug": blog.slug}
            )
        except NoReverseMatch:
            return f"/{blog.slug}/"

    def article_absolute_url(self, article: "Article") -> str:
        try:
            return reverse(
                "blog_core:article_detail",
                kwargs={
                    "blog_slug": article.blog.slug,
                    "slug": article.slug,
                },
            )
        except NoReverseMatch:
            return f"/{article.blog.slug}/{article.slug}/"

    def can_view(
        self, request: Optional[HttpRequest], article: "Article"
    ) -> bool:
        """Return True if the article may be shown to this request.

        Published articles are always viewable. Draft/scheduled/archived
        require staff (or authenticated author) unless a preview secret is used
        via the preview view (checked separately).
        """
        if article.is_published:
            return True
        if request is None:
            return False
        user = getattr(request, "user", None)
        if user is None or not user.is_authenticated:
            return False
        if user.is_staff or user.is_superuser:
            return True
        if article.author_id and article.author_id == user.pk:
            return True
        return False

    def can_preview_with_secret(
        self, article: "Article", secret_key: str
    ) -> bool:
        """Validate preview secret. Does not grant public listing."""
        return bool(secret_key) and secrets_equal(article.secret_key, secret_key)

    def render_body(self, article: "Article") -> str:
        cfg = conf.get_config()
        sanitize = bool(cfg.get("SANITIZE_HTML")) and not bool(
            cfg.get("ALLOW_RAW_HTML")
        )
        return render_article_body(
            article.body, article.body_format, sanitize=sanitize
        )

    def feed_title(self, blog: Optional["Blog"] = None) -> str:
        if blog is not None:
            return blog.name
        return "Blog"

    def feed_description(self, blog: Optional["Blog"] = None) -> str:
        if blog is not None:
            return blog.description or blog.name
        return "Articles"


def secrets_equal(left: str, right: str) -> bool:
    """Constant-time string compare for preview tokens."""
    import hmac

    return hmac.compare_digest(str(left), str(right))
