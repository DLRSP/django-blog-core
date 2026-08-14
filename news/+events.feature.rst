Add opt-in ``[events]`` extra with a domain-neutral ``ArticleEvent`` model
(``article``, ``occurred_at``, ``label``, ``source``, ``source_id``,
``body``, ``metadata``) for per-article timelines. Enable by installing
the extra and adding ``blog_core.extras.events`` to ``INSTALLED_APPS``;
``(source, source_id)`` is unique for idempotent re-import.
