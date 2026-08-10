"""Package smoke / extras stubs."""

from blog_core import VERSION, __version__
from blog_core.extras import images, search, social, tags


def test_version():
    assert __version__ == "0.1.0"
    assert VERSION[0] == 0


def test_extras_stubs():
    assert search.STATUS == "stub"
    assert tags.STATUS == "stub"
    assert social.STATUS == "stub"
    assert images.STATUS == "stub"
