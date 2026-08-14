"""``ArticleEvent`` — domain-neutral timeline child of ``Article``.

A row is one timestamped occurrence attached to an ``Article`` (e.g. one
row per detected access, alert, or external event). The model carries no
domain vocabulary of its own: ``label``, ``source`` and ``source_id`` are
free text supplied by the ingesting host, so the same shape works for any
timeline use case (fail2ban jail hits, webhook deliveries, audit trails,
...).
"""

from __future__ import annotations

from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from blog_core.models import Article


class ArticleEvent(models.Model):
    """A single timestamped occurrence on an :class:`Article` timeline."""

    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        related_name="events",
        verbose_name=_("article"),
    )
    occurred_at = models.DateTimeField(
        _("occurred at"),
        default=timezone.now,
        db_index=True,
        help_text=_(
            "When the underlying occurrence happened "
            "(not when this row was created)."
        ),
    )
    label = models.CharField(
        _("label"),
        max_length=200,
        blank=True,
        help_text=_(
            "Free-text label supplied by the ingesting host "
            "(e.g. a tag or category)."
        ),
    )
    source = models.CharField(
        _("source"),
        max_length=100,
        help_text=_(
            "Origin identifier for the event feed (e.g. an importer name)."
        ),
    )
    source_id = models.CharField(
        _("source id"),
        max_length=255,
        help_text=_(
            "Stable identifier from the source, used for idempotent "
            "re-import."
        ),
    )
    body = models.TextField(_("body"), blank=True)
    metadata = models.JSONField(_("metadata"), default=dict, blank=True)
    created_at = models.DateTimeField(_("created at"), auto_now_add=True)

    class Meta:
        ordering = ["occurred_at", "pk"]
        verbose_name = _("article event")
        verbose_name_plural = _("article events")
        constraints = [
            models.UniqueConstraint(
                fields=["source", "source_id"],
                name="blog_core_events_articleevent_source_uniq",
            ),
        ]
        indexes = [
            models.Index(fields=["article", "occurred_at"]),
        ]

    def __str__(self) -> str:
        return f"{self.source}:{self.source_id}"
