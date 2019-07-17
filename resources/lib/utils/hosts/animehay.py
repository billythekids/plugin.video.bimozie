import re
import json
from urlparse import urlparse
from utils.mozie_request import Request


def get_link(url):
    req = Request()

    req.get(url, redirect=True)
    response = req.get_request()
    location = response.history[0].headers['Location']

    id = re.search('id=(.*)', location).group(1)
    base_url = urlparse(location)
    base_url = base_url.scheme + '://' + base_url.netloc

    return '%s/hls/%s/%s.playlist.m3u8' % (base_url, id, id)

    # POST http://sl2.animehay.tv/vl/{id}
    # response = json.loads(req.post('%s/vl/%s' % (base_url, id), headers={
    #     'Referer': location
    # }))

    # if '720p' in response:
    #     create_playlist(response['720p'])
    #
    # return None


def create_playlist(data):
    print(data)
