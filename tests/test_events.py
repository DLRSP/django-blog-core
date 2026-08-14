"""``[events]`` extra: ArticleEvent creation, uniqueness, ordering."""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.db import IntegrityError
from django.utils import timezone

from blog_core.extras.events.models import ArticleEvent


def test_create_event_for_article(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline", author=user
    )
    event = ArticleEvent.objects.create(
        article=article,
        source="importer",
        source_id="1",
        label="example-tag",
    )
    assert event.article == article
    assert article.events.count() == 1
    assert str(event) == "importer:1"


def test_source_and_source_id_unique_together(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline-2", author=user
    )
    ArticleEvent.objects.create(article=article, source="importer", source_id="dup")
    with pytest.raises(IntegrityError):
        ArticleEvent.objects.create(
            article=article, source="importer", source_id="dup"
        )


def test_same_source_id_allowed_across_different_sources(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline-3", author=user
    )
    ArticleEvent.objects.create(article=article, source="pinax", source_id="42")
    ArticleEvent.objects.create(article=article, source="maildir", source_id="42")
    assert article.events.count() == 2


def test_default_ordering_by_occurred_at(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline-4", author=user
    )
    now = timezone.now()
    newest = ArticleEvent.objects.create(
        article=article,
        source="importer",
        source_id="newest",
        occurred_at=now,
    )
    oldest = ArticleEvent.objects.create(
        article=article,
        source="importer",
        source_id="oldest",
        occurred_at=now - timedelta(days=1),
    )
    middle = ArticleEvent.objects.create(
        article=article,
        source="importer",
        source_id="middle",
        occurred_at=now - timedelta(hours=12),
    )
    assert list(article.events.all()) == [oldest, middle, newest]


def test_metadata_defaults_to_empty_dict(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline-5", author=user
    )
    event = ArticleEvent.objects.create(
        article=article, source="importer", source_id="meta"
    )
    assert event.metadata == {}


def test_article_delete_cascades_to_events(db, blog, user):
    from blog_core.models import Article

    article = Article.objects.create(
        blog=blog, title="Timeline", slug="timeline-6", author=user
    )
    ArticleEvent.objects.create(article=article, source="importer", source_id="cascade")
    article.delete()
    assert ArticleEvent.objects.filter(source="importer", source_id="cascade").count() == 0
