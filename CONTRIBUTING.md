# Contributing

1. Use a virtualenv and `pip install -e ".[testing,linting]"`.
2. Run `pytest` (or `tox -e py313-django52`).
3. Add a towncrier fragment under `news/` for user-visible changes.
4. Do not commit site-specific names into package code or docs.
