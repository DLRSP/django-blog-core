"""django-blog-core — reusable multi-blog Django application.

See PEP 386 (https://peps.python.org/pep-0386/).
"""

__version__ = "0.1.2"
__version_info__ = tuple(
    int(i) if i.isdigit() else i for i in __version__.split(".")
)
__license__ = "MIT"
__title__ = "django-blog-core"

__author__ = "DLRSP"
__copyright__ = "Copyright 2010-present DLRSP"

# Version synonym
VERSION = __version_info__
