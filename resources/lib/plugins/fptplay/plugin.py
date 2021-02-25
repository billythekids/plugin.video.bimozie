# -*- coding: utf-8 -*-

import utils.fpt_helper as fpt
from six.moves.urllib.parse import quote_plus
from utils.mozie_request import Request

from .parser.category import Parser as Category
from .parser.channel import Parser as Channel
from .parser.movie import Parser as Movie


class Fptplay:
    domain = "https://fptplay.vn"

    def __init__(self):
        # if not helper.getSetting('fptplay.username'):
        #     self.username = 'romvemot@gmail.com'
        #     self.password = 'bimozie'
        # else:
        #     self.username = helper.getSetting('fptplay.username')
        #     self.password = helper.getSetting('fptplay.password')

        self.request = Request(session=True)

    def login(self, redirect=None):
        params = {
            'login': self.username,
            'password': self.password,
            'register': 0,
            'cookie_check': 1,
            '_xfToken': '',
            'redirect': redirect
        }
        self.request.get('%s/login' % self.domain)
        response = self.request.post('%s/login/login' % self.domain, params)
        return response

    def getCategory(self):
        # https://api.fptplay.net/api/v6.1_w/structure/vod
        token, timestamp = fpt.generate_stoken('structure/vod')
        url = '%s%sstructure/vod' % (fpt.domain, fpt.suffix)

        response = self.request.get(url, params={
            'st': token, 'e': timestamp
        })

        return Category().get(response), None

    def getChannel(self, channel, page=1):
        # https://api.fptplay.net/api/v6.1_w/vod?structure_id=55701c1517dc1321ee85857a&per_page=24&page=2

        # if page > 1:
        token, timestamp = fpt.generate_stoken('vod')
        url = '%s%svod' % (fpt.domain, fpt.suffix)
        response = self.request.get(url, params={
            'st': token,
            'e': timestamp,
            'structure_id': channel,
            'per_page': 24,
            'page': page
        })

        return Channel().get_page_ajax(response, page=page, domain=self.domain)

    def getMovie(self, id):
        url = '%s/xem-video/aaa-%s' % (self.domain, id)
        response = self.request.get(url)
        result = Movie().get(response, id)
        return result

    def getLink(self, movie):
        # https://api.fptplay.net/api/v6.1_w/stream/vod/5d2413182089bd10412a0c92/1/auto_vip

        path = 'stream/vod/%s/auto_vip' % movie['link']
        url = '%s%s%s' % (fpt.domain, fpt.suffix, path)
        token, timestamp = fpt.generate_stoken(path)
        response = self.request.get(url, params={
            'st': token,
            'e': timestamp
        })

        result = Movie().get_link(response)
        return result

    def search(self, text):
        text = quote_plus(text)
        params = {
            'keywords': text,
            'nodes[]': [337, 116, 150, 33, 57, 123],
            'type': 'post',
            'order': 'date',
            'child_nodes': 1
        }

        url = "%s/tim-kiem/%s" % (self.domain, text)
        response = Request().get(url)
        return Channel().get_search(response)
