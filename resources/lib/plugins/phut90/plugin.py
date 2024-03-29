import re
from utils.mozie_request import Request
from phut90.parser.channel import Parser as Channel
from phut90.parser.movie import Parser as Movie


class Phut90:
    domain = "https://mitom.90phuttttt.xyz"

    def getCategory(self):
        channel = Channel.get(Request().get(self.domain))
        return [], channel

    def getMovie(self, id):
        id = id.replace(self.domain, '')
        url = "%s%s" % (self.domain, id)
        response = Request().get(url)
        return Movie().get(response, url, self.domain)

    def search(self, text):
        return None
