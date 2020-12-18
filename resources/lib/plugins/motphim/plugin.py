from utils.mozie_request import Request
from motphim.parser.category import Parser as Category
from motphim.parser.channel import Parser as Channel
from motphim.parser.movie import Parser as Movie
import utils.xbmc_helper as helper
import urllib, pickle


class Motphim:
    domain = "https://motphjm.net"
    api = "https://api.mpapis.xyz"

    def __init__(self):
        self.request = Request(session=True)
        # if helper.has_file_path('motphim.bin'):
        #     with open(helper.get_file_path('motphim.bin')) as f:
        #         self.request.set_session(pickle.load(f))

    def updateSession(self):
        with open(helper.get_file_path('motphim.bin'), 'wb') as f:
            pickle.dump(self.request.get_request_session(), f)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = channel.replace(".html", "")
            url = '%s%s/%d' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        response = self.request.get("%s%s" % (self.domain, url))
        url = Movie().get_movie_link(response)
        response = self.request.get("%s%s" % (self.domain, url))
        # self.updateSession()
        return Movie().get(response)

    def getLink(self, movie):
        url = "%s%s" % (self.domain, movie['link'])
        response = self.request.get(url)
        # self.updateSession()
        return Movie().get_link(response, self.request, self.api, self.domain, url)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
