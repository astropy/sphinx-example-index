# -*- coding: utf-8 -*-
# Licensed under a 3-clause BSD style license - see LICENSE.rst
#
# Sphinx documentation build configuration file.
#
# This file is execfile()d with the current directory set to its containing dir.

import datetime
import os
import sys

if sys.version_info < (3, 8):
    import importlib_metadata
else:
    import importlib.metadata as importlib_metadata

import astropy_sphinx_theme


# Packaging metadata
pkg_metadata = importlib_metadata.metadata('sphinx-example-index')

# -- General configuration ----------------------------------------------------

# This is added to the end of RST files - a good place to put substitutions to
# be used globally.
rst_epilog = """

.. _Astropy: https://www.astropy.org
"""

# Configuration for intersphinx
intersphinx_mapping = {
    'python': ('https://docs.python.org/3/',
               (None, 'http://data.astropy.org/intersphinx/python3.inv')),
}

# By default, highlight as Python 3.
highlight_language = 'python3'

# If your documentation needs a minimal Sphinx version, state it here.
needs_sphinx = '1.7'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', '_templates']

# The master toctree document.
master_doc = 'index'

# The reST default role (used for this markup: `text`) to use for all
# documents. Set to the "smart" one.
default_role = 'obj'

# -- Sphinx extensions --------------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
    'sphinx.ext.inheritance_diagram',
    'sphinx.ext.viewcode',
    'numpydoc',
    'sphinx_automodapi.automodapi',
    'sphinx_automodapi.smart_resolver',
]

# -- Project information ------------------------------------------------------

# This does not *have* to match the package name, but typically does
project = pkg_metadata.get('Name')
author = pkg_metadata.get('Author')
copyright = '{0}, {1}'.format(
    datetime.datetime.now().year, author)

# The version info for the project you're documenting, acts as replacement for
# |version| and |release|, also used in various other places throughout the
# built documents.

# The full version, including alpha/beta/rc tags.
release = pkg_metadata.get('Version', '0.0.0')
# The short X.Y version.
version = release.split('-', 1)[0]


# -- Options for HTML output --------------------------------------------------

html_theme = 'bootstrap-astropy'

html_sidebars = {
    '**': ['localtoc.html'],
    'search': [],
    'genindex': [],
    'py-modindex': []
}

html_theme_options = {
    'logotext1': 'sphinx-example-index',  # white,  semi-bold
    'logotext2': '',  # orange, light
    'logotext3': ':docs'   # white,  light
}

# We include by default the favicon that is in the bootstrap-astropy theme.
html_theme_path = astropy_sphinx_theme.get_html_theme_path()
html_favicon = os.path.join(html_theme_path[0], html_theme, 'static', 'astropy_logo.ico')

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = '{0} v{1}'.format(project, release)

# If not '', a 'Last updated on:' timestamp is inserted at every page bottom,
# using the given strftime format.
html_last_updated_fmt = '%d %b %Y'

# Output file base name for HTML help builder.
htmlhelp_basename = project + 'doc'


# -- Options for the linkcheck builder ----------------------------------------

# A timeout value, in seconds, for the linkcheck builder
linkcheck_timeout = 60


# -- Options for LaTeX output -------------------------------------------------

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [('index', project + '.tex', project + u' Documentation',
                    author, 'manual')]

# For "manual" documents, if this is true, then toplevel headings are parts,
# not chapters.
latex_toplevel_sectioning = 'part'

latex_elements = {}

# Additional stuff for the LaTeX preamble.
latex_elements['preamble'] = r"""
% Use a more modern-looking monospace font
\usepackage{inconsolata}
% The enumitem package provides unlimited nesting of lists and enums.
% Sphinx may use this in the future, in which case this can be removed.
% See https://bitbucket.org/birkenfeld/sphinx/issue/777/latex-output-too-deeply-nested
\usepackage{enumitem}
\setlistdepth{15}
% In the parameters section, place a newline after the Parameters
% header.  (This is stolen directly from Numpy's conf.py, since it
% affects Numpy-style docstrings).
\usepackage{expdlist}
\let\latexdescription=\description
\def\description{\latexdescription{}{} \breaklabel}
% Support the superscript Unicode numbers used by the "unicode" units
% formatter
\DeclareUnicodeCharacter{2070}{\ensuremath{^0}}
\DeclareUnicodeCharacter{00B9}{\ensuremath{^1}}
\DeclareUnicodeCharacter{00B2}{\ensuremath{^2}}
\DeclareUnicodeCharacter{00B3}{\ensuremath{^3}}
\DeclareUnicodeCharacter{2074}{\ensuremath{^4}}
\DeclareUnicodeCharacter{2075}{\ensuremath{^5}}
\DeclareUnicodeCharacter{2076}{\ensuremath{^6}}
\DeclareUnicodeCharacter{2077}{\ensuremath{^7}}
\DeclareUnicodeCharacter{2078}{\ensuremath{^8}}
\DeclareUnicodeCharacter{2079}{\ensuremath{^9}}
\DeclareUnicodeCharacter{207B}{\ensuremath{^-}}
\DeclareUnicodeCharacter{00B0}{\ensuremath{^{\circ}}}
\DeclareUnicodeCharacter{2032}{\ensuremath{^{\prime}}}
\DeclareUnicodeCharacter{2033}{\ensuremath{^{\prime\prime}}}
% Make the "warning" and "notes" sections use a sans-serif font to
% make them stand out more.
\renewenvironment{notice}[2]{
  \def\py@noticetype{#1}
  \csname py@noticestart@#1\endcsname
  \textsf{\textbf{#2}}
}{\csname py@noticeend@\py@noticetype\endcsname}
"""


# -- Options for manual page output -------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [('index', project.lower(), project + u' Documentation',
              [author], 1)]

# -- Turn on nitpicky mode for sphinx (to warn about references not found) ----
#
# nitpicky = True
# nitpick_ignore = []
#
# Some warnings are impossible to suppress, and you can list specific references
# that should be ignored in a nitpick-exceptions file which should be inside
# the docs/ directory. The format of the file should be:
#
# <type> <class>
#
# for example:
#
# py:class astropy.io.votable.tree.Element
# py:class astropy.io.votable.tree.SimpleElement
# py:class astropy.io.votable.tree.SimpleElementWithContent
#
# Uncomment the following lines to enable the exceptions:
#
# for line in open('nitpick-exceptions'):
#     if line.strip() == "" or line.startswith("#"):
#         continue
#     dtype, target = line.split(None, 1)
#     target = target.strip()
#     nitpick_ignore.append((dtype, six.u(target)))

# -- Numpydoc and automodapi extension configuration --------------------------

# Don't show summaries of the members in each class along with the
# class' docstring
numpydoc_show_class_members = False

autosummary_generate = True

automodapi_toctreedirnm = 'api'

# Class documentation should contain *both* the class docstring and
# the __init__ docstring
autoclass_content = "both"

# Render inheritance diagrams in SVG
graphviz_output_format = "svg"

graphviz_dot_args = [
    '-Nfontsize=10',
    '-Nfontname=Helvetica Neue, Helvetica, Arial, sans-serif',
    '-Efontsize=10',
    '-Efontname=Helvetica Neue, Helvetica, Arial, sans-serif',
    '-Gfontsize=10',
    '-Gfontname=Helvetica Neue, Helvetica, Arial, sans-serif'
]
