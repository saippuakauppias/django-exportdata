Usage
=====

Command syntax::

    $ python manage.py exportdata <app.Model> [options]

Basic
-----

Run for export all model data in **~/exportdata/app.Model.csv** file::

    $ python manage.py exportdata app.Model


Advanced
--------

.. toctree::
   :maxdepth: 1

   options/fields
   options/filters
   options/ordering
   options/range
   options/filepath
   options/permalinks
