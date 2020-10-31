import urllib
import json
from utils.mozie_request import Request
from fimfast.parser.category import Parser as Category
from fimfast.parser.channel import Parser as Channel
from fimfast.parser.movie import Parser as Movie


class Fimfast:
    domain = "https://phim1080.me"
    api = "https://phim1080.me/api/v2"

    def __init__(self):
        self.request = Request(session=True)

    def getCategory(self):
        response = self.request.get(self.domain)
        return Category().get(response), Channel().get(response, 1)

    def getChannel(self, channel, page=1):
        channel = channel.replace(self.domain, '')
        baseurl = '%s%s' % (self.domain, channel)
        if page == 1:
            response = self.request.get(baseurl)
        else:
            baseurl = "{}?page={}".format(baseurl, page)
            response = self.request.get(baseurl)

        return Channel().get(response, page)

    def getMovie(self, id):
        movieurl = '%s%s' % (self.domain, id)
        response = self.request.get(movieurl)
        fid, epid = Movie().get_movie_id(response)
        url = '%s/films/%s/episodes?sort=name' % (self.api, fid)

        response = self.request.get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })

        response = json.loads(response)
        url = '%s/films/%s/episodes?sort=name' % (self.api, fid)
        if 'ova' in response: url += '&ova=true'

        response = self.request.get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })
        return Movie().get(response, fid)

    def getLink(self, movie):
        movieurl = '%s%s' % (self.domain, movie['link'])
        response = self.request.get(movieurl)
        fid, epid = Movie().get_movie_id(response)
        url = '%s/films/%s/episodes/%s/true' % (self.api, fid, epid)

        response = self.request.get(url, headers={
            'referer': movieurl,
            'authority': 'fimfast.com',
            'x-requested-with': 'XMLHttpRequest',
        })

        return Movie().get_link(response, movieurl)

    def search(self, text):
        # https://fimfast.com/api/v2/search?q=nu%20hon&limit=12
        # https://fimfast.com/tim-kiem/sieu%20diep%20vien
        url = "%s/tim-kiem/%s" % (self.domain, text)
        response = self.request.get(url, headers={
            'referer': self.domain,
            # 'x-requested-with': 'XMLHttpRequest',
        })

        return Channel().get(response, 1)
