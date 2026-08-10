"""Application configuration for django-blog-core."""

from django.apps import AppConfig


class BlogCoreConfig(AppConfig):
    """Multi-blog editorial articles with feeds and a pluggable hookset."""

    name = "blog_core"
    label = "blog_core"
    verbose_name = "Blog Core"
    default_auto_field = "django.db.models.BigAutoField"

    def ready(self) -> None:
        # Import conf early so defaults are validated at startup when accessed.
        from blog_core import conf  # noqa: F401
