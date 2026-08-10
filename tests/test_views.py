"""HTTP list/detail/preview tests."""

import pytest
from django.urls import reverse


@pytest.mark.django_db
def test_list_shows_published_only(client, blog, published_article, draft_article):
    url = reverse("blog_core:article_list", kwargs={"blog_slug": blog.slug})
    resp = client.get(url)
    assert resp.status_code == 200
    body = resp.content.decode()
    assert published_article.title in body
    assert draft_article.title not in body


@pytest.mark.django_db
def test_detail_published(client, published_article):
    url = reverse(
        "blog_core:article_detail",
        kwargs={
            "blog_slug": published_article.blog.slug,
            "slug": published_article.slug,
        },
    )
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Hello" in resp.content.decode() or "Published" in resp.content.decode()


@pytest.mark.django_db
def test_detail_draft_404_anonymous(client, draft_article):
    url = reverse(
        "blog_core:article_detail",
        kwargs={
            "blog_slug": draft_article.blog.slug,
            "slug": draft_article.slug,
        },
    )
    assert client.get(url).status_code == 404


@pytest.mark.django_db
def test_preview_with_secret(client, draft_article):
    url = reverse(
        "blog_core:article_preview",
        kwargs={
            "blog_slug": draft_article.blog.slug,
            "slug": draft_article.slug,
            "secret_key": draft_article.secret_key,
        },
    )
    resp = client.get(url)
    assert resp.status_code == 200
    assert "Preview" in resp.content.decode()
    assert "Secret draft" in resp.content.decode()


@pytest.mark.django_db
def test_preview_wrong_secret_404(client, draft_article):
    url = reverse(
        "blog_core:article_preview",
        kwargs={
            "blog_slug": draft_article.blog.slug,
            "slug": draft_article.slug,
            "secret_key": "wrong-key-value-here",
        },
    )
    assert client.get(url).status_code == 404
