# Licensed under a 3-clause BSD style license - see LICENSE.rst
"""Utilities for managing and rendering page templates.

These utilities are based on sphinx.ext.autosummary, copyright 2007-2019 by the
Sphinx team.
"""

__all__ = ["Renderer", "Underliner"]

import os
from typing import TYPE_CHECKING, Dict, Any

from jinja2.sandbox import SandboxedEnvironment
from sphinx.jinja2glue import BuiltinTemplateLoader
from sphinx.util import rst

if TYPE_CHECKING:
    from sphinx.builders import Builder


class Underliner:
    """Jinja filter for underlining a line of text (to make a headline in
    reStructuredText).

    Parameters
    ----------
    character : str
        The character used for the underline. For example (``'#'``).
    """

    def __init__(self, character: str) -> None:
        if len(character) != 1:
            raise ValueError(
                "The underline must be a single character, "
                "got %r" % character
            )
        self._character = character

    def __call__(self, text: str) -> str:
        if "\n" in text:
            raise ValueError("Can only underline single lines")
        return text + "\n" + self._character * len(text)


class Renderer:
    """A class for managing and rendering page templates.

    Inspired by the AutosummaryRenderer in ``sphinx.ext.autosummary``.

    Parameters
    ----------
    builder : sphinx.builders.Builder
        The Sphinx builder. When using the ``builder``, the project's
        own templates (if available and configured via the ``templates_dir``
        configuration variable) are automatically preprended to the search
        path. This lets a user override this extension's own templates.
    h1_underline : str, optional
        Character for the underlines of titles.

    Notes
    -----
    This Jinja template renderer finds templates from two places, in this order
    of priority:

    1. If a project sets a ``templates_path`` configuration variable, this
       class uses templates found in the ``example_index`` subdirectory of
       that path.
    2. By default, this class uses templates built into this page.
       See the ``/src/data/templates/example_index`` path.
    """

    def __init__(
        self, builder: "Builder", h1_underline: str = "#",
    ):
        built_in_template_dirs = [
            os.path.join(os.path.dirname(__file__), "..", "data", "templates")
        ]
        print(built_in_template_dirs)
        loader = BuiltinTemplateLoader()
        loader.init(builder, dirs=built_in_template_dirs)

        self.env = SandboxedEnvironment(loader=loader)
        """The Jinja2 environment for rendering templates.
        """

        self.env.filters["escape"] = rst.escape
        self.env.filters["h1underline"] = Underliner(h1_underline)

    def render(self, template_name: str, context: Dict[str, Any]) -> str:
        """Render a template.

        Parameters
        ----------
        template_name : str
            Name of the template. This is a filename within the
            ``template_dir`` (see the contructor's parameters).
        context : dict
            Jinja rendering context
        """
        return self.env.get_template(template_name).render(context)
