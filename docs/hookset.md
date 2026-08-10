# Hookset

Pinax-style customization without forking.

```python
# myapp/hooks.py
from blog_core.hookset import DefaultBlogHookSet

class BlogHookSet(DefaultBlogHookSet):
    def article_absolute_url(self, article):
        return f"/writing/{article.blog.slug}/{article.slug}/"
```

```python
BLOG_CORE_HOOKSET = "myapp.hooks.BlogHookSet"
# or BLOG_CORE = {"HOOKSET": "myapp.hooks.BlogHookSet"}
```

Override points: `blog_absolute_url`, `article_absolute_url`, `can_view`,
`can_preview_with_secret`, `render_body`, `feed_title`, `feed_description`.

**Security:** do not widen public visibility beyond `published()` or bypass
authz for drafts.
