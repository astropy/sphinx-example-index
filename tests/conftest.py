# Licensed under a 3-clause BSD style license - see LICENSE.rst

from typing import TYPE_CHECKING

import pytest
from sphinx.testing.path import path

try:
    from pytest_astropy_header.display import TESTED_VERSIONS

    ASTROPY_HEADER = True
except ImportError:
    ASTROPY_HEADER = False

if TYPE_CHECKING:
    from _pytest.config import Config


# Exclude 'cases' dirs for pytest test collector
collect_ignore = ["cases"]

# Add Sphinx's internal pytest plugin for running a Sphinx build via a fixture.
pytest_plugins = ("sphinx.testing.fixtures",)


def pytest_configure(config: "Config") -> None:
    if ASTROPY_HEADER:
        config.option.astropy_header = True

        from sphinx_example_index import __version__

        TESTED_VERSIONS["sphinx_example_index"] = __version__

    config.addinivalue_line(
        "markers", "sphinx(builder, testroot='name'): Run sphinx on a site"
    )


@pytest.fixture(scope="session")
def rootdir() -> path:
    """Directory containing Sphinx projects for testing.

    This fixture, ``rootdir``, is needed by the ``pytest.mark.sphinx`` mark.
    Internal users can use the `casesdir` fixture instead for more canonical
    terminology.
    """
    return path(__file__).parent.abspath() / "cases"


@pytest.fixture(scope="session")
def casesdir(rootdir: path) -> path:
    """Directory containing Sphinx projects for testing."""
    return rootdir
