from django.conf import settings

class ClientBsae(object):

    def download(self, torrent):
        """
        Downloads the torrent using this client

        :param torrent:
            A Torrent object or a file that exists in the filesystem
        """
        raise NotImplementedError("The backend doesn't have a download method")