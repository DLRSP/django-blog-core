"""S06–S07 syndication feeds."""

from datetime import timedelta

import pytest
from django.urls import reverse
from django.utils import timezone

from blog_core.models import Article


@pytest.mark.django_db
def test_rss_excludes_non_public(client, blog, published_article, draft_article, user):
    Article.objects.create(
        blog=blog,
        title="Sched",
        slug="sched-feed",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() - timedelta(minutes=1),
        author=user,
    )
    url = reverse("blog_core:feed_rss", kwargs={"blog_slug": blog.slug})
    resp = client.get(url)
    assert resp.status_code == 200
    assert "application/rss+xml" in resp["Content-Type"] or "xml" in resp[
        "Content-Type"
    ]
    body = resp.content.decode()
    assert published_article.title in body
    assert draft_article.title not in body
    assert "Sched" not in body


@pytest.mark.django_db
def test_atom_feed_ok(client, blog, published_article):
    url = reverse("blog_core:feed_atom", kwargs={"blog_slug": blog.slug})
    resp = client.get(url)
    assert resp.status_code == 200
    assert "atom" in resp["Content-Type"] or "xml" in resp["Content-Type"]
    assert published_article.title in resp.content.decode()
