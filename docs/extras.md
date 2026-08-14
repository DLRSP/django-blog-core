# Extras

| Extra | Status | Notes |
|-------|--------|-------|
| `markdown` | implemented | `markdown` package |
| `sanitize` | implemented | `bleach` |
| `search` | stub | Index `published()` only; host picks backend |
| `tags` | stub | Soft dep on host tag library |
| `social` | stub | Share matrix; secrets in host env |
| `images` | stub | Future media / image-primary format |
| `events` | implemented | Domain-neutral `ArticleEvent` timeline, opt-in app |

Stubs live under `blog_core.extras.*` for discoverability.

## `events`

`blog_core.extras.events` ships a domain-neutral `ArticleEvent` model: a
timestamped occurrence attached to an `Article` (`article`, `occurred_at`,
`label`, `source`, `source_id`, `body`, `metadata`). It carries no domain
vocabulary of its own, so a host can use it for any per-article timeline
(access log, webhook deliveries, audit trail, ...). `(source, source_id)`
is unique, so re-importing the same upstream record is idempotent.

The model and its migrations only load when the app is opted in:

```bash
pip install "django-blog-core[events]"
```

```python
INSTALLED_APPS = [
    ...,
    "blog_core",
    "blog_core.extras.events",
]
```

```bash
python manage.py migrate
```

```python
from blog_core.extras.events.models import ArticleEvent

ArticleEvent.objects.create(
    article=article,
    source="my-importer",
    source_id="42",
    label="example-tag",
    occurred_at=timestamp,
)
article.events.all()  # chronological timeline, oldest first
```
