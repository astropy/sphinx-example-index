# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Test utilities."""

__all__ = [
    "is_directive_registered",
    "is_node_registered",
    "Build",
    "parse_example_page",
    "contains_href",
    "contains_external_href",
    "contains_linked_img",
]

import os

from typing import TYPE_CHECKING, NamedTuple

from bs4 import BeautifulSoup
from docutils import nodes
from docutils.parsers.rst import directives

if TYPE_CHECKING:
    from bs4 import Tree


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


def parse_example_page(build_dir: str, example_id: str) -> "Tree":
    """Parse an HTML page of a standalone example from an example site build.

    Parameters
    ----------
    example_build : tuple
        The build
    """
    path = os.path.join(build_dir, "examples", "{}.html".format(example_id))
    with open(path) as f:
        soup = BeautifulSoup(f, "html.parser")
    return soup


def contains_href(
    tree: "Tree",
    expected_href: str,
    selector: str = ".body a.reference.internal",
) -> bool:
    """Test if a BeautifulSoup tree contains an ``<a>`` with an expected
    href (optimized for Sphinx links with a ``reference internal`` class).

    Parameters
    ----------
    tree : bs4.Tree
        HTML content of a Sphinx page, parsed by BeautifulSoup.
    expected_href : str
        The expected href value of a tag on the page.
    selector : str
        The CSS selector for finding tags that might contain the expected href.
        The default selector is optimized to find ``<a>`` tags in the body of
        a Sphinx page with a ``reference internal``. For example, links
        made using the ``ref`` and ``doc`` roles.

    Returns
    -------
    contains : bool
        `True` if the link is found, `False` otherwise.
    """
    for atag in tree.select(selector):
        if atag["href"] == expected_href:
            return True
    return False


def contains_external_href(
    tree: "Tree",
    expected_href: str,
    selector: str = ".body a.reference.external",
) -> bool:
    """Test if a BeautifulSoup tree contains an ``<a>`` with an expected
    href (optimized for Sphinx links with a ``reference external`` class).

    Parameters
    ----------
    tree : bs4.Tree
        HTML content of a Sphinx page, parsed by BeautifulSoup.
    expected_href : str
        The expected href value of a tag on the page.
    selector : str
        The CSS selector for finding tags that might contain the expected href.
        The default selector is optimized to find ``<a>`` tags in the body of
        a Sphinx page with a ``reference internal``. For example, links
        made using intersphinx to other projects.

    Returns
    -------
    contains : bool
        `True` if the link is found, `False` otherwise.
    """
    return contains_href(tree, expected_href, selector=selector)


def contains_linked_img(
    tree: "Tree", expected_src: str, selector: str = ".body a.image-reference"
) -> bool:
    """Test if a BeautifulSoup tree contains an ``img`` tag with the expected
    src attribute that's also wrapped in an ``a`` tag.

    Parameters
    ----------
    soup : BeautifulSoup
        HTML content of a Sphinx page, parsed by BeautifulSoup.
    expected_src : str
        The expected src value of an ``img`` tag on the page (and the href
        value of the wrapping ``a`` tag).
    selector : str
        The CSS selector for finding ``<a>`` tags that wrap an image.

    Returns
    -------
    contains : bool
        `True` if the linked image is found, `False` otherwise.
    """
    for atag in tree.select(selector):
        # Check the href of both the <a> tag and the src of the <img> itself
        if atag["href"] == expected_src and atag.img["src"] == expected_src:
            return True
    return False
