"""SEC-HOOK / hookset customization tests."""

from django.test import override_settings

from blog_core.conf import get_hookset
from blog_core.hookset import DefaultBlogHookSet


class DenyAllHookSet(DefaultBlogHookSet):
    def can_view(self, request, article):
        return False


def test_default_hookset_allows_published(rf, published_article):
    hookset = DefaultBlogHookSet()
    assert hookset.can_view(rf.get("/"), published_article) is True


def test_default_hookset_denies_draft_anon(rf, draft_article):
    hookset = DefaultBlogHookSet()
    assert hookset.can_view(rf.get("/"), draft_article) is False


@override_settings(BLOG_CORE_HOOKSET="tests.test_hookset.DenyAllHookSet")
def test_custom_hookset_setting(published_article):
    hookset = get_hookset()
    assert isinstance(hookset, DenyAllHookSet)
    assert hookset.can_view(None, published_article) is False


def test_blog_core_hookset_in_dict(settings, published_article):
    settings.BLOG_CORE = {
        **getattr(settings, "BLOG_CORE", {}),
        "HOOKSET": "tests.test_hookset.DenyAllHookSet",
    }
    # Clear top-level override if present
    if hasattr(settings, "BLOG_CORE_HOOKSET"):
        delattr(settings, "BLOG_CORE_HOOKSET")
    hookset = get_hookset()
    assert isinstance(hookset, DenyAllHookSet)
