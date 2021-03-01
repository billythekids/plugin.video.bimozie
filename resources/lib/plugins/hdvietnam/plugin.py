# coding=utf-8
import pickle
import re
import time

import utils.xbmc_helper as helper
from hdvietnam.parser.category import Parser as Category
from hdvietnam.parser.channel import Parser as Channel
from hdvietnam.parser.movie import Parser as Movie
from six.moves.urllib.parse import quote_plus
from utils.mozie_request import Request


class Hdvietnam:
    domain = "http://www.hdvietnam.com"

    def __init__(self):
        if not helper.getSetting('hdvietnam.username'):
            self.username = 'romvemot@gmail.com'
            self.password = 'bimozie'
        else:
            self.username = helper.getSetting('hdvietnam.username')
            self.password = helper.getSetting('hdvietnam.password')

        self.request = Request(header={
            'User-Agent': 'Mozilla/5.0',
            'Origin': self.domain,
            'Referer': self.domain
        }, session=True)

        if helper.has_file_path('hdvietnam.bin') and helper.get_last_modified_time_file('hdvietnam.bin') + 3600 < int(
                time.time()):
            helper.remove_file('hdvietnam.bin')

        if helper.has_file_path('hdvietnam.bin'):
            self.request.set_session(pickle.loads(helper.read_file('hdvietnam.bin', True)))
        else:
            self.login()

    def login(self, redirect='/'):
        params = {
            'login': self.username,
            'register': 0,
            'password': self.password,
            'remember': 1,
            'cookie_check': 1,
            '_xfToken': '',
            'redirect': redirect
        }
        response = self.request.post('%s/login/login' % self.domain, params)
        helper.write_file('hdvietnam.bin', pickle.dumps(self.request.get_request_session()), True)
        return response

    def thank(self, mid, token, postLink):
        params = {
            '_xfRequestUri': '/%s' % mid,
            '_xfToken': token,
            '_xfNoRedirect': 1,
            '_xfResponseType': 'json'
        }

        for v in postLink:
            url = '{}/{}'.format(self.domain, v)
            url = url.replace('likes', 'like')
            self.request.post(url, params=params)


    def getCategory(self):
        return Category().get(), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%spage-%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page=page, domain=self.domain)

    def getMovie(self, movie):
        url = '%s/%s' % (self.domain, movie)
        self.login(url)
        response = self.request.get(url)
        parser = Movie()
        result, postLinks = parser.is_block(response)
        if result is True:
            token = re.findall(r'name="_xfToken"\svalue="(.*?)"\s', response)
            self.thank(movie, token[0], postLinks)
            response = self.request.get(url)
            parser.is_block(response)

        result = parser.get(response, url)
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

        url = "%s/search/search" % self.domain
        response = Request().post(url, params=params)
        return Channel().get_search(response)
