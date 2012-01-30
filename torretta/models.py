import hashlib
from django.db import models

class Torrent(models.Model):
    text = models.CharField(max_length=500, db_index=True)
    seeds = models.IntegerField(db_index=True, default=0)
    rating = models.IntegerField(db_index=True, default=0)
    backend = models.CharField(max_length=500, db_index=True)
    link = models.CharField(max_length=500, null=False, db_index=True)
    sha1 = models.CharField(max_length=500, db_index=True, unique=True, null=False)
    filename = models.CharField(max_length=500)

    class MongoMeta:
        capped = True
        collection_max = 10000

    def save(self, *args, **kwargs):
        sha = hashlib.sha1()
        sha.update(self.link)
        self.sha1 = sha.hexdigest()
        super(Torrent, self).save(*args, **kwargs)

    def download(self):
        from torretta.backends import backends
        backend = backends.get(self.backend)()
        assert backend, "%s backend has been disabled" % self.backend

        name = self.text
        if not name.endswith(".torrent"):
            name = name + ".torrent"
        self.filename = backend.get_torrent(self.link, name=name)
        self.save()
        return self.filename

