# -*- coding: utf-8 -*-
import json

from .. import xbmc_helper as helper
from ..mozie_request import Request
from ..pastebin import PasteBin

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def create_playlist(datas):
    master_playlist = """#EXTM3U
#EXT-X-VERSION:3
    """
    for data in datas:

        play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:{}\n#EXT-X-PLAYLIST-TYPE:VOD\n".format(
            data.get('duration'))

        for i in data.get('content'):
            play_list += "#EXTINF:{},\n".format(i.get('extinf'))
            play_list += "{}\n".format(i.get('url'))

        play_list += "#EXT-X-ENDLIST"
        url = PasteBin().dpaste(play_list, name='playoffsite', expire=60)
        master_playlist += create_master_playlist(url, data)

    url = PasteBin().dpaste(master_playlist, name='playoffsite', expire=60)
    return url


def create_master_playlist(url, data):
    return """
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH={},RESOLUTION={}
{}
    """.format(data.get('bandwidth'), data.get('resolution'), url)


def get_link(url, media):
    header = {
        'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
    }

    req = Request()
    url = url.replace('api/play', 'api/json')
    response = req.get(url, headers=header)
    response = json.loads(response)
    url = create_playlist(response.get('content').get('playlist'))

    return url, 'beststream'
