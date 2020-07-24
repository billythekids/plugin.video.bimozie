import urllib
import re
from utils.mozie_request import Request
from hphim.parser.category import Parser as Category
from hphim.parser.channel import Parser as Channel
from hphim.parser.movie import Parser as Movie


class Hphim:
    domain = "http://biphimz.tv"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        if page > 1:
            channel = re.sub(r'i(\d+).html', 'i%d.html' % page, channel)
            url = '%s%s' % (self.domain, channel)
        else:
            url = '%s%s' % (self.domain, channel)
        response = Request().get(url)
        return Channel().get(response, page)

    def getMovie(self, id):
        url = '%s%s' % (self.domain, id)
        url = Movie().get_movie_link(Request().get(url))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        url = '%s%s' % (self.domain, movie['link'])
        response = Request().get(url)
        return Movie().get_link(response, self.domain, url)

    def search(self, text):
        # text = urllib.quote_plus(text)
        url = "%s/searchajax" % self.domain
        response = Request().post(url, params={
            'search': text
        })
        return Channel().search_result(response)
