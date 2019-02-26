import urllib
import json
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
        if page == 1:
            response = Request().get(baseurl)
            api_type, api_value = Channel().get_api_type(response)
        else:
            api_type, api_value = channel.split('|')

        # https://fimfast.com/api/v2/films/cinema?offset=24&limit=24
        if api_type:
            if api_type == 'cinema':
                url = '%s/films/cinema?offset=%d&limit=24' % (self.api, (page - 1) * 24)
            else:
                url = '%s/films?offset=%d&limit=24&%s=%s' % (self.api, (page - 1) * 24, api_type, api_value)

        response = Request().get(url, headers={
            'referer': baseurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })

        return Channel().get(response, page, api_type, api_value)

    def getMovie(self, id):
        movieurl = '%s/%s' % (self.domain, id)
        response = Request().get(movieurl)
        fid, epid = Movie().get_movie_id(response)
        url = '%s/films/%s/episodes/%s' % (self.api, fid, epid)

        response = Request().get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })

        response = json.loads(response)
        url = '%s/films/%s/episodes?sort=name' % (self.api, fid)
        if 'ova' in response: url += '&ova=true'

        response = Request().get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })
        return Movie().get(response, fid)

    def getLink(self, movie):
        movieurl = '%s%s' % (self.domain, movie['link'])
        response = Request().get(movieurl)
        fid, epid = Movie().get_movie_id(response)
        url = '%s/films/%s/episodes/%s' % (self.api, fid, epid)

        response = Request().get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })

        return Movie().get_link(response)

    def search(self, text):
        url = "%ssearch/%s" % (self.domain, urllib.quote_plus(text))
        response = Request().get(url)
        return Channel().get(response, 1)
