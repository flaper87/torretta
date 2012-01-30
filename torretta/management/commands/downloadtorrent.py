#!/usr/bin/env python
# -*- coding: utf-8 -*-

from optparse import make_option
from django.core.management.base import BaseCommand

from torretta.models import Torrent
from torretta.clients import clients
from torretta.backends import backends

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--torrent', action='store', dest='torrent', default=0, help='Torrent id or link'),
        make_option('--backend', action='store', dest='backend', default='IsoHunt', help=''),
        make_option('--client', action='store', dest='client', default='RTorrent', help='Torrent id or link'),
    )

    help = 'Downloads the specified torrent'
    args = '--torrent'

    def handle(self, *torrents, **options):
        assert options.get('torrent')

        torrent = options.pop('torrent')
        client = clients.get(options.get('client'))()
        backend = backends.get(options.get('backend'))()

        try:
            torrent = Torrent.objects.get(pk=int(torrent))
        except ValueError:
            assert torrent.startswith("http")
            torrent = backend.get_torrent(torrent)

        client.download(torrent)


