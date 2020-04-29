# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The reStructuredText page generated for each example."""

__all__ = [
    "ExamplePage",
    "ExampleContentNode",
    "visit_example_content_html",
    "depart_example_content_html",
    "ExampleContentDirective",
]

import os
from typing import TYPE_CHECKING, List, Any

from docutils import nodes
from docutils.parsers.rst import Directive

from sphinx.util.logging import getLogger

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx_example_index.preprocessor import ExampleSource
    from sphinx_example_index.pages._renderer import Renderer
    from sphinx_example_index.pages._tagpage import TagPage


class ExamplePage:
    """A class that renders and represents a standalone example page in
    reStructuredText.

    Parameters
    ----------
    example_source : sphinx_astropy.ext.example.preprocessor.ExampleSource
        Object describing the source of the example.
    examples_dir : str
        The directory path where example pages are written.
    app : sphinx.application.Sphinx
        The Sphinx application instance.
    """

    def __init__(
        self, *, source: "ExampleSource", examples_dir: str, app: "Sphinx"
    ) -> None:
        self._example_source = source
        self._examples_dir = examples_dir
        self._app = app
        self._srcdir = app.srcdir
        self._tag_pages: "List[TagPage]" = []

    @property
    def source(self) -> "ExampleSource":
        """Metadata about the source of the example, a
        `sphinx_astropy.ext.example.preprocessor.ExampleSource` instance.`
        """
        return self._example_source

    def __str__(self) -> str:
        return "<ExamplePage {self.docref!r}>".format(self=self)

    def __repr__(self) -> str:
        return (
            "ExamplePage(source={self._example_source!r}, "
            "examples_dir={self._examples_dir!r}, "
            "app={self._app!r})"
        ).format(self=self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExamplePage):  # pragma: no cover
            return NotImplemented
        return self.source == other.source

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, ExamplePage):  # pragma: no cover
            return NotImplemented
        return self.source != other.source

    def __lt__(self, other: "ExamplePage") -> bool:
        return self.source < other.source

    def __le__(self, other: "ExamplePage") -> bool:
        return self.source <= other.source

    def __gt__(self, other: "ExamplePage") -> bool:
        return self.source > other.source

    def __ge__(self, other: "ExamplePage") -> bool:
        return self.source >= other.source

    @property
    def docname(self) -> str:
        """The docname of the standalone example page.

        The Sphinx docname is similar to the page's file path relative to the
        root of the source directory but does include the ``.rst`` extension.
        """
        return os.path.splitext(
            os.path.relpath(self.filepath, start=self._srcdir)
        )[0]

    @property
    def rel_docref(self) -> str:
        """The "relative docname" of the standalone example page relative to
        the "examples" directory.
        """
        return self.source.example_id

    @property
    def docref(self) -> str:
        """The "absolute docname" of the standalone example page, suitable for
        using with a ``doc`` referencing role.
        """
        return (
            "/"
            + os.path.splitext(
                os.path.relpath(self.filepath, start=self._srcdir)
            )[0]
        )

    @property
    def filepath(self) -> str:
        """The filesystem path where the reStructuredText file for the
        standalone example page is rendered.
        """
        return os.path.join(self._examples_dir, self.rel_docref + ".rst")

    def insert_tag_page(self, tag_page: "TagPage") -> None:
        """Associate a tag page with the example page.

        Typically this API is called by
        `sphinx_example_index.pages.TagPage.generate_tag_pages`, which
        simultaneously creates tag pages and associates eample pages with
        those tag pages.

        Parameters
        ----------
        tag_page : sphinx_example_index.pages.TagPage
            A tag page.

        See also
        --------
        tag_pages
        """
        self._tag_pages.append(tag_page)
        self._tag_pages.sort()

    @property
    def tag_pages(self) -> "List[TagPage]":
        """Sequence of tag pages
        (`sphinx_astropy.ext.examples.indexpages.TagPage`) associated with
        the example page.
        """
        return self._tag_pages

    def render(self, renderer: "Renderer") -> str:
        """Render the source for the standalone example page using a
        ``astropy_example/examplepage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.

        Returns
        -------
        content : str
            The content of the standalone example page.
        """
        context = {
            "title": self.source.title,
            "tag_pages": self.tag_pages,
            "example": self.source,
        }
        return renderer.render("example_index/examplepage.rst", context)

    def render_and_save(self, renderer: "Renderer") -> None:
        """Render the standalone example page and write it to `filepath`
        using the ``example_index/examplepage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.
        """
        content = self.render(renderer)
        with open(self.filepath, "w") as fh:
            fh.write(content)


class ExampleContentNode(nodes.container):
    """Docutils node that provides a placeholder for the content of an example.

    This node is inserted by the `ExampleContentDirective` directive.
    """


def visit_example_content_html(self: Any, node: ExampleContentNode) -> None:
    """HTML visitor for the `ExampleContentNode`.

    In HTML, marked up examples are wrapped in a ``<div>`` tag with a class
    of ``astropy-example-content``.
    """
    # The class is used by the HTML postprocessor to capture the HTML of
    # examples. The content of the div gets re-posted onto the stand-alone
    # example pages.
    self.body.append(self.starttag(node, "div", CLASS="example-index-content"))


def depart_example_content_html(self: Any, node: ExampleContentNode) -> None:
    """HTML departure handler for the `ExampleContentNode`.
    """
    self.body.append("</div>")


class ExampleContentDirective(Directive):
    """A directive that inserts an ExampleContentNode into the page to mark
    where the corresponding example content (from ``ExampleMarkerDirective``)
    is added in the HTML post-processing phase.

    Example:

    .. code-block:: rst

       .. example-content:: example-id

    The argument is the ID of the example.
    """

    _logger = getLogger(__name__)
    has_content = False
    required_arguments = 1  # example ID

    def run(self) -> List[nodes.Node]:
        self.env = self.state.document.settings.env
        self.example_id = self.arguments[0].strip()

        content_node = ExampleContentNode()
        # In docutils, the first item in 'ids' becomes the HTML id.
        content_node["ids"] = [self.example_id]

        return [content_node]
