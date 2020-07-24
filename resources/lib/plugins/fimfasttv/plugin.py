import urllib
import json
from utils.mozie_request import Request
from fimfast.parser.category import Parser as Category
from fimfast.parser.channel import Parser as Channel
from fimfast.parser.movie import Parser as Movie


class Fimfast:
    domain = "http://fimfast.tv"
    api = "http://fimfast.tv/wp-content/themes/halimmovies/player.php"

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
            baseurl = "{}/page/{}".format(baseurl, page)
            response = self.request.get(baseurl)

        return Channel().get(response, page, self.domain)

    def getMovie(self, id):
        id = id.replace(self.domain, "")
        movieurl = '%s%s' % (self.domain, id)
        response = self.request.get(movieurl)

        return Movie().get(response)

    def getLink(self, movie):
        episode_slug, server_id, post_id = movie.get('link').split(',')
        response = self.request.get(self.api, headers={
            'x-requested-with': 'XMLHttpRequest',
        }, params={
            'episode_slug': episode_slug, 'server_id': server_id, 'post_id': post_id
        })

        return Movie().get_link(response)

    def search(self, text):
        # https://fimfast.com/api/v2/search?q=nu%20hon&limit=12
        # https://fimfast.com/tim-kiem/sieu%20diep%20vien
        url = "%s/search/%s" % (self.domain, text)
        response = self.request.get(url, headers={
            'referer': self.domain,
            # 'x-requested-with': 'XMLHttpRequest',
        })

        return Channel().get(response, 1)
