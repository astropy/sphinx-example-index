# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""The preprocessor detects examples in the reStructuredText source to prepare
their standalone example pages in the index.
"""

__all__ = [
    "EXAMPLE_PATTERN",
    "ExampleSource",
    "detect_examples",
]

import re
from typing import Iterator, Set, TYPE_CHECKING

from sphinx.util.logging import getLogger

from sphinx_example_index.identifiers import format_title_to_example_id

if TYPE_CHECKING:
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
