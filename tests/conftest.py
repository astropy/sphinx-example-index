# Licensed under a 3-clause BSD style license - see LICENSE.rst

from typing import TYPE_CHECKING

try:
    from pytest_astropy_header.display import TESTED_VERSIONS
    ASTROPY_HEADER = True
except ImportError:
    ASTROPY_HEADER = False

if TYPE_CHECKING:
    from _pytest.config import Config


def pytest_configure(config: "Config") -> None:
    if ASTROPY_HEADER:
        config.option.astropy_header = True

        from sphinx_example_index import __version__
        TESTED_VERSIONS["sphinx_example_index"] = __version__
