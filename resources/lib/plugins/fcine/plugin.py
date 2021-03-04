import pickle
import re
import time

import utils.xbmc_helper as helper
from fcine.parser.category import Parser as Category
from fcine.parser.channel import Parser as Channel
from fcine.parser.movie import Parser as Movie
from utils.mozie_request import Request


class Fcine:
    domain = "https://fcine.net"
    token = None
    member_id = None

    def __init__(self):
        if not helper.getSetting('fcine.username'):
            # helper.message('Please login to fcine.net', 'Login Required')
            self.username = 'romvemot@gmail.com'
            self.password = 'bimozie'
        else:
            self.username = helper.getSetting('fcine.username'),
            self.password = helper.getSetting('fcine.password'),

        self.request = Request(header={
            'User-Agent': 'Mozilla/5.0',
            'origin': 'https://fcine.net',
            'referer': 'https://fcine.net/login/',
        }, session=True)

        if helper.has_file_path('fcine.bin') and helper.get_last_modified_time_file('fcine.bin') + 86400 < int(
                time.time()):
            helper.remove_file('fcine.bin')

        if helper.has_file_path('fcine.bin'):
            self.request.set_session(pickle.loads(helper.read_file('fcine.bin', True)))
        else:
            self.login()

    def get_token(self, response=None):
        if not response:
            response = self.request.get('%s/page/help/' % self.domain)

        self.token = re.search('csrfKey: "(.*)",', response).group(1)
        self.member_id = re.search('memberID: (\d+)', response).group(1)

        return self.token, self.member_id

    def login(self):
        self.get_token()

        params = {
            'login__standard_submitted': 1,
            'csrfKey': self.token,
            'auth': self.username,
            'password': self.password,
            'remember_me': 1,
            'remember_me_checkbox': 1
        }

        self.request.post('%s/login/' % self.domain, params)
        helper.write_file('fcine.bin', pickle.dumps(self.request.get_request_session()), True)

    def getCategory(self):
        response = self.request.get(self.domain)
        movies = Channel().get(response, 1)
        movies['page'] = 1
        return Category().get(response), movies

    def getChannel(self, channel, page=1):
        url = '%s?alphabet=all&page=%d' % (channel, page)
        response = self.request.get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        response = self.request.get(id)
        return Movie().get(response)

    def getLink(self, url):
        response = self.request.get(url)
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/findContent/" % self.domain
        params = {
            'term': text
        }
        response = self.request.post(url, params)
        return Channel().get(response, 1)
