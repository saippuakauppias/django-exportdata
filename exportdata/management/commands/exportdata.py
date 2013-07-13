import os
import csv
import sys
from optparse import make_option
from collections import Callable

from django.contrib.sites.models import Site
from django.db.models.loading import get_model
from django.core.management.base import LabelCommand, CommandError


DOMAIN = Site.objects.get_current().domain


class Command(LabelCommand):

    option_list = LabelCommand.option_list + (
        make_option('--fields', dest='fields'),
        make_option('--filters', dest='filters', default=None),
        make_option('--ordering', dest='ordering', default=None),
        # TODO: advanced filtration, ranges
    )
    help = 'Export any data in csv'
    label = 'app.model'

    def get_model(self, label):
        app, model = label.split('.', 1)
        Model = get_model(app, model)
        if not Model:
            raise CommandError('Model "{0}" not found!'.format(label))
        return Model

    def get_result_filename(self, label):
        directory = os.path.join(os.path.expanduser('~'), 'exportdata')
        # TODO: add option for configuration directory
        if not os.path.exists(directory):
            os.makedirs(directory)
        return os.path.join(directory, '{0}.csv'.format(label))

    def set_filters(self, qs, filters):
        if filters:
            filters = filters.split(',')
            for filter_name in filters:
                # TODO: advanced filtration: filter_name.split('=', 1)
                if not hasattr(qs, filter_name):
                    msg = 'Model has no method "{1}"'.format(filter_name)
                    raise CommandError(msg)
                qs = getattr(qs, filter_name)()
        return qs

    def set_ordering(self, qs, ordering):
        if ordering:
            ordering = ordering.split(',')
            qs = qs.order_by(*ordering)
        return qs

    def get_fields(self, fields, Model):
        if not fields:
            return map(lambda x: x.name, Model._meta.fields)
        return fields.split(',')

    def handle_label(self, label, **options):
        fields = options.get('fields', None)
        filters = options.get('filters', None)
        ordering = options.get('ordering', None)

        Model = self.get_model(label)
        filename = self.get_result_filename(label)
        resultcsv = csv.writer(open(filename, 'wb'), delimiter=';',
                               quoting=csv.QUOTE_MINIMAL)

        qs = Model.objects.all()
        qs = self.set_filters(qs, filters)
        qs = self.set_ordering(qs, ordering)

        fields = self.get_fields(fields, Model)

        resultcsv.writerow(fields)
        for obj in qs:
            result = []
            for field_name in fields:
                if '__' in field_name:
                    parent_field, child_field = field_name.split('__', 1)
                    field = getattr(obj, parent_field, None)
                    field = getattr(field, child_field, None)
                else:
                    field = getattr(obj, field_name, None)

                if isinstance(field, Callable):
                    field = field()

                # TODO: move get_absolute_url to options (site_url_fields)
                if field_name == 'get_absolute_url':
                    # hack, because in python not possible
                    # check function has a decorator
                    field = u'http://{0}{1}'.format(DOMAIN, field)

                if isinstance(field, (str, unicode,)):
                    field = field.encode('utf-8')
                result.append(field)

            resultcsv.writerow(result)

        sys.exit('Done! Exported objects: {0}'.format(qs.count()))
