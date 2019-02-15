import urllib
from utils.mozie_request import Request
from fimfast.parser.category import Parser as Category
from fimfast.parser.channel import Parser as Channel
from fimfast.parser.movie import Parser as Movie


class Fimfast:
    domain = "https://fimfast.com"
    api = "https://fimfast.com/api/v2"

    def getCategory(self):
        response = Request().get(self.domain)
        return Category().get(response)

    def getChannel(self, channel, page=1):
        baseurl = '%s%s' % (self.domain, channel)
        # if page == 1:
        response = Request().get(baseurl)
        api_type = Channel().get_api_type(response)

        # https://fimfast.com/api/v2/films?offset=24&limit=24&type=country.han-quoc
        url = '%s/film?offset=%d&&limit=24&type=%s' % (self.api, page*24, api_type)
        response = Request().get(url, headers={
            'referer': baseurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })
        print(response.encode('utf-8'))

        return Channel().get(response, page)

    def getMovie(self, id):
        url = Movie().get_movie_link(Request().get(id))
        response = Request().get(url)
        return Movie().get(response)

    def getLink(self, movie):
        response = Request().get(movie['link'])
        return Movie().get_link(response)

    def search(self, text):
        url = "%ssearch/%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
