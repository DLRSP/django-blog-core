"""S10–S11 markdown + sanitize render tests."""

import pytest
from django.test import override_settings

from blog_core.models import Article
from blog_core.render import markdown_to_html, sanitize_html


def test_markdown_to_html():
    html = markdown_to_html("# Title\n\nHello **world**")
    assert "<h1>" in html
    assert "<strong>world</strong>" in html


def test_sanitize_strips_script():
    dirty = '<p>ok</p><script>alert(1)</script><a href="javascript:alert(1)">x</a>'
    clean = sanitize_html(dirty)
    assert "<script>" not in clean
    assert "javascript:" not in clean
    assert "ok" in clean


@pytest.mark.django_db
@override_settings(BLOG_CORE={"SANITIZE_HTML": True, "ALLOW_RAW_HTML": False})
def test_article_render_html_sanitized(blog, user):
    article = Article.objects.create(
        blog=blog,
        title="XSS",
        slug="xss",
        body='<p>hi</p><script>alert(1)</script>',
        body_format=Article.BODY_HTML,
        state=Article.STATE_PUBLISHED,
        author=user,
    )
    html = article.render_body()
    assert "<script>" not in html
    assert "hi" in html


@pytest.mark.django_db
@override_settings(BLOG_CORE={"SANITIZE_HTML": True, "ALLOW_RAW_HTML": False})
def test_article_render_markdown(blog, user, published_article):
    html = published_article.render_body()
    assert "<h1>" in html or "Hello" in html
