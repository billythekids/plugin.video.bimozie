import re
from utils.mozie_request import Request
from fcine.parser.category import Parser as Category
from fcine.parser.channel import Parser as Channel
from fcine.parser.movie import Parser as Movie
import utils.xbmc_helper as helper


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

    def get_token(self, response=None):
        if not response:
            response = self.request.get('%s/page/help/' % self.domain)

        self.token = re.search('csrfKey: "(.*)",', response).group(1)
        self.member_id = re.search('memberID: (\d+)', response).group(1)

        return self.token, self.member_id

    def login(self, username, password, header):
        params = {
            'login__standard_submitted': 1,
            'csrfKey': self.token,
            'auth': username,
            'password': password,
            'remember_me': 1,
            'remember_me_checkbox': 1
        }
        return self.request.post('%s/login/' % self.domain, params, headers=header)

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
        self.get_token()
        response = self.login(
            self.username,
            self.password,
            {'referer': id})
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
