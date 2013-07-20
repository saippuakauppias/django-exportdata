django-exportdata
=================

App for export data in csv files from models with selected fields and custom filtration.

Useful for create reports and calculate some statistic data for external sources.

Requires
--------

Python 2.6 or 2.7 and Django 1.3 and higher.

Installation
------------

Install using pip:

    $ pip install django-exportdata

Add ``exportdata`` in ``INSTALLED_APPS``.

Examples Of Usage
-----------------

Create **~/exportdata/auth.User.csv** file with all model data:

    $ python manage.py exportdata auth.User

Set fields for export:

    $ python manage.py exportdata app.model --fields=pk,model_field,get_absolute_url,method_property,fk__field

Set custom filtration (based on model manager methods and ``filter(field=value)`` filtration):

    $ python manage.py exportdata app.model --filters=active,paid,field=value,fk__field__gte=value

Set custom ordering:

    $ python manage.py exportdata app.model --ordering=-created_on,title

Set "from and to" range values primary keys (pks) for export:

    $ python manage.py exportdata app.model --range=1-100

Or set range with comma-separated values:

    $ python manage.py exportdata app.model --range=1,2,3,4,5

Set custom file path for save:

    $ python manage.py exportdata app.model --filepath=directory/filename.extension

Set fields when decorated ``models.permalink`` (by default ``get_absolute_url`` field). For adding the domain before data:

    $ python manage.py exportdata app.model --permalinks=get_absolute_url,get_absolute_admin_url
