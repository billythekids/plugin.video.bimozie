import re
from utils.mozie_request import Request
from thuckhuya.parser.channel import Parser as Channel
from thuckhuya.parser.movie import Parser as Movie


class Thuckhuya:
    domain = "http://thuckhuya.me"

    def getCategory(self):
        channel = Channel.get(Request().get(self.domain))
        return [], channel

    def getMovie(self, url):
        response = Request().get(url)
        return Movie().get(response, url)

    def search(self, text):
        return None
