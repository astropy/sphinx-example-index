{{ "Example Index" | escape | h1underline}}

.. hidden toctree for Sphinx navigation

.. toctree::
   :hidden:
{% for example in example_pages %}
   {{ example.rel_docref }}
{%- endfor %}

.. Listing for styling (eventually will become a tiled grid)
{% for example in example_pages %}
- :doc:`{{ example.source.title }} <{{ example.docref }}>`
{%- for tag_page in example.tag_pages %}
  {% if loop.first %}({% endif %}:doc:`{{ tag_page.name }} <{{ tag_page.docref }}>`{% if not loop.last %},{% else %}){% endif %}
{%- endfor %}
{%- endfor %}
