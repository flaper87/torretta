import os
import shutil
from django.conf import settings

from torretta.models import Torrent
from torretta.clients.base import ClientBsae

class RTorrent(ClientBsae):

    def download(self, torrent):
        filename = torrent
        if isinstance(torrent, Torrent):
            filename = torrent.download()

        watched = getattr(settings, "RTORRENT_WATCHED_FOLDER", "./")

        if not os.path.exists(watched):
            os.makedirs(watched)

        if os.path.dirname(filename) != watched:
            shutil.copy(filename, watched)




