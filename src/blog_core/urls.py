"""URL patterns for blog_core list, detail, preview, and feeds."""

from django.urls import path

from blog_core.feeds import BlogArticleAtomFeed, BlogArticleFeed
from blog_core.views import (
    ArticleDetailView,
    ArticleListView,
    ArticlePreviewView,
)

app_name = "blog_core"

urlpatterns = [
    path(
        "<slug:blog_slug>/feed/rss/",
        BlogArticleFeed(),
        name="feed_rss",
    ),
    path(
        "<slug:blog_slug>/feed/atom/",
        BlogArticleAtomFeed(),
        name="feed_atom",
    ),
    path(
        "<slug:blog_slug>/preview/<slug:slug>/<str:secret_key>/",
        ArticlePreviewView.as_view(),
        name="article_preview",
    ),
    path(
        "<slug:blog_slug>/<slug:slug>/",
        ArticleDetailView.as_view(),
        name="article_detail",
    ),
    path(
        "<slug:blog_slug>/",
        ArticleListView.as_view(),
        name="article_list",
    ),
]
