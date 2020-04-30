.. currentmodule:: sphinx_example_index

Link resolution demo
====================

This page demonstrates that links (internal and external) can be resolved in standalone examples.

.. example:: API link
   :tags: links

   An internal API link: `setup`.

.. example:: Ref link
   :tags: links

   A ref link to a header: :ref:`api`.

.. example:: Doc link
   :tags: links

   A doc link to a page: :doc:`page-with-examples`.

.. example:: Intersphinx ref link
   :tags: links

   An intersphinx link to a section in the Astropy documentation: :ref:`astropy.wcs <astropy:astropy-wcs>`.

.. example:: Intersphinx API link
   :tags: links

   An intersphinx link to an API in the Astropy documentation: `astropy.table.Table`.

.. example:: File download example
   :tags: links, downloads

   This example features a file download link:

   :download:`Download hello.py <_includes/hello.py>`.

.. example:: Absolute file download example
   :tags: links, downloads

   :download:`Download the Astropy logo </astropy_project_logo.svg>`.

.. example:: External file download example
   :tags: links, downloads

   :download:`Download the Astropy README from GitHub <https://raw.githubusercontent.com/astropy/astropy/master/README.rst>`.
