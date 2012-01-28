#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand

from torretta.spider.models import TorrentSearchCache

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--search', action='store_true', dest='use_search', default=False, help=''),
        make_option('--list-backends', action='store_true', dest='list_backends', default=False, help=''),

    )

    help = 'Looks for torrents on internet'
    args = '[--verbosity] [--backend] [--cache] [--list-backends] [search args ...]'

    def handle(self, *torrents, **options):
        if options.pop('use_search'):
            query = '%20'.join(torrents)
            torrents = TorrentSearchCache.objects.filter(search=query)
        else:
            torrents = TorrentSearchCache.objects.filter(pk__in=torrents)

        for t in torrents:
            print "Downloading torrent %s" % t.name
            t.download()



