django-exportdata
=================

Export model data (filtered and ordered) to csv file.
Useful for create reports for model with only selected fields.

Installation
------------

Install using pip:

    $ pip install django-exportdata

Add ``exportdata`` in ``INSTALLED_APPS``.

Example Of Usage
----------------

Create **~/exportdata/auth.User.csv** file with all model data:

    $ python manage.py exportdata auth.User

Set fields for export:

    $ python manage.py exportdata app.model --fields=pk,model_field,get_absolute_url,method_property,fk__field

Set custom filtration (based on model manager methods):

    $ python manage.py exportdata app.model --filters=active,paid

Set custom ordering:

    $ python manage.py exportdata app.model --ordering=-created_on,title
