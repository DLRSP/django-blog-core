"""Shared fixtures."""

from __future__ import annotations

from datetime import timedelta

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from blog_core.models import Article, Blog


@pytest.fixture
def user(db):
    User = get_user_model()
    return User.objects.create_user(username="author", password="x")


@pytest.fixture
def blog(db):
    return Blog.objects.create(
        name="News", slug="news", description="Site news"
    )


@pytest.fixture
def published_article(blog, user):
    return Article.objects.create(
        blog=blog,
        title="Hello World",
        slug="hello-world",
        teaser="A teaser",
        body="# Hello\n\nPublished body.",
        body_format=Article.BODY_MARKDOWN,
        state=Article.STATE_PUBLISHED,
        publish_at=timezone.now() - timedelta(hours=1),
        author=user,
    )


@pytest.fixture
def draft_article(blog, user):
    return Article.objects.create(
        blog=blog,
        title="Draft Piece",
        slug="draft-piece",
        body="Secret draft",
        body_format=Article.BODY_HTML,
        state=Article.STATE_DRAFT,
        publish_at=timezone.now(),
        author=user,
    )
