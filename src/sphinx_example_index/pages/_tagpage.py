# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""APIs for generating index pages for tags.
"""

__all__ = ["TagPage"]

import os
from typing import TYPE_CHECKING, List, Iterator

from docutils import nodes

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx_example_index.pages._examplepage import ExamplePage
    from sphinx_example_index.pages import Renderer


class TagPage:
    """A class that renders and represents the index page for a tagged
    set of examples.

    Parameters
    ----------
    tag_name : str
        The tag that this page corresponds to
    example_pages : list of sphinx_example_index.pages.ExampePage
        Sequence of example pages.
    examples_dir : str
        The directory path where example pages are written.
    app : sphinx.application.Sphinx
        The Sphinx application instance.
    """

    def __init__(
        self,
        *,
        name: str,
        example_pages: "List[ExamplePage]",
        examples_dir: str,
        app: "Sphinx",
    ) -> None:
        self.name = name
        self._examples_dir = examples_dir
        self._app = app
        self._srcdir = app.srcdir

        # Process example pages to get all examples with this tag;
        # also insert a reference to this tag page into that example page
        # so it can link to the tag index page.
        self._example_pages = []
        for example_page in example_pages:
            if name in example_page.source.tags:
                self._example_pages.append(example_page)
                example_page.insert_tag_page(self)

    @classmethod
    def generate_tag_pages(
        cls,
        *,
        example_pages: "List[ExamplePage]",
        examples_dir: str,
        app: "Sphinx",
    ) -> "Iterator[TagPage]":
        """Construct `TagPage` instances for all tags associated with a
        sequence of ExamplePage instances.

        Simultaneously, this constructor also associates `TagPage` instances
        with `ExamplePage` instances
        (`sphinx_astropy.ext.example.examplepages.ExamplePage.tag_pages`).

        Parameters
        ----------
        example_pages : sequence of ExamplePage
            Example pages.
        examples_dir : str
            The directory path where example pages are written.
        app : sphinx.application.Sphinx
            The Sphinx application instance.

        Yields
        ------
        tag_page : TagPage
            A tag index page.
        """
        tag_set = set()
        for example_page in example_pages:
            tag_set.update(example_page.source.tags)
        tag_names = list(tag_set)
        tag_names.sort()
        for tag_name in tag_names:
            yield cls(
                name=tag_name,
                example_pages=example_pages,
                examples_dir=examples_dir,
                app=app,
            )

    def __str__(self) -> str:
        return "<TagPage {self.docref!r}>".format(self=self)

    def __repr__(self) -> str:
        return (
            "TagPage({self.name!r}, {self._example_pages!r}, "
            "{self._examples_dir!r}, {self._srcdir!r})"
        ).format(self=self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TagPage):  # pragma: no cover
            return NotImplemented
        return self.name == other.name

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, TagPage):  # pragma: no cover
            return NotImplemented
        return self.name != other.name

    def __lt__(self, other: "TagPage") -> bool:
        return self.name < other.name

    def __le__(self, other: "TagPage") -> bool:
        return self.name <= other.name

    def __gt__(self, other: "TagPage") -> bool:
        return self.name > other.name

    def __ge__(self, other: "TagPage") -> bool:
        return self.name >= other.name

    @property
    def tag_id(self) -> str:
        """The URL-safe ID of the tag.
        """
        return nodes.make_id(self.name)

    @property
    def example_pages(self) -> "Iterator[ExamplePage]":
        """Iterator over ExamplePage instances tagged with this tag.
        """
        for example in self._example_pages:
            yield example

    @property
    def docname(self) -> str:
        """The docname of the tag page relative to the examples directory.
        """
        return "tags/{self.tag_id}".format(self=self)

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
        tag page is rendered.
        """
        return os.path.join(self._examples_dir, self.docname + ".rst")

    def render(self, renderer: "Renderer") -> str:
        """Render the source for the tag page using a
        ``example_index/tagpage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.

        Returns
        -------
        content : str
            The content of the tag page.
        """
        context = {
            "tag": self,
            "title": "Examples tagged {self.name}".format(self=self),
        }
        return renderer.render("example_index/tagpage.rst", context)

    def render_and_save(self, renderer: "Renderer") -> None:
        """Render the tag page and write it to `filepath`
        using the ``astropy_example/tagpage.rst`` template.

        Parameters
        ----------
        renderer : sphinx_example_index.pages.Renderer
            The Jinja template renderer.
        """
        content = self.render(renderer)
        os.makedirs(os.path.dirname(self.filepath), exist_ok=True)
        with open(self.filepath, "w") as fh:
            fh.write(content)
