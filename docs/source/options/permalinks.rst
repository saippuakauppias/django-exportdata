``--permalinks`` option
=======================

Set fields when decorated ``models.permalink`` (by default ``get_absolute_url`` field).

This option add the domain before data from field.

Example
-------

::

    $ python manage.py exportdata app.model --permalinks=get_absolute_url,get_absolute_admin_url
