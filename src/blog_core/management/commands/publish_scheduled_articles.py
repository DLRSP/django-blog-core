"""Promote due scheduled articles to published.

Intended for cron / ``SH_DjangoCommand``-style hosts::

    python manage.py publish_scheduled_articles
"""

from __future__ import annotations

from django.core.management.base import BaseCommand
from django.utils import timezone

from blog_core.models import Article


class Command(BaseCommand):
    help = "Publish articles whose state is scheduled and publish_at is due."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="Show how many articles would be published without updating.",
        )

    def handle(self, *args, **options):
        due = Article.objects.scheduled_due()
        count = due.count()
        if options["dry_run"]:
            self.stdout.write(
                self.style.WARNING(f"Would publish {count} article(s).")
            )
            return
        # Idempotent: only touch scheduled rows that are still due.
        updated = due.update(state=Article.STATE_PUBLISHED)
        self.stdout.write(
            self.style.SUCCESS(
                f"Published {updated} article(s) at {timezone.now().isoformat()}."
            )
        )
