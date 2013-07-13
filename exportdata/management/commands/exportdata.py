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

    def handle_label(self, label, **options):
        app, model = label.split('.', 1)
        Model = get_model(app, model)
        if not Model:
            raise CommandError('Model "{0}" not found!'.format(label))

        filename = os.path.join(os.path.expanduser('~'),
                                '{0}.csv'.format(label))
        resultcsv = csv.writer(open(filename, 'wb'), delimiter=';',
                               quoting=csv.QUOTE_MINIMAL)

        fields = options.get('fields')
        filters = options.get('filters', None)
        ordering = options.get('ordering', None)

        qs = Model.objects.all()
        if filters:
            filters = filters.split(',')
            for filter_name in filters:
                if not hasattr(qs, filter_name):
                    raise CommandError(
                        'Model "{0}" not not to have "{1}" filter'.format(
                            label,
                            filter_name
                        )
                    )
                qs = getattr(qs, filter_name)()

        if ordering:
            ordering = ordering.split(',')
            qs = qs.order_by(*ordering)

        fields = fields.split(',')
        resultcsv.writerow(fields)
        for obj in qs:
            result = []
            for field_name in fields:
                if '__' in field_name:
                    field_name = field_name.split('__', 1)
                    field = getattr(obj, field_name[0], None)
                    field = getattr(field, field_name[1], None)
                else:
                    field = getattr(obj, field_name, None)
                if field_name == 'get_absolute_url':
                    # hack, because in python not possible
                    # check function has a decorator
                    field = field()
                    field = u'http://{0}{1}'.format(DOMAIN, field)
                if isinstance(field, Callable):
                    field = field()
                if isinstance(field, (str, unicode,)):
                    field = field.encode('utf-8')
                result.append(field)

            resultcsv.writerow(result)

        sys.exit('Done! Exported objects: {0}'.format(qs.count()))
