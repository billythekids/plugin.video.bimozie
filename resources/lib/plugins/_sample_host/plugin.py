from _sample_host.parser.category import Parser as Category
from _sample_host.parser.channel import Parser as Channel
from _sample_host.parser.movie import Parser as Movie
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


class Sample:
    domain = "https://test.com"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get('{}/'.format(self.domain), headers=h)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        response = self.request.get(channel, headers=h)
        return Channel().get(response, page)

    def getMovie(self, movie_url):
        response = self.request.get(movie_url, headers=h)
        return Movie().get(response, movie_url)

    def getLink(self, movie):
        url = movie['link'].replace(self.domain, '')
        url = "%s/%s" % (self.domain, url)
        response = self.request.get(url, headers=h)
        return Movie().get_link(response, self.domain, url, self.request)

    def search(self, text):
        url = "%s/tim-nang-cao/?keyword=%s" % (self.domain, quote_plus(text))
        response = self.request.get(url, headers=h)
        return Channel().get(response, 1)
