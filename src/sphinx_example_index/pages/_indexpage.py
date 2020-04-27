# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""APIs for generating an index page of all examples.
"""

__all__ = ["IndexPage"]

import os
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx_example_index.pages._examplepage import ExamplePage
    from sphinx_example_index.pages import Renderer


class IndexPage:
    """A class that renders and represents the index page for an example
    index.

    Parameters
    ----------
    example_pages : list of sphinx_example_index.pages.ExampePage
        Sequence of example pages.
    examples_dir : str
        The directory path where example pages are written.
    app : sphinx.application.Sphinx
        The Sphinx application instance.
    """

    def __init__(
        self,
        example_pages: "List[ExamplePage]",
        examples_dir: str,
        app: "Sphinx",
    ) -> None:
        self._example_pages = example_pages
        self._examples_dir = examples_dir
        self._app = app
        self._srcdir = app.srcdir

    @property
    def docname(self) -> str:
        """The docname of the index page relative to the examples directory.
        """
        return "index"

    @property
    def docref(self) -> str:
        """The docref of the index page, for use with the ``doc`` role.
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
        index page is rendered.
        """
        return os.path.join(self._examples_dir, self.docname + ".rst")

    def render(self, renderer: "Renderer") -> str:
        """Render the source for the index page using a
        ``example_index/indexpage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.

        Returns
        -------
        content : str
            The content of the standalone example page.
        """
        context = {"example_pages": self._example_pages}
        return renderer.render("example_index/indexpage.rst", context)

    def render_and_save(self, renderer: "Renderer") -> None:
        """Render the landing page and write it to `filepath`
        using the ``example_index/indexpage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.
        """
        content = self.render(renderer)
        with open(self.filepath, "w") as fh:
            fh.write(content)
