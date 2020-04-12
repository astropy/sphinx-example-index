# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The sphinx-example-index Sphinx extension.

This extension adds an ``example`` directive to mark standalone example where
they appear in documentation. The extension builds an index of those examples
and also reproduces those examples on standalone pages.
"""

__all__ = ["__version__", "setup"]

from typing import TYPE_CHECKING, Any, Dict

from sphinx_example_index.version import version

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
    return {
        "version": __version__,
        # env_version needs to be incremented when the persisted data
        # formats of the extension change.
        "env_version": 1,
        "parallel_read_safe": True,
        "parallel_write_safe": True,
    }
