import os
import csv
import sys
from optparse import make_option
from collections import Callable

from django.db.models import Q
from django.contrib.sites.models import Site
from django.db.models.loading import get_model
from django.core.management.base import LabelCommand, CommandError


DOMAIN = Site.objects.get_current().domain


class Command(LabelCommand):

    option_list = LabelCommand.option_list + (
        make_option('--fields', dest='fields', default=None,
                    help='Comma-separated list of fields for export'),
        make_option('--filters', dest='filters', default=None,
                    help='"field=value" formatted list or comma-separated '
                         'list of model methods for filtering'),
        make_option('--ordering', dest='ordering', default=None,
                    help='Comma-separated list of fields for order_by method'),
        make_option('--range', dest='range', default=None,
                    help='"from-to" range or comma-separated list '
                         'of primary keys for export'),
        make_option('--filepath', dest='filepath', default=None,
                    help='Path to file for save data'),
        make_option('--permalinks', dest='permalinks',
                    default=['get_absolute_url'],
                    help='Comma-separated list of model methods decorated '
                         '"models.permalink" decorator'),
    )
    help = 'Export filtered/ordered/ranged data from model (with selected ' \
           'fields) in csv'
    label = 'app.model'
    args = '<app.model>'

    def get_model(self, label):
        app, model = label.split('.', 1)
        Model = get_model(app, model)
        if not Model:
            raise CommandError('Model "{0}" not found!'.format(label))
        return Model

    def get_result_filename(self, filepath, label):
        if filepath:
            directory = filepath.rsplit('/', 1)
            filename = directory.pop()
            if directory:
                directory = directory.pop()
            else:
                directory = '.'
        else:
            directory = os.path.join(os.path.expanduser('~'), 'exportdata')
            filename = '{0}.csv'.format(label)
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(directory, filename)

    def set_filters(self, qs, filters):
        if filters:
            filters = filters.split(',')
            for filter_name in filters:
                if '=' in filter_name:
                    field, value = filter_name.split('=', 1)
                    qs = qs.filter(**{field: value})
                elif hasattr(qs, filter_name):
                    qs = getattr(qs, filter_name)()
                else:
                    msg = 'Model has no method "{0}" ' \
                          'or this filter not "key=value" ' \
                          'formatted'.format(filter_name)
                    raise CommandError(msg)
        return qs

    def set_ordering(self, qs, ordering):
        if ordering:
            ordering = ordering.split(',')
            qs = qs.order_by(*ordering)
        return qs

    def set_range(self, qs, pk_range):
        if pk_range:
            if '-' in pk_range:
                from_value, to_value = pk_range.split('-', 1)
                qs = qs.filter(pk__gte=from_value)
                qs = qs.filter(pk__lte=to_value)
            if ',' in pk_range:
                values = pk_range.split(',')
                lookup = Q(pk=values[0])
                for value in values[1:]:
                    lookup |= Q(pk=value)
                qs = qs.filter(lookup)
        return qs

    def get_fields(self, fields, Model):
        if not fields:
            return map(lambda x: x.name, Model._meta.fields)
        return fields.split(',')

    def get_field_data(self, field_name, obj, permalinks):
        if '__' in field_name:
            parent_field, child_field = field_name.split('__', 1)

            if not hasattr(obj, parent_field):
                msg = 'Model object has no attribute "{0}"'.format(
                    parent_field)
                raise CommandError(msg)
            field = getattr(obj, parent_field, None)

            if not hasattr(field, child_field):
                msg = '"{0}" object has no attribute "{1}"'.format(
                    parent_field, child_field)
                raise CommandError(msg)
            field = getattr(field, child_field)
        else:
            field = getattr(obj, field_name)

        if isinstance(field, Callable):
            field = field()

        if field_name in permalinks:
            # hack, because in python not possible
            # check function has a decorator
            field = u'http://{0}{1}'.format(DOMAIN, field)

        if isinstance(field, (str, unicode,)):
            field = field.encode('utf-8')
        return field

    def handle_label(self, label, **options):
        fields = options.get('fields')
        filters = options.get('filters')
        ordering = options.get('ordering')
        pk_range = options.get('range')
        filepath = options.get('filepath')
        permalinks = options.get('permalinks')

        Model = self.get_model(label)
        full_path = self.get_result_filename(filepath, label)
        resultcsv = csv.writer(open(full_path, 'wb'), delimiter=';',
                               quoting=csv.QUOTE_MINIMAL)

        if not isinstance(permalinks, list):
            permalinks = permalinks.split(',')

        qs = Model.objects.all()
        qs = self.set_filters(qs, filters)
        qs = self.set_ordering(qs, ordering)
        qs = self.set_range(qs, pk_range)

        fields = self.get_fields(fields, Model)

        resultcsv.writerow(fields)
        for obj in qs:
            result = []
            for field_name in fields:
                data = self.get_field_data(field_name, obj, permalinks)
                result.append(data)

            resultcsv.writerow(result)

        sys.exit('Done! Exported objects: {0}'.format(qs.count()))
