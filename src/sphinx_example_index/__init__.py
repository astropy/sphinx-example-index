# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The sphinx-example-index Sphinx extension.

This extension adds an ``example`` directive to mark standalone example where
they appear in documentation. The extension builds an index of those examples
and also reproduces those examples on standalone pages.
"""

__all__ = ["__version__", "setup"]

from typing import TYPE_CHECKING, Any, Dict

from sphinx_example_index.version import version

from sphinx_example_index.marker import (
    ExampleMarkerNode,
    visit_example_marker_html,
    depart_example_marker_html,
    ExampleMarkerDirective,
)
from sphinx_example_index.preprocessor import preprocess_examples
from sphinx_example_index.pages import (
    ExampleContentNode,
    visit_example_content_html,
    depart_example_content_html,
    ExampleContentDirective,
)

if TYPE_CHECKING:
    from sphinx.application import Sphinx

__version__ = version


def setup(app: "Sphinx") -> Dict[str, Any]:
    """Set up the sphinx-example-index Sphinx extension.

    Parameters
    ----------
    app : sphinx.application.Sphinx
        The Sphinx application.

    Returns
    -------
    metadata : dict
        Dictionary with extension metadata. See
        http://www.sphinx-doc.org/en/master/extdev/index.html#extension-metadata
        for more information.
    """
    app.add_node(
        ExampleMarkerNode,
        html=(visit_example_marker_html, depart_example_marker_html),
    )
    app.add_node(
        ExampleContentNode,
        html=(visit_example_content_html, depart_example_content_html),
    )

    app.add_directive("example", ExampleMarkerDirective)
    app.add_directive("example-content", ExampleContentDirective)

    app.connect("builder-inited", preprocess_examples)

    # Toggles the gallery generation on or off.
    app.add_config_value("example_index_enabled", False, "env")

    # Configures the directory, relative to the documentation source root,
    # where example pages are created.
    app.add_config_value("example_index_dir", "examples", "env")

    # Configures the character to use for h1 underlines in rst
    app.add_config_value("example_index_h1", "#", "env")

    return {
        "version": __version__,
        # env_version needs to be incremented when the persisted data
        # formats of the extension change.
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
