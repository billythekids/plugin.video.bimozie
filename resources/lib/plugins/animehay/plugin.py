# -*- coding: utf-8 -*-
import utils.xbmc_helper as helper
from animehay.parser.category import Parser as Category
from animehay.parser.channel import Parser as Channel
from animehay.parser.movie import Parser as Movie
from utils.mozie_request import Request
from six.moves.urllib.parse import quote_plus
try:
    from cloudscraper2 import CloudScraper
except:
    import cloudscraper as CloudScraper


class Animehay:
    domain = "https://animehay.site"

    def __init__(self):
        self.username = helper.getSetting('animehay.username')
        self.password = helper.getSetting('animehay.password')
        # self.request = Request(session=True)
        self.request = CloudScraper.create_scraper(browser={
            'browser': 'firefox',
            'platform': 'windows',
            'mobile': True
        }, allow_brotli=False)
        # self.login()

    def login(self, redirect=None):
        params = {
            'user_id': self.username,
            'password': self.password,
            'send_log': "Đăng Nhập"
        }
        response = self.request.post('%s/dang-nhap?ref=/' % self.domain, params)
        return response

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response.content), Channel().get(response.content, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s?page=%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = self.request.get(url)
        return Channel().get(response.content, page)

    def getMovie(self, mid):
        url = Movie().get_movie_link(self.request.get(mid).content)
        response = self.request.get(url)
        return Movie().get(response.content)

    def getLink(self, movie):
        response = self.request.get(movie['link'])
        return Movie().get_link(response.content, movie['link'])

    def search(self, text):
        url = "%s/tim-kiem?q=%s" % (self.domain, quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response.content, 1)
