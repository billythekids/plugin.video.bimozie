import urllib
import re
import base64
from utils.sucuri_cloudproxy import SucuriCloudProxy
from utils.mozie_request import Request
from tvhay.parser.category import Parser as Category
from tvhay.parser.channel import Parser as Channel
from tvhay.parser.movie import Parser as Movie


class Tvhay:
    domain = "http://tvhai.org"
    cookie = {}
    h = {
        'Referer': domain,
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
    }

    def __init__(self):
        self.request = Request(self.h, session=True)
        # try:
        #     body = self.request.get(self.domain)
        #     cookie = SucuriCloudProxy.get_cookie(body)
        #     body = self.request.get(self.domain, cookies=cookie, headers={
        #         'Referer': 'http://tvhay.org/',
        #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        #     })
        #     self.cookie = SucuriCloudProxy.get_cookie(body)
        # except: pass

    def getCategory(self):
        response = self.request.get('%s/phim-le/' % self.domain, cookies=self.cookie)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace("http://tvhayzz.org", "")
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%spage/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = self.request.get(url, cookies=self.cookie)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(
            self.request.get(id, cookies=self.cookie)
        )
        response = self.request.get(url, cookies=self.cookie)
        return Movie().get(response)

    def getLink(self, movie):
        response = self.request.get(movie['link'], cookies=self.cookie)
        return Movie().get_link(response, movie['link'])

    def search(self, text):
        url = "%s/search/%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url, cookies=self.cookie)
        return Channel().get(response, 1)
