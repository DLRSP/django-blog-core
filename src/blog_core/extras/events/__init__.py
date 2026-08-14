"""``[events]`` extra — domain-neutral Article timeline.

Install with ``pip install "django-blog-core[events]"`` and add
``"blog_core.extras.events"`` to ``INSTALLED_APPS`` to enable the
``ArticleEvent`` model and its migrations. Not loaded, and no table
created, unless the host opts in via ``INSTALLED_APPS``.

See docs/extras.md.
"""

FEATURE = "events"
STATUS = "implemented"
