# django-blog-core

[![CI/CD](https://github.com/DLRSP/django-blog-core/actions/workflows/ci.yaml/badge.svg)](https://github.com/DLRSP/django-blog-core/actions/workflows/ci.yaml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reusable **multi-blog** Django app: `Blog`, optional `Section`, and `Article`
with draft / scheduled / published / archived workflow, RSS + Atom feeds,
a Pinax-style **hookset**, secret preview URLs, and optional Markdown / HTML
sanitize extras.

> Status: **0.1.0** — publish-ready core. Extras `[search]`, `[tags]`,
> `[social]`, `[images]` are documented stubs.

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

### Browser E2E

Package templates ship for reuse, but **browser E2E is deferred** until a
registry consumer installs the app and wires public URLs (no consumer dogfood
in this release). Module CI covers unit + Django Client/ORM/HTTP tests only.
When a consumer integrates, run that consumer’s Playwright suite
(`e2e_run.py --repo <consumer>`).

## License

MIT — see [LICENSE](LICENSE).
