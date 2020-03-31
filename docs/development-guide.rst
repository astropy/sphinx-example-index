##################
Developement Guide
##################

``sphinx-example-index`` is open source software and we welcome contributions of all kinds.
If you're interested in working on ``sphinx-example-index``\ ’s code and documentation, this page will help you get oriented with our development process and conventions.

Setting Up a Development Environment
====================================

Installation for Development
----------------------------

First, create a fork of the https://github.com/astropy/sphinx-example-index repository.
Then, clone your fork to your own computer.
For more information about GitHub-based development, see the `GitHub help pages on working with forks <https://help.github.com/en/github/collaborating-with-issues-and-pull-requests/working-with-forks>`__.

Next, set up a Python virtual environment for your local ``sphinx-example-index`` development.
See `Astropy's documentation on Python virtual environments <http://docs.astropy.org/en/latest/development/workflow/virtual_pythons.html#virtual-envs>`__ for help if you haven't done this before.

Finally, from the root of your cloned ``sphinx-example-index`` repository, install the package with development extras, along with the tox_ automation package:

.. code-block:: bash

   python -m pip install -e ".[test,docs]"
   python -m pip install tox

Run Tests with tox
------------------

You can run tests against the latest release of Sphinx, as well as validate code style by running tox_:

.. code-block:: bash

   tox -e py-test-cov,codestyle

That command uses your computer's default version of Python.

If you have multiple versions of Python available (namely ``python3.6``, ``python3.7``, and ``python3.8``), you can run a full test matrix:

.. code-block:: bash

   tox -p auto

`pyenv <https://github.com/pyenv/pyenv>`__ is a great way to install multiple versions of Python on your computer.
Don't worry if you can't run the full test matrix locally: the GitHub Actions-based continuous integration workflow will run the full matrix of tests once you push to GitHub.

Build the Documentation
-----------------------

You can also use tox_ to build the documentation with Sphinx_:

.. code-block:: bash

   tox -e build_docs

The built documentation is located in the :file:`docs/_build/html` directory:

.. code-block:: bash

   open docs/_build/html/index.html

You can check that the documentation's links work by running the ``linkcheck`` test environment:

.. code-block:: bash

   tox -e linkcheck

Code Style
==========

This codebase follows :pep:`8`, the Python project's style guide.
The maximum line length is 80 characters.

The code base's style is checked with flake8_.
You can run flake8_ through tox_:

.. code-block:: bash

   tox -e codestyle

As a product of the Astropy Project, ``sphinx-example-index`` adheres to the `Astropy Coding Guidelines <http://docs.astropy.org/en/latest/development/codeguide.html>`__.
There are some areas where this project can't follow those guidelines, though, because ``sphinx-example-index`` is upstream of the ``astropy`` package.
For example, this project doesn't use utilities and configuration infrastructure provided by the ``astropy`` package itself.

Documentation Style
===================

Write docstrings for this project in the `numpydoc format <https://numpydoc.readthedocs.io/en/latest/format.html>`__.

Documentation content should follow the `Astropy Narrative Style Guide <http://docs.astropy.org/en/latest/development/style-guide.html#astropy-style-guide>`__.
