"""RSS and Atom feeds via django.contrib.syndication."""

from __future__ import annotations

from django.contrib.syndication.views import Feed
from django.shortcuts import get_object_or_404
from django.utils.feedgenerator import Atom1Feed

from blog_core import conf
from blog_core.models import Article, Blog


class BlogArticleFeed(Feed):
    """RSS 2.0 feed of published articles for a blog."""

    title_template = None
    description_template = None

    def get_object(self, request, blog_slug: str):
        return get_object_or_404(Blog, slug=blog_slug, is_active=True)

    def title(self, obj: Blog) -> str:
        return conf.get_hookset().feed_title(obj)

    def link(self, obj: Blog) -> str:
        return obj.get_absolute_url()

    def description(self, obj: Blog) -> str:
        return conf.get_hookset().feed_description(obj)

    def items(self, obj: Blog):
        return (
            Article.objects.published()
            .filter(blog=obj)
            .select_related("author")[:50]
        )

    def item_title(self, item: Article) -> str:
        return item.title

    def item_description(self, item: Article) -> str:
        return item.teaser or item.title

    def item_link(self, item: Article) -> str:
        return item.get_absolute_url()

    def item_pubdate(self, item: Article):
        return item.publish_at

    def item_author_name(self, item: Article) -> str:
        if item.author_id and item.author:
            return item.author.get_username()
        return ""


class BlogArticleAtomFeed(BlogArticleFeed):
    """Atom 1.0 variant of :class:`BlogArticleFeed`."""

    feed_type = Atom1Feed
    subtitle = BlogArticleFeed.description
