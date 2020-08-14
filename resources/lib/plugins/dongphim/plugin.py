import urllib, re, json
from utils.mozie_request import Request
from dongphim.parser.category import Parser as Category
from dongphim.parser.channel import Parser as Channel
from dongphim.parser.movie import Parser as Movie
import utils.xbmc_helper as XbmcHelper


class Dongphim:
    # domain = "https://dongphim.biz"
    domain = "https://dongphym.net"
    api = "https://dp.vodcdn.xyz"

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
                # http://dp.voocdn.xyz/subitems?mid=BG56xgbS&a=1593610184&type=all
                response = self.request.get('{}/content/subitems?mid={}&type=all'.format(self.api, mid.group(1)))
                response = json.loads(response)
                response = response.get('data').encode('utf-8', errors='ignore')

                eps = Movie().get(response)
        return eps

    def getLink(self, movie):
        link = "{}{}".format(self.domain, movie['link'].replace(self.domain, ""))
        response = self.request.get(link)
        return Movie().get_link(response, movie['link'], self.api)

    def search(self, text):
        url = "%s/content/search?t=kw&q=%s" % (self.domain, urllib.quote_plus(text))
        response = self.request.get(url)
        return Channel().get(response, 1)
