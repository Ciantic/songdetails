{{ fullname }}
{{ underline }}

.. automodule:: {{ fullname }}

    {% block functions %}
    {% if functions %}
    .. rubric:: Functions

    .. autosummary::
        :toctree: {{ fullname }}/functions
        
    {% for item in functions %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block classes %}
    {% if classes %}
    .. rubric:: Classes

    .. autosummary::
        :toctree: {{ fullname }}/classes
        
    {% for item in classes %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}

    {% block exceptions %}
    {% if exceptions %}
    .. rubric:: Exceptions

    .. autosummary::
        :toctree: {{ fullname }}/exceptions
        
    {% for item in exceptions %}
        {{ item }}
    {%- endfor %}
    {% endif %}
    {% endblock %}
