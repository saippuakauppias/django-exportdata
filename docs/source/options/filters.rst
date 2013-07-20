``--filters`` option
====================

You can set custom filtration (based on model manager methods or ``filter(field=value)`` filtration).

Example
-------

::

    $ python manage.py exportdata app.model --filters=active,paid,field=value,fk__field__gte=value
