import urllib
import re
from utils.mozie_request import Request
from fcine.parser.category import Parser as Category
from fcine.parser.channel import Parser as Channel
from fcine.parser.movie import Parser as Movie


class Fcine:
    domain = "https://fcine.net"

    def __init__(self):
        self.request = Request(header={
            'User-Agent': 'Mozilla/5.0',
            'origin': 'https://fcine.net',
            'referer': 'https://fcine.net/login/',
        }, session=True)

    def get_token(self, response):
        self.token = re.search('csrfKey: "(.*)",', response).group(1)
        self.member_id = re.search('memberID: (\d+)', response).group(1)
        return self.token, self.member_id

    def login(self, username, password):
        params = {
            'login__standard_submitted': 1,
            'csrfKey': self.token,
            'auth': username,
            'password': password,
            'remember_me': 0,
            'remember_me_checkbox': 1
        }
        self.request.post('%s/login/' % self.domain, params)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        url = '%s?alphabet=all&page=%d' % (channel, page)
        response = self.request.get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        response = self.request.get(id)
        self.get_token(response)
        self.login('billythekidsde@gmail.com', '123456')
        response = self.request.get(id)
        return Movie().get(response)

    def getLink(self, url):
        response = self.request.get(url)
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/findContent/" % (self.domain)
        params = {
            'term': text
        }
        response = self.request.post(url, params)
        return Channel().get(response, 1)
