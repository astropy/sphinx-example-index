# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The reStructuredText page generated for each example."""

__all__ = ["ExamplePage"]

import os
from typing import TYPE_CHECKING, List

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
