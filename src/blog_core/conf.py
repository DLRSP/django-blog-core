"""Settings access layer for django-blog-core.

Configuration is driven by a ``BLOG_CORE`` dict in Django settings. The hookset
may also be set via top-level ``BLOG_CORE_HOOKSET`` (dotted path), which wins
over ``BLOG_CORE["HOOKSET"]``.

Example::

    BLOG_CORE = {
        "HOOKSET": "myapp.hooks.BlogHookSet",
        "PAGINATE_BY": 10,
        "SANITIZE_HTML": True,
        "ALLOW_RAW_HTML": False,
    }
"""

from __future__ import annotations

from typing import Any, Dict

from django.conf import settings
from django.utils.module_loading import import_string

SETTING_NAME = "BLOG_CORE"
HOOKSET_SETTING = "BLOG_CORE_HOOKSET"

DEFAULTS: Dict[str, Any] = {
    # Dotted path to a BlogHookSet subclass, or None for the package default.
    "HOOKSET": "blog_core.hookset.DefaultBlogHookSet",
    "PAGINATE_BY": 12,
    # When True and bleach is installed, HTML bodies (and Markdown output) are
    # sanitized before display. See docs/sanitize.md.
    "SANITIZE_HTML": True,
    # When True, skip bleach even if installed (site accepts XSS risk).
    "ALLOW_RAW_HTML": False,
    # Optional default blog slug used by URL patterns without a blog kwarg.
    "DEFAULT_BLOG_SLUG": None,
}


def get_config() -> Dict[str, Any]:
    """Return merged configuration (defaults + user overrides)."""
    user_config = getattr(settings, SETTING_NAME, None) or {}
    return {**DEFAULTS, **user_config}


def get_setting(key: str, default: Any = None) -> Any:
    """Return a single merged setting value."""
    return get_config().get(key, default)


def get_hookset():
    """Resolve and return the configured hookset instance."""
    # Top-level BLOG_CORE_HOOKSET wins when set.
    dotted = getattr(settings, HOOKSET_SETTING, None)
    if not dotted:
        dotted = get_setting("HOOKSET")
    if not dotted:
        from blog_core.hookset import DefaultBlogHookSet

        return DefaultBlogHookSet()
    if isinstance(dotted, type):
        return dotted()
    cls = import_string(dotted)
    return cls() if isinstance(cls, type) else cls
