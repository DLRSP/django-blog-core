# django-blog-core

[![CI/CD](https://github.com/DLRSP/django-blog-core/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-blog-core/actions/workflows/ci.yaml)
[![PyPI](https://img.shields.io/pypi/v/django-blog-core.svg)](https://pypi.org/project/django-blog-core/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Docs](https://img.shields.io/badge/docs-GitHub_Pages-blue)](https://dlrsp.github.io/django-blog-core/)
[![codecov](https://codecov.io/github/DLRSP/django-blog-core/coverage.svg?branch=main)](https://codecov.io/github/DLRSP/django-blog-core?branch=main)

Reusable **multi-blog** Django app: `Blog`, optional `Section`, and `Article`
with draft / scheduled / published / archived workflow, RSS + Atom feeds,
a Pinax-style **hookset**, secret preview URLs, and optional Markdown / HTML
sanitize extras.

> Status: **0.1.x** on PyPI. Extras `[search]`, `[tags]`, `[social]`,
> `[images]` are documented stubs.

## Install

```bash
pip install django-blog-core
pip install "django-blog-core[markdown]"   # Markdown bodies
pip install "django-blog-core[sanitize]"   # bleach HTML policy
pip install "django-blog-core[all]"        # markdown + sanitize
```

## Quickstart

```python
# settings.py
INSTALLED_APPS = [
    # ...
    "blog_core",
]

BLOG_CORE = {
    "PAGINATE_BY": 12,
    "SANITIZE_HTML": True,
    # "HOOKSET": "myapp.hooks.BlogHookSet",
}
# Or: BLOG_CORE_HOOKSET = "myapp.hooks.BlogHookSet"
```

```python
# urls.py
from django.urls import include, path

urlpatterns = [
    path("blog/", include("blog_core.urls")),
]
```

```bash
python manage.py migrate
python manage.py publish_scheduled_articles   # cron / host scheduler
```

Create a `Blog` and `Article` in admin. Public list/detail live at
`/blog/<blog-slug>/` and `/blog/<blog-slug>/<article-slug>/`. Feeds:

- `/blog/<blog-slug>/feed/rss/`
- `/blog/<blog-slug>/feed/atom/`

Preview drafts with the secret URL from the admin “Preview” column.

### Public visibility

`Article.objects.published()` (alias `public()`) is the single source of truth:

`state == "published"` **and** `publish_at <= now`.

### Hookset

Subclass `blog_core.hookset.DefaultBlogHookSet` to customize absolute URLs,
who may view non-public articles, body rendering, and feed titles — without
forking the package. Hooksets must not widen the public queryset.

### HTML / Markdown safety

- Markdown → HTML via the `[markdown]` extra.
- HTML (and Markdown output) is sanitized with bleach when `[sanitize]` is
  installed and `BLOG_CORE["SANITIZE_HTML"]` is true (default).
- Without bleach, HTML is escaped rather than passed through.
- Set `ALLOW_RAW_HTML = True` only if you accept XSS risk. See `docs/sanitize.md`.

### Extras

| Extra | Purpose |
|-------|---------|
| `[markdown]` | Markdown body rendering |
| `[sanitize]` | bleach allow-list |
| `[search]` | stub — Haystack/`published()` index patterns |
| `[tags]` | stub — tagging integration |
| `[social]` | stub — share matrix |
| `[images]` | stub — media attachments |

## Development

```bash
pip install -e ".[testing]"
pytest
# or: tox -e py313-django52
```

## License

MIT — see [LICENSE](LICENSE).
