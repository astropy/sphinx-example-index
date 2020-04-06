# Licensed under a 3-clause BSD style license - see LICENSE.rst

try:
    from pytest_astropy_header.display import TESTED_VERSIONS
    ASTROPY_HEADER = True
except ImportError:
    ASTROPY_HEADER = False


def pytest_configure(config):
    if ASTROPY_HEADER:
        config.option.astropy_header = True

        from sphinx_example_index import __version__
        TESTED_VERSIONS["sphinx_example_index"] = __version__
