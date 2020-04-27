{{ title | escape | h1underline}}

From :doc:`{{ example.docref }}`.
{% if tag_pages %}
Tagged:
{%- for tag_page in tag_pages %}
:doc:`{{ tag_page.name }} <{{ tag_page.docref }}>`{% if not loop.last %},{% else %}.{% endif %}
{%- endfor %}
{%- endif %}
