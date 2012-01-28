import os
from datetime import datetime

from django.test import TestCase
from torretta.backends import BackendBase, IsoHunt

class GeneralTests(TestCase):

    def setUp(self):
        self.base_backend = BackendBase()

        for root, dirs, files in os.walk(self.base_backend.watch_folder):
            for f in files:
                os.unlink(os.path.join(root, f))
            for d in dirs:
                shutil.rmtree(os.path.join(root, d))

    def test_requests(self):
        resp = self.base_backend.get("http://httpbin.org/get")
        self.assertEquals(resp.status_code, 200)

    def test_isohunt(self):
        isohunt = IsoHunt()
        torrents = isohunt.get_torrents_list(query="nikita")
        self.assertTrue(torrents)

        link, filename = isohunt.get_torrent(torrents[0])
        self.assertTrue(os.path.exists(filename))


