# -*- coding: utf-8 -*-
from utils.mozie_request import Request
from bilutvb.parser.category import Parser as Category
from bilutvb.parser.channel import Parser as Channel
from bilutvb.parser.movie import Parser as Movie
import urllib


class Bilutvb:
    domain = "https://bilutvb.com"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%spage/%d/' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = Request().get(url, headers={
            "Accept-Language": "en-US,en;q=0.9,vi-VN;q=0.8,vi;q=0.7,de-DE;q=0.6,de;q=0.5,nb;q=0.4"
        })
        return Channel().get(response)

    def getMovie(self, url):
        # url = "%s/phim-0-%s.html" % (self.domain, id)
        response = Request().get(url)
        url = Movie().get_movie_link(response)
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response, self.domain)

    def search(self, text, page=1):
        url = "%s/search/%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response)
