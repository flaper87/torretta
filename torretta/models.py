import hashlib
from django.db import models
from djangotoolbox.fields import ListField

class Torrent(models.Model):
    seeds = models.IntegerField(db_index=True, default=0)
    rating = models.IntegerField(db_index=True, default=0)
    backend = models.CharField(max_length=500, db_index=True)
    link = models.CharField(max_length=500, null=False, db_index=True)
    sha1 = models.CharField(max_length=500, db_index=True, unique=True, null=False)

    class MongoMeta:
        capped = True
        collection_max = 10000

    def save(self, *args, **kwargs):
        sha = hashlib.sha1()
        sha.update(self.link)
        self.sha1 = sha.hexdigest()
        super(Torrent, self).save(*args, **kwargs)

class TorrentSearchCache(models.Model):
    name = models.CharField(max_length=500, db_index=True)
    backend = models.CharField(max_length=500, db_index=True)
    url = models.CharField(max_length=500, db_index=True)

    class MongoMeta:
        capped = True
        collection_max = 10000

    def __unicode__(self):
        return self.url

    def download(self):
        pass