from utils.mozie_request import Request
from xomphimhay.parser.category import Parser as Category
from xomphimhay.parser.channel import Parser as Channel
from xomphimhay.parser.movie import Parser as Movie
import urllib, pickle, time
import utils.xbmc_helper as helper


class Xomphimhay:
    domain = "https://xem-phim.tv"
    api = "https://xem-phim.tv/api/v1/episodes/%s/player"

    def __init__(self):
        self.request = Request(session=True)
        if helper.has_file_path('xomphimhay.bin') and helper.get_last_modified_time_file('xomphimhay.bin') + 43200 < int(time.time()):
            helper.remove_file('xomphimhay.bin')

        if helper.has_file_path('xomphimhay.bin'):
            with open(helper.get_file_path('xomphimhay.bin')) as f:
                self.request.set_session(pickle.load(f))
            cookies_jar = self.request.get_request_session().cookies
            cookies_jar.set('vietnamese', 'true', domain='xomphimhay.com', path='/')

    def updateSession(self):
        if not helper.has_file_path('xomphimhay.bin'):
            helper.write_file('xomphimhay.bin', '')

        with open(helper.get_file_path('xomphimhay.bin'), 'wb+') as f:
            pickle.dump(self.request.get_request_session(), f)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s/trang-%d/' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url)
        return Channel().get(response)

    def getMovie(self, url):
        response = self.request.get(url)
        url = Movie().get_movie_link(response)
        response = self.request.get(url)
        self.updateSession()
        return Movie().get(response, url)

    def getLink(self, movie):
        # https://xomphimhay.com/api/v1/episodes/1155146/player
        url, mid = movie['link'].split('|')
        response = self.request.get(self.api % mid)
        return Movie().get_link(response, self.domain, self.request, url)

    def search(self, text, page=1):
        url = "%s/tim-kiem/%s/" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response)
