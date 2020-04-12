# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Tests that use the Sphinx pytest fixture to build a test case site and
permit inspection of the Sphinx application object.
"""

import os
from typing import TYPE_CHECKING

import pytest
from sphinx.util import logging
from bs4 import BeautifulSoup

from tests.utils import is_directive_registered, is_node_registered

from sphinx_example_index.marker import ExampleMarkerNode, EXAMPLE_SRC_DIV_CLASS

if TYPE_CHECKING:
    from io import StringIO
    from sphinx.application import Sphinx


@pytest.mark.sphinx("html", testroot="example-index")
def test_setup(app: "Sphinx", status: "StringIO", warning: "StringIO") -> None:
    """Test that sphinx_example_index is set up by Sphinx and that all its
    features are added.
    """
    assert "sphinx_example_index" in app.extensions

    # Check registered directives
    assert is_directive_registered("example")

    # Check registered nodes
    assert is_node_registered(ExampleMarkerNode)


@pytest.mark.sphinx("html", testroot="example-index")
def test_example_directive_targets(
    app: "Sphinx", status: "StringIO", warning: "StringIO"
) -> None:
    """Test that the example directive creates target nodes with the
    appropriate Ids.
    """
    app.verbosity = 2
    logging.setup(app, status, warning)
    app.builder.build_all()

    with open(os.path.join(app.outdir, "page-with-examples.html")) as f:
        soup = BeautifulSoup(f, "html.parser")

    known_target_refids = [
        "example-src-example-with-two-paragraphs",
        "example-src-tagged-example",
        "example-src-example-with-multiple-tags",
        "example-src-example-with-subsections",
    ]
    for known_target_refid in known_target_refids:
        divs = soup.find_all("div", id=known_target_refid)
        assert len(divs)
        assert EXAMPLE_SRC_DIV_CLASS in divs[0]["class"]
