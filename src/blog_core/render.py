"""Body rendering and optional HTML sanitization."""

from __future__ import annotations

from html import escape

from django.utils.safestring import mark_safe

# Conservative allow-list when bleach is available.
ALLOWED_TAGS = [
    "a",
    "abbr",
    "b",
    "blockquote",
    "br",
    "code",
    "em",
    "h1",
    "h2",
    "h3",
    "h4",
    "h5",
    "h6",
    "hr",
    "i",
    "img",
    "li",
    "ol",
    "p",
    "pre",
    "strong",
    "ul",
    "table",
    "thead",
    "tbody",
    "tr",
    "th",
    "td",
]
ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "rel"],
    "img": ["src", "alt", "title", "width", "height"],
    "*": ["class"],
}
ALLOWED_PROTOCOLS = ["http", "https", "mailto"]


def markdown_to_html(text: str) -> str:
    """Convert Markdown to HTML. Requires the ``markdown`` extra."""
    try:
        import markdown
    except (
        ImportError
    ) as exc:  # pragma: no cover - exercised when extra missing
        raise ImportError(
            "Markdown rendering requires the 'markdown' package. "
            "Install with: pip install 'django-blog-core[markdown]'"
        ) from exc
    return markdown.markdown(
        text or "",
        extensions=["extra", "sane_lists", "smarty"],
        output_format="html",
    )


def sanitize_html(html: str) -> str:
    """Sanitize HTML with bleach when installed; otherwise escape.

    Sites that set ``BLOG_CORE["ALLOW_RAW_HTML"] = True`` skip this path in the
    hookset. Without bleach, unknown HTML is escaped rather than passed through.
    """
    try:
        import bleach
    except ImportError:
        return escape(html or "")
    return bleach.clean(
        html or "",
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        protocols=ALLOWED_PROTOCOLS,
        strip=True,
    )


def render_article_body(body: str, body_format: str, *, sanitize: bool) -> str:
    """Return safe HTML for an article body."""
    if body_format == "markdown":
        html = markdown_to_html(body)
    else:
        html = body or ""
    if sanitize:
        html = sanitize_html(html)
    return mark_safe(html)
