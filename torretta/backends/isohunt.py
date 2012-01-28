#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from django.utils.encoding import smart_unicode

# Torretta
from torretta.models import Torrent
from torretta.exceptions import NoTorrentFound
from torretta.backends.base import BackendBase

class IsoHunt(BackendBase):
    name = "IsoHunt"

    def __init__(self, *args, **kwargs):
        super(IsoHunt, self).__init__(*args, **kwargs)
        self.base_url = 'http://isohunt.com'
        self.url = 'http://isohunt.com/torrents/%s?iht=-1&ihp=1&ihs1=1&iho1=d'
        self.last_query = None

    def prepare_url(self, query):
        if isinstance(query, Torrent):
            query = query.link

        if query.startswith("/"):
            return self.base_url + query
        return self.url % query

    def get_torrents_list(self, query, use_cache=False):
        if use_cache:
            if not query:
                raise RuntimeError("Query needed to use cache")
            return TorrentSearchCache.objects.filter(search=query)

        tree = self.tree(query)

        pages = tree("table[class=pager]") or []
        if pages:
            pages = pages[0].cssselect("td")[1].cssselect("a")

        def get_torrents(page_tree):
            def filter_links(urls_list):
                for url in urls_list:
                    yield "/torrent_details/" in link[0] and (not link[1].startswith("+") and not len(link[1]) == 1)

            links = []
            for l in page_tree(".row3 a"):
                href = l.get("href")

                if not href \
                        or not "torrent_details" in href \
                            or not "comments" in href:
                    continue

                rating = l.get("title").split(" ")[0]
                if rating.startswith("-"):
                    continue

                try:
                    rating = int(rating[1:])
                except ValueError:
                    rating = 0

                href = href.replace("comments", "summary")

                seeds = l.getparent().getparent().cssselect(".row1") or 0
                if seeds:
                    try:
                        seeds = int(seeds[0].text)
                    except ValueError:
                        seeds = 0

                torrent, created = Torrent.objects.get_or_create(link=href, defaults={"backend" : self.name,
                                                                                "seeds" : seeds,
                                                                                "rating" : rating})
                if not created:
                    torrent.seeds = seeds
                    torrent.rating = rating
                    torrent.save()
                links .append(torrent)
            return links

        # Get the torrents list for the current page
        links_objects = get_torrents(tree)

        # Iterate over all pages and get the torrents list
        for page in pages:
            links_objects += get_torrents(self.tree(page.get("href")))

        return links_objects

    def get_torrent(self, torrent_link, name=None):
        page = self.tree(torrent_link)
        if not page:
            raise NoTorrentFound(torrent_link)

        link = page("a[target=_top]")
        if not link:
            raise NoTorrentFound(torrent_link)

        link = link[0].get("href")

        filename = os.path.join(self.watch_folder, name or link.split("/")[-1])

        with open(filename, "w") as out:
            torrent = self.get(link)
            out.write(torrent.content)

        return link, filename
