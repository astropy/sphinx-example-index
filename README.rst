#####################################################################
Sphinx extension for collecting examples from narrative documentation
#####################################################################

Your `Sphinx <https://www.sphinx-doc.org/en/master/>`__ documentation pages contain a lot of information: overviews, examples, how-tos, and references.
Embedded within your documentation pages might be useful standalone content.
This content makes sense in the flow of your existing documentation, but it might also get lost.
The ``sphinx-example-index`` extension helps you to resurface content into easily-discovered standalone pages.

With this extension, all you need to do to create a standalone example is mark it up with an ``example`` directive, give it a title, and optionally tag it.
The extension will:

- Generate an HTML page for each example with a copy of the example's content from the original documentation page.
- Generate an index of all the examples.
- Generate an index page for each unique tag.

**sphinx-example-index** is in early development.
Stay tuned for the initial release.

License
=======

This project is Copyright (c) Astropy Developers and licensed under the terms of the `BSD 3-Clause license <./licenses/LICENSE.rst>`__.
This package is based upon the `Astropy package template <https://github.com/astropy/package-template>`__ which is licensed under the BSD 3-clause license.
See the `licenses folder <./licenses>`__ for more information.

Contributing
============

We love contributions! Sphinx Example Index is open source, built on open source, and we'd love to have you hang out in our community.

**Imposter syndrome disclaimer**: We want your help. No, really.

There may be a little voice inside your head that is telling you that you're not ready to be an open source contributor; that your skills aren't nearly good enough to contribute.
What could you possibly offer a project like this one?

We assure you - the little voice in your head is wrong.
If you can write code at all, you can contribute code to open source.
Contributing to open source projects is a fantastic way to advance one's coding skills.
Writing perfect code isn't the measure of a good developer (that would disqualify all of us!); it's trying to create something, making mistakes, and learning from those mistakes.
That's how we all improve, and we are happy to help others learn.

Being an open source contributor doesn't just mean writing code, either.
You can help out by writing documentation, tests, or even giving feedback about the project (and yes - that includes giving feedback about the contribution process).
Some of these contributions may be the most valuable to the project as a whole, because you're coming to the project with fresh eyes, so you can see the errors and assumptions that seasoned contributors have glossed over.

Note: This disclaimer was originally written by `Adrienne Lowe <https://github.com/adriennefriend>`__ for a `PyCon talk <https://www.youtube.com/watch?v=6Uj746j9Heo>`__, and was adapted by sphinx-example-index based on its use in the README file for the `MetPy project <https://github.com/Unidata/MetPy>`__.
