# -*- coding: utf-8 -*-
from utils.mozie_request import Request
from bilutvb.parser.category import Parser as Category
from bilutvb.parser.channel import Parser as Channel
from bilutvb.parser.movie import Parser as Movie
import urllib, re


class Bilutvb:
    domain = "https://bilutvb.com"

    def __init__(self):
        self.request = Request(header={
            "Accept-Language": "en-US,en;q=0.9,vi;q=0.8",
            "accept-encoding": "deflate"
        })

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace('.html/', "/")
            channel = channel.replace('.html', "/")
            url = '%s%s/page/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        # https://bilutvb.com/ajax/movie_load_info/1936
        mid = re.search(r'load_info/(\d+)', url).group(1)
        # https://bilutvb.com/ajax/get_episodes/1936
        response = self.request.get('%s/ajax/get_episodes/%s' % (self.domain, mid))
        return Movie().get(response)

    def getLink(self, movie):
        # response = self.request.get(movie['link'])
        # https://bilutvb.com/ajax/get_sources/67325
        response = self.request.get('%s/ajax/get_sources/%s' % (self.domain, movie['link']))
        return Movie().get_link(response, self.request, self.domain)

    def search(self, text, page=1):
        # url = "%s/search/%s" % (self.domain, urllib.quote_plus(text))
        url = "%s/wp-admin/admin-ajax.php" % self.domain
        response = self.request.post(url, params={
            'action': 'halimthemes_ajax_search',
            'search': text
        })

        return Channel().getSearchResult(response)
