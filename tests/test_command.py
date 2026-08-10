"""S04–S05 publish_scheduled_articles command."""

from datetime import timedelta

from django.core.management import call_command
from django.utils import timezone

from blog_core.models import Article


def test_publish_scheduled_due(db, blog, user):
    due = Article.objects.create(
        blog=blog,
        title="Due",
        slug="due",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() - timedelta(minutes=1),
        author=user,
    )
    future = Article.objects.create(
        blog=blog,
        title="Later",
        slug="later",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() + timedelta(hours=2),
        author=user,
    )
    call_command("publish_scheduled_articles")
    due.refresh_from_db()
    future.refresh_from_db()
    assert due.state == Article.STATE_PUBLISHED
    assert future.state == Article.STATE_SCHEDULED


def test_publish_scheduled_idempotent(db, blog, user):
    Article.objects.create(
        blog=blog,
        title="Due2",
        slug="due2",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() - timedelta(minutes=1),
        author=user,
    )
    call_command("publish_scheduled_articles")
    call_command("publish_scheduled_articles")
    assert Article.objects.filter(state=Article.STATE_PUBLISHED).count() == 1


def test_publish_scheduled_dry_run(db, blog, user, capsys):
    Article.objects.create(
        blog=blog,
        title="Dry",
        slug="dry",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() - timedelta(minutes=1),
        author=user,
    )
    call_command("publish_scheduled_articles", dry_run=True)
    assert Article.objects.filter(state=Article.STATE_SCHEDULED).count() == 1
