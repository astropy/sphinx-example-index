:orphan:

{{ title | h1underline }}
{% for example in tag.example_pages %}
- :doc:`{{ example.source.title }} <{{ example.docref }}>`
{%- for tag_page in example.tag_pages %}
  {% if loop.first %}({% endif %}:doc:`{{ tag_page.name }} <{{ tag_page.docref }}>`{% if not loop.last %},{% else %}){% endif %}
{%- endfor %}
{%- endfor %}
