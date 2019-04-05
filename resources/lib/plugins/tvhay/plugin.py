import urllib
import re
import base64
from utils.sucuri_cloudproxy import SucuriCloudProxy
from utils.mozie_request import Request
from tvhay.parser.category import Parser as Category
from tvhay.parser.channel import Parser as Channel
from tvhay.parser.movie import Parser as Movie


class Tvhay:
    domain = "http://tvhay.org/"

    def __init__(self):
        self.request = Request(session=True)
        body = self.request.get(self.domain)
        cookie = SucuriCloudProxy.get_cookie(body)
        print(cookie)
        body = self.request.get(self.domain, cookies=cookie, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.86 Safari/537.36'
        })
        print(body)


    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%spage/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = self.request.get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id))
        response = self.request.get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = self.request.get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%ssearch/%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response, 1)
