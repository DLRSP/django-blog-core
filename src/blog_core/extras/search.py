"""``[search]`` extra — Haystack / search-backend patterns (stub).

Intended contract (future):

* Index only ``Article.objects.published()``.
* Multi-field facets over title/teaser/body/section.
* Host chooses the backend (Whoosh, Elasticsearch, Xapian, …).

No hard dependency is declared in v0.1 — see docs/extras.md.
"""

FEATURE = "search"
STATUS = "stub"
