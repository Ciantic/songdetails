{{ fullname }}
{{ '=' * ((fullname | length) + 7) }}

.. automodule:: {{ fullname }}

{% block modules %}
{% if modules %}	
Modules
------------------

.. autosummary::
    :toctree: {{ name }}/

{% for submodule in modules %}
    {{ submodule }}
{% endfor %}

{% endif %}
{% endblock %}

Members
---------------

.. autosummary::
	:nosignatures:
	
	{% for member in members %}
	{% if not member.startswith("_") %}
	{{ member }}
	{% endif %}
	{% endfor %}

Member definitions
------------------

{% block attributes %}
{% if attributes %}	
.. rubric:: Attributes

{% for attr in attributes %}
.. autoattribute:: {{ fullname }}.{{ attr }}
{% endfor %}
{% endif %}
{% endblock %}


{% block datas %}
{% if datas %}	
.. rubric:: Attributes

{% for data in datas %}
.. autodata:: {{ fullname }}.{{ data }}
{% endfor %}
{% endif %}
{% endblock %}


{% block functions %}
{% if functions %}
.. rubric:: Functions

{% for item in functions %}
.. autofunction:: {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}


{% block classes %}
{% if classes %}

.. rubric:: Classes

{% for item in classes %}
.. autoclass:: {{ item }}()
	:inherited-members:
	:show-inheritance:
{%- endfor %}
{% endif %}
{% endblock %}


{% block exceptions %}
{% if exceptions %}
.. rubric:: Exceptions
    
{% for item in exceptions %}
.. autoexception:: {{ item }}
{%- endfor %}
{% endif %}
{% endblock %}
