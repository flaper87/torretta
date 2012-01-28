#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
from optparse import make_option
from django.core.management.base import BaseCommand

from django.utils.encoding import smart_unicode, smart_str

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
            for module in module_pool.modules:
                print module
            return

        backend = options.get('backend', True)
        query = '%20'.join(search)

        mod = module_pool.get_module(backend)()
        table = [["pk", "name", "backend", "search"]]

        limit = options.pop('limit')

        for i,t in enumerate(mod.get_torrents_list(query, use_cache=options.pop('use_cache'))):
            if limit > 0 and i >= limit:
                break
            table.append([t.pk, smart_str(t.name, errors='ignore'), t.backend, t.search])
        pprint_table(sys.stdout, table)


