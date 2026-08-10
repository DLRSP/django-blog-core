# Getting started

## Install

```bash
pip install "django-blog-core[markdown,sanitize]"
```

## Configure

```python
INSTALLED_APPS = [..., "blog_core"]

BLOG_CORE = {
    "PAGINATE_BY": 12,
    "SANITIZE_HTML": True,
}
```

```python
urlpatterns = [
    path("blog/", include("blog_core.urls")),
]
```

```bash
python manage.py migrate
```

## Publish flow

1. Create a **Blog** in admin.
2. Create an **Article** (`draft` → `scheduled` or `published`).
3. Cron: `python manage.py publish_scheduled_articles`.
4. Public list: `/blog/<blog-slug>/`.
5. Feeds: `/blog/<blog-slug>/feed/rss/` and `.../atom/`.

`Article.objects.published()` is the public SSoT.
