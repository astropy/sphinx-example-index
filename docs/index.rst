####################
sphinx-example-index
####################

Your Sphinx_ documentation pages contain a lot of information: overviews, examples, how-tos, and references.
Embedded within your documentation pages might be useful standalone content.
This content makes sense in the flow of your existing documentation, but it might also get lost.
The ``sphinx-example-index`` extension helps you to resurface content into easily-discovered standalone pages.

With this extension, all you need to do to create a standalone example is mark it up with an ``example`` directive, give it a title, and optionally tag it.
The extension will:

- Generate an HTML page for each example with a copy of the example's content from the original documentation page.
- Generate an index of all the examples.
- Generate an index page for each unique tag.

Getting started
===============

.. toctree::
   :maxdepth: 1

   changelog

Contributor's guide
===================

.. toctree::
   :maxdepth: 1

   development-guide
   api
