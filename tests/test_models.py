"""Model and published-manager tests."""

from datetime import timedelta

from django.utils import timezone

from blog_core.models import Article, Blog, Section


def test_blog_slug_auto(db):
    blog = Blog.objects.create(name="Ops Notes")
    assert blog.slug == "ops-notes"


def test_section_unique_per_blog(db, blog):
    Section.objects.create(blog=blog, name="Announcements", slug="ann")
    other = Blog.objects.create(name="Other", slug="other")
    Section.objects.create(blog=other, name="Announcements", slug="ann")
    assert Section.objects.count() == 2


def test_published_excludes_draft_scheduled_future_archived(
    db, blog, user, published_article, draft_article
):
    future = Article.objects.create(
        blog=blog,
        title="Future",
        slug="future",
        state=Article.STATE_PUBLISHED,
        publish_at=timezone.now() + timedelta(days=1),
        author=user,
    )
    scheduled = Article.objects.create(
        blog=blog,
        title="Sched",
        slug="sched",
        state=Article.STATE_SCHEDULED,
        publish_at=timezone.now() - timedelta(minutes=5),
        author=user,
    )
    archived = Article.objects.create(
        blog=blog,
        title="Old",
        slug="old",
        state=Article.STATE_ARCHIVED,
        publish_at=timezone.now() - timedelta(days=30),
        author=user,
    )
    pub = list(Article.objects.published())
    assert published_article in pub
    assert draft_article not in pub
    assert future not in pub
    assert scheduled not in pub
    assert archived not in pub
    assert list(Article.objects.public()) == pub


def test_article_slug_unique_per_blog(db, blog, user):
    Article.objects.create(
        blog=blog,
        title="One",
        slug="same",
        state=Article.STATE_DRAFT,
        author=user,
    )
    other = Blog.objects.create(name="B2", slug="b2")
    Article.objects.create(
        blog=other,
        title="Two",
        slug="same",
        state=Article.STATE_DRAFT,
        author=user,
    )
    assert Article.objects.filter(slug="same").count() == 2


def test_metadata_json_default(db, blog, user):
    a = Article.objects.create(
        blog=blog, title="Meta", slug="meta", author=user, metadata={"ip": "x"}
    )
    a.refresh_from_db()
    assert a.metadata["ip"] == "x"
