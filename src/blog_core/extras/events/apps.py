"""Application configuration for the ``[events]`` extra."""

from django.apps import AppConfig


class EventsConfig(AppConfig):
    """Domain-neutral ArticleEvent timeline, opt-in via INSTALLED_APPS."""

    name = "blog_core.extras.events"
    label = "blog_core_events"
    verbose_name = "Blog Core Events"
    default_auto_field = "django.db.models.BigAutoField"
