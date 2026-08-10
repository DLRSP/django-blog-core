# Security Policy

## Reporting a Vulnerability

Please report security issues privately to **dlrsp.dev@gmail.com** or via
GitHub Security Advisories. Do not open public issues for vulnerabilities.

## Threat model (django-blog-core)

- **XSS** — article bodies may contain HTML or Markdown-derived HTML. Default
  policy sanitizes with bleach when the `[sanitize]` extra is installed
  (`BLOG_CORE["SANITIZE_HTML"]=True`). Without bleach, HTML is escaped.
  `ALLOW_RAW_HTML=True` is an explicit site-accepted risk.
- **Draft / scheduled leakage** — public querysets use
  `Article.objects.published()` only. Preview URLs require the per-article
  `secret_key`. Hooksets must not widen public visibility.
- **Feeds** — RSS/Atom expose only published articles.
- **Secrets** — do not store credentials in `Article.metadata` or body text.
