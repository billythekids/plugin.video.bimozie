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
        return Category().get(response), None

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, '')
        baseurl = '%s%s' % (self.domain, channel)
        if page == 1:
            response = Request().get(baseurl)
        else:
            baseurl = "{}?page={}".format(baseurl, page)
            response = Request().get(baseurl)

        return Channel().get(response, page)

    def getMovie(self, id):
        movieurl = '%s%s' % (self.domain, id)
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
        # https://fimfast.com/api/v2/search?q=nu%20hon&limit=12
        url = "%s/search?q=%s&limit=12" % (self.api, urllib.quote_plus(text))
        response = Request().get(url, headers={
            'referer': self.domain,
            'x-requested-with': 'XMLHttpRequest',
        })

        return Channel().get(response, 1)
