# HTML sanitize policy

## Defaults

| Setting | Default | Meaning |
|---------|---------|---------|
| `SANITIZE_HTML` | `True` | Run output through the sanitize path |
| `ALLOW_RAW_HTML` | `False` | Skip sanitization (XSS risk) |

## With `[sanitize]` (bleach)

Allow-list in `blog_core.render`: common block/inline tags, `a[href|title|rel]`,
`img[src|alt|…]`, `http`/`https`/`mailto` protocols. Scripts and `javascript:`
URLs are stripped.

## Without bleach

If `SANITIZE_HTML` is true but bleach is not installed, HTML is **escaped**
(not passed through). Install `django-blog-core[sanitize]` for allow-list
cleaning of intentional HTML bodies.

## Markdown

`body_format=markdown` requires `[markdown]`. Output is then sanitized the same
way as HTML when `SANITIZE_HTML` is enabled.
