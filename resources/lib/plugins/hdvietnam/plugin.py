# coding=utf-8
import urllib
import re
from utils.mozie_request import Request
from hdvietnam.parser.category import Parser as Category
from hdvietnam.parser.channel import Parser as Channel
from hdvietnam.parser.movie import Parser as Movie
import utils.xbmc_helper as helper


class Hdvietnam:
    domain = "http://www.hdvietnam.com"

    def __init__(self):
        if not helper.getSetting('hdvietnam.username'):
            self.username = 'romvemot@gmail.com'
            self.password = 'bimozie'
        else:
            self.username = helper.getSetting('hdvietnam.username')
            self.password = helper.getSetting('hdvietnam.password')

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

    def thank(self, id, token, postLink):
        params = {
            '_xfRequestUri': id,
            '_xfToken': token,
            '_xfNoRedirect': 0,
            '_xfResponseType': 'json'
        }
        map(lambda v: self.request.post('%s/%s' % (self.domain, v), params), postLink)

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
        response = self.login(redirect=url)
        parser = Movie()
        result, postLinks = parser.is_block(response)
        if result is True:
            token = re.findall(r'name="_xfToken"\svalue="(.*?)"\s', response)
            self.thank(movie, token[0], postLinks)
            response = self.request.get(url)

        result = parser.get(response, url)
        return result

    def search(self, text):
        text = urllib.quote_plus(text)
        params = {
            'keywords': text,
            'nodes[]': [337, 116, 150, 33, 57, 123],
            'type': 'post',
            'order': 'date',
            'child_nodes': 1
        }

        url = "%s/search/search" % self.domain
        response = Request().post(url, params=params)
        # print('77777777777777777777777777777777777777')
        # print(helper.write_file('test.html', response.encode('utf-8')))
        return Channel().get_search(response)
