import requests
from django.conf import settings
from pyquery import PyQuery as pq

class BackendBase(object):

    def __init__(self, *args, **kwargs):
        self.http = requests.session()
        self.watch_folder = getattr(settings, "TORRENT_WATCH_FOLDER", "")

    def tree(self, url_or_query):
        """
        Builds a pyquery object afeter executing the http reuqest.

        :param url_or_query:
            The url or query
        """
        resp = self.get(url_or_query)
        if resp.status_code == 200:
            return pq(resp.content)

    def prepare_url(self, url_or_query):
        """
        Overridable method that prepares the url for the http request.

        :param url_or_query:
            The url or query
        """
        return url_or_query

    def get(self, url_or_query):
        """
        GET http request.

        This methods calls ``prepare_url`` before executing the http request.

        :param url_or_query:
            The query or url to execute
        """
        return self.http.get(self.prepare_url(url_or_query))

    def get_torrents_list(self):
        """
        Gets the torrents list and stores them into mongodb if save is True.
        """
        raise NotImplementedError("The backend doesn't have a get_torrents_list method")

    def get_torrent(self, torrent_link, name=None):
        """
        Downloads the torrent associated to torrent_link.

        :param torrent_link:
            The torrent_link could be a direct torrent link or a summary page where a
            .torrent link could be extracted. It depends on the specfied backend.

        :param name:
            The name of the file where the torrent should be written to.
        """
        raise NotImplementedError("The backend doesn't have a get_torrent method")