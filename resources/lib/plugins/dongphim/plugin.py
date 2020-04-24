import urllib, re, json
from utils.mozie_request import Request
from dongphim.parser.category import Parser as Category
from dongphim.parser.channel import Parser as Channel
from dongphim.parser.movie import Parser as Movie
import utils.xbmc_helper as XbmcHelper


class Dongphim:
    domain = "https://www.dongphim.net"

    def __init__(self):
        self.request = Request()

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            url = '%s%s&p=%d' % (self.domain, channel, page - 1)
        else:
            url = '%s%s' % (self.domain, channel)
        response = self.request.get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        response = self.request.get(id)
        eps = Movie().get(response)

        if len(eps.get('group').get(eps.get('group').keys()[0])) == 0:
            mid = re.search(r'data-playlist-contain="(.*?)"', response)
            if mid:
                # https://stats.dongphim.net/content/subitems?mid=DMnhnQL0&a=1587703526&type=all
                response = self.request.get('https://stats.dongphim.net/content/subitems?mid={}&a=1587703526&type=all'.format(mid.group(1)))
                response = json.loads(response)
                response = response.get('data').encode('utf-8', errors='ignore')
                print response
                eps = Movie().get(response)
        return eps

    def getLink(self, movie):
        response = self.request.get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%s/content/search?t=kw&q=%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response, 1)
