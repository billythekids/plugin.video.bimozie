# -*- coding: utf-8 -*-
import urllib
from utils.mozie_request import Request
from animehay.parser.category import Parser as Category
from animehay.parser.channel import Parser as Channel
from animehay.parser.movie import Parser as Movie
import utils.xbmc_helper as helper


class Animehay:
    domain = "https://animehay.tv"

    def __init__(self):
        self.username = helper.getSetting('animehay.username')
        self.password = helper.getSetting('animehay.password')
        self.request = Request(session=True)
        self.login()

    def login(self, redirect=None):
        params = {
            'user_id': self.username,
            'password': self.password,
            'send_log': "Đăng Nhập"
        }
        response = self.request.post('%s//dang-nhap?ref=/' % self.domain, params)
        return response

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s?page=%d' % (self.domain, channel, page)
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
        return Movie().get_link(response, movie['link'])

    def search(self, text):
        url = "%s/tim-kiem?q=%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response, 1)
