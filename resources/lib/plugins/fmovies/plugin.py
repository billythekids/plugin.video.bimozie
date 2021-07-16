from .parser.category import Parser as Category
from .parser.channel import Parser as Channel
from .parser.movie import Parser as Movie
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


class fmovies:
    domain = "https://fmovies.to"

    def __init__(self):
        self.request = Request(h, session=True)

    def getCategory(self):
        response = self.request.get('{}/home'.format(self.domain), headers=h)
        return Category().get(response), Channel().getTop(response)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, "")
        baseurl = "{}{}".format(self.domain, channel)

        if page == 1:
            response = self.request.get(baseurl)
        else:
            baseurl = "{}?page={}".format(baseurl, page)
            response = self.request.get(baseurl)

        return Channel().get(response, page)

    def getMovie(self, movie_url):
        movie_url = '%s%s' % (self.domain, movie_url)

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
