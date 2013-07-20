``--range`` option
==================

Set "from and to" diapason values primary keys (pks) for export or set comma-separated values.

Examples
--------

"From and to" range::

    $ python manage.py exportdata app.model --range=1-100

Comma separated values::

    $ python manage.py exportdata app.model --range=1,2,3,4,5
