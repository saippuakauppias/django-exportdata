``--fields`` option
===================

You can select fields in model for export. By default, if ``--fields`` option is not set -- export all fields.

Option support FK-fields, model methods, properties, and decorated methods.

Example
-------

::

    $ python manage.py exportdata app.model --fields=pk,model_field,get_absolute_url,method_property,fk__field
