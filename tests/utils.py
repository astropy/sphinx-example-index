# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test utilities."""

__all__ = [
    "is_directive_registered",
    "is_node_registered",
    "Build",
]

from typing import NamedTuple

from docutils import nodes
from docutils.parsers.rst import directives


def is_directive_registered(name: str) -> bool:
    """Test if a directive is registered.

    This function is equivalent to
    `sphinx.util.docutils.is_directive_registered` that appears in
    Sphinx >= 2.0.

    Parameters
    ----------
    name : str
        Name of the directive.

    Returns
    -------
    bool
        `True` if the directive is loaded, `False` otherwise.
    """
    return name in directives._directives


def is_node_registered(node: nodes.Node) -> bool:
    """Test if a node is registered.

    This function is equivalent to `sphinx.util.docutils.is_node_registered`
    that appears in Sphinx >= 1.8.

    Parameters
    ----------
    node : docutils.nodes.Node
        A docutils node.

    Returns
    -------
    bool
        `True` if the node is loaded, `False` otherwise.
    """
    return hasattr(nodes.GenericNodeVisitor, "visit_" + node.__name__)


class Build(NamedTuple):
    """Build result."""

    src_dir: str
    build_dir: str
    status: int
