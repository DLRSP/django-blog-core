=========
Changelog
=========

.. towncrier release notes start

blog_core 0.1.4 (2026-08-14)
============================

Features
--------

- Add opt-in ``[events]`` extra with a domain-neutral ``ArticleEvent`` model
  (``article``, ``occurred_at``, ``label``, ``source``, ``source_id``,
  ``body``, ``metadata``) for per-article timelines. Enable by installing
  the extra and adding ``blog_core.extras.events`` to ``INSTALLED_APPS``;
  ``(source, source_id)`` is unique for idempotent re-import.


blog_core 0.1.3 (2026-08-14)
============================

No significant changes.


blog_core 0.1.2 (2026-08-11)
============================

No significant changes.


django-blog-core 0.1.1 (2026-08-10)
===================================

Bug Fixes
---------

- Install ``[markdown]`` and ``[sanitize]`` extras in the tox testenv so CI covers Markdown rendering and bleach sanitization.


Improved Documentation
----------------------

- Keep README and contributing docs adoption-facing; add Docs, PyPI, and coverage badges after first publish.
- Stop hard-coding the package version in the smoke test so releases do not fail the matrix on every bump.


django-blog-core 0.1.0 (2026-08-10)
===================================

Features
--------

- Initial public release: multi-blog models (Blog, Section, Article),
  ``published()`` manager, hookset, RSS/Atom feeds, ``publish_scheduled_articles``
  management command, admin UX, list/detail templates, Markdown/sanitize extras,
  and stubs for ``[search]``, ``[tags]``, ``[social]``, ``[images]``.
