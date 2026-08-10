"""QuerySet / Manager helpers for public article visibility."""

from __future__ import annotations

from django.db import models
from django.utils import timezone


class ArticleQuerySet(models.QuerySet):
    """Article queryset with the public visibility filter."""

    def published(self):
        """Public SSoT: ``state=published`` and ``publish_at <= now``."""
        now = timezone.now()
        return self.filter(
            state=self.model.STATE_PUBLISHED,
            publish_at__lte=now,
        )

    def public(self):
        """Alias of :meth:`published` (documented synonym)."""
        return self.published()

    def scheduled_due(self):
        """Articles in ``scheduled`` whose ``publish_at`` is due."""
        now = timezone.now()
        return self.filter(
            state=self.model.STATE_SCHEDULED,
            publish_at__lte=now,
        )


class ArticleManager(models.Manager.from_queryset(ArticleQuerySet)):
    """Default manager exposing :meth:`published` on the model class."""

    def published(self):
        return self.get_queryset().published()

    def public(self):
        return self.get_queryset().public()

    def scheduled_due(self):
        return self.get_queryset().scheduled_due()
