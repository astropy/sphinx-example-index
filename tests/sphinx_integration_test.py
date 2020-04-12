# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests that use the Sphinx pytest fixture to build a test case site and
permit inspection of the Sphinx application object.
"""

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from io import StringIO
    from sphinx.application import Sphinx


@pytest.mark.sphinx('html', testroot='example-index')
def test_setup(app: "Sphinx", status: "StringIO", warning: "StringIO") -> None:
    """Test that sphinx_example_index is set up by Sphinx and that all its
    features are added.
    """
    assert "sphinx_example_index" in app.extensions
