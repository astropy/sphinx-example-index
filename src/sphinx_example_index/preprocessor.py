# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The preprocessor detects examples in the reStructuredText source to prepare
their standalone example pages in the index.
"""

__all__ = [
    "EXAMPLE_PATTERN",
    "ExampleSource",
    "detect_examples",
    "preprocess_examples",
]

import os
import re
import shutil
from typing import Iterator, Set, TYPE_CHECKING

from sphinx.util.logging import getLogger

from sphinx_example_index.identifiers import format_title_to_example_id
from sphinx_example_index.pages import ExamplePage, TagPage, IndexPage, Renderer

if TYPE_CHECKING:
    from sphinx.application import Sphinx
    from sphinx.environment import BuildEnvironment


EXAMPLE_PATTERN = re.compile(
    # Match the example directive and title argument
    r"^\.\. example:: (?P<title>.+)\n"
    # Optionally match the tags option that follows
    # Note: this only works because there aren't other options.
    r"( +:tags: +(?P<tags>.+))?$",
    flags=re.MULTILINE,
)
"""This regular expression pattern matches ``example`` directives in the
reStructuredText content.

Named groups:

title
    The title of the example

tags
    The comma-separated tag list.

See also
--------
detect_examples
"""


def preprocess_examples(app: "Sphinx") -> None:
    """Preprocess the Sphinx project to detect examples and generate stub
    reStructuredText pages for each example and indexes of examples.

    This function is run as part of the ``builder-inited`` event.

    Parameters
    ----------
    app : `sphinx.application.Sphinx`
        The application instance.
    """
    logger = getLogger(__name__)
    config = app.config  # type: ignore

    if config.example_index_enabled is False:
        logger.debug("[sphinx_example_index] Skipping example index (disabled)")
        return

    logger.debug("[sphinx_example_index] Preprocessing example pages")

    # Create directory for example pages inside the documentation source dir.
    # Incrememental rebuilds of the example gallery aren't supported yet;
    # so for now the examples directory is cleared out before each rebuild.
    examples_dir = os.path.join(app.srcdir, config.example_index_dir)
    if os.path.isdir(examples_dir):
        shutil.rmtree(examples_dir)
    os.makedirs(examples_dir)

    renderer = Renderer(
        builder=app.builder, h1_underline=config.example_index_h1
    )

    example_pages = []
    example_docname_prefix = config.example_index_dir + "/"
    for docname in app.env.found_docs:
        if docname.startswith(example_docname_prefix):
            # Don't scan for examples in examples directory because those
            # docs were deleted at the start of this function.
            continue
        filepath = app.env.doc2path(docname)
        for detected_example in detect_examples(filepath, app.env):
            example_page = ExamplePage(
                source=detected_example, examples_dir=examples_dir, app=app
            )
            example_pages.append(example_page)
    example_pages.sort()

    # Generate and render tag pages first because doing so associates tags
    # with index pages.
    for tag_page in TagPage.generate_tag_pages(
        example_pages=example_pages, examples_dir=examples_dir, app=app
    ):
        tag_page.render_and_save(renderer)

    for example_page in example_pages:
        example_page.render_and_save(renderer)

    index_page = IndexPage(example_pages, examples_dir, app)
    index_page.render_and_save(renderer)


class ExampleSource:
    """Metadata about an example detected from a source file.

    Parameters
    ----------
    title : str
        The title of an example.
    docname : str
        The docname where the example originates from.
    tags : set of str
        The tags associated with the example.

    Notes
    -----
    ``ExampleSource`` objects can sort by title.
    """

    def __init__(self, *, title: str, docname: str, tags: Set[str]) -> None:
        self.title = title
        """The title of the example.
        """

        self.tags = tags
        """The tags associated with the example."""

        self.docname = docname
        """Docname of the page where the example comes from.
        """

        self.docref = "/" + docname
        """"Absolute docname" of the origin page, suitable for using with a
        ``doc`` referencing role.
        """

        self.example_id = format_title_to_example_id(self.title)
        """The unique ID of the example, based on the title.
        """

    def __repr__(self) -> str:
        return (
            "ExampleSource({self.title!r}, {self.docname!r},"
            " tags={self.tags!r})"
        ).format(self=self)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ExampleSource):  # pragma: no cover
            return NotImplemented
        return self.title == other.title

    def __ne__(self, other: object) -> bool:
        if not isinstance(other, ExampleSource):  # pragma: no cover
            return NotImplemented
        return self.title != other.title

    def __lt__(self, other: "ExampleSource") -> bool:
        return self.title < other.title

    def __le__(self, other: "ExampleSource") -> bool:
        return self.title <= other.title

    def __gt__(self, other: "ExampleSource") -> bool:
        return self.title > other.title

    def __ge__(self, other: "ExampleSource") -> bool:
        return self.title >= other.title


def detect_examples(
    filepath: str, env: "BuildEnvironment"
) -> Iterator[ExampleSource]:
    """Detect ``example`` directives from a source file by regular expression
    matching.

    Parameters
    ----------
    filepath : str
        A path to a source file.
    env : sphinx.environment.BuildEnvironment
        The build environment.

    Yields
    ------
    detected_example : DetectedExample
        An object containing metadata about an example.
    """
    logger = getLogger(__name__)

    with open(filepath, encoding="utf-8") as fh:
        text = fh.read()

    src_docname = env.path2doc(filepath)

    for m in EXAMPLE_PATTERN.finditer(text):
        title = m.group("title")
        if not title:
            logger.warning(
                "[sphinx_example_index] Could not parse example title from %s",
                m.group(0),
            )

        tag_option = m.group("tags")
        if tag_option:
            tags = set([t.strip() for t in tag_option.split(", ")])
        else:
            tags = set()

        yield ExampleSource(title=title, docname=src_docname, tags=tags)
