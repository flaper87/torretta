#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import make_option
from django.core.management.base import BaseCommand
from django.utils.encoding import smart_unicode, smart_str

from torretta.backends import backends
from torretta.utils.pprint import pprint_table

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--backend', action='store', dest='backend', default='IsoHunt', help=''),
        make_option('--limit', action='store', dest='limit', default=0, type=int, help=''),
        make_option('--cache', action='store_true', dest='use_cache', default=False, help=''),
        make_option('--list-backends', action='store_true', dest='list_backends', default=False, help=''),
    )

    help = 'Looks for torrents on internet'
    args = '[--verbosity] [--backend] [--cache] [--list-backends] [search args ...]'

    requires_model_validation = False

    def handle(self, *search, **options):

        if options.pop('list_backends'):
            for module in backends:
                print module
            return

        backend = options.get('backend', True)
        query = '%20'.join(search)

        mod = backends.get(backend)()
        table = [["pk", "text", "rating", "seeds", "backend"]]

        limit = options.pop('limit')
        for i, t in enumerate(mod.get_torrents_list(query, use_cache=options.pop('use_cache'))):
            if limit > 0 and i >= limit:
                break
            table.append([str(t.pk), smart_str(t.text, errors='ignore'), t.rating, t.seeds, t.backend])
        pprint_table(sys.stdout, table)


