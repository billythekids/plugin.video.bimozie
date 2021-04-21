from hayghes.parser.category import Parser as Category
from hayghes.parser.channel import Parser as Channel
from hayghes.parser.movie import Parser as Movie
from six.moves.urllib.parse import quote_plus
from utils.mozie_request import Request


user_agent = (
    "Mozilla/5.0 (X11; Linux x86_64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/59.0.3071.115 Safari/537.36"
)

h = {
    'User-Agent': user_agent,
    'Accept-Encoding': 'utf-8'
}


class Hayghes:
    domain = "https://hayghes.net"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get('{}'.format(self.domain), headers=h)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")

        if page > 1:
            url = '%s%strang-%d.html' % (self.domain, channel, page)
        else:
            url = '%s%s' % (self.domain, channel)

        response = self.request.get(url, headers=h)
        return Channel().get(response, page)

    def getMovie(self, movie_url):
        url = '{}xem-phim.html'.format(movie_url)
        response = self.request.get(url, headers=h)
        return Movie().get(response, url)

    def getLink(self, movie):
        url = movie['link'].replace(self.domain, '')
        url = "%s%s" % (self.domain, url)
        response = self.request.get(url, headers=h)

        return Movie().get_link(response, self.domain, url, self.request)

    def search(self, text):
        url = "%s/tim-nang-cao/?keyword=%s" % (self.domain, quote_plus(text))
        response = self.request.get(url, headers=h)
        return Channel().get(response, 1)
