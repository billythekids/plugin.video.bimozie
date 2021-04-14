# -*- coding: utf-8 -*-
import json
import re

from ..mozie_request import Request

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


def create_playlist(text, idfile, domains, headers):
    data = json.loads(text)
    domains = json.loads(domains)

    play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:{}\n#EXT-X-PLAYLIST-TYPE:VOD\n".format(
        data.get('tgdr'))

    j = 0
    for i in range(len(data.get('data')[0])):
        domain = domains[j]
        j += 1
        if j >= len(domains): j = 0
        play_list += "#EXTINF:{},\n".format(data.get('data')[0][i])
        play_list += "https://{}/stream/linkv2/{}/{}/{}/{}.html\n".format(domain, data.get('quaity'),
                                                                          data.get('idplay'),
                                                                          idfile, data.get('data')[1][i],
                                                                          urlencode(headers))

    play_list += "#EXT-X-ENDLIST"
    return play_list


def create_master_playlist(url):
    return """#EXTM3U
#EXT-X-VERSION:3
#EXT-X-STREAM-INF:PROGRAM-ID=1,BANDWIDTH=648224,RESOLUTION=640x360
{}
    """.format(url)


def get_link(url, media):
    # https://play.playoffsite.xyz/play/v1/5f753b4889b8c5269a591e29
    # https://play.playoffsite.xyz/apiv1/playhq/5f6581f43036707a6803e61c
    m_id = re.search(r'v1/(.*)', url)
    header = {
        'referer': url
        # 'Referer': 'http://tvhayz.net'
    }

    req = Request()

    if m_id:
        m_id = m_id.group(1)

        # get domain list https://play.playoffsite.xyz/play/v1/5f6581f43036707a6803e61c
        # var DOMAIN_LIST =
        link = "https://play.vstreamplay.xyz/play/v1/{}".format(m_id)
        response = req.get(link, headers=header)
        domains = re.search(r'var DOMAIN_LIST = (\[.*\])', response).group(1)
        idfile = re.search(r'var idfile = "(.*)";', response).group(1)
        iduser = re.search(r'var idUser = "(.*)";', response).group(1)

        header = {
            'referer': 'https://play.vstreamplay.xyz/',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 12_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148',
            'verifypeer': 'false'
            # 'Content-Type': 'application/x-www-form-urlencoded'
        }
        response = req.post("https://api-sing.vstreamplay.xyz/apiv2/{}/{}".format(iduser, idfile), headers=header,
                            params={
                                'referrer': 'http://tvhai.org',
                                'typeend': 'html'
                            })
        response = json.loads(response)
        url = response.get('data')
        # req.head("https://m3u8.playoffsite.xyz/api/v1/png/{}".format(idfile), headers=header)
        # url = req.get_request().history[0].headers['Location']

        # response = req.post("https://api.playoffsite.xyz/apiv1/playhq/{}".format(m_id), headers=header, params="referrer=http%3A%2F%2Ftvhayz.net")
        # header = {
        #     'referer': link,
        #     'verifypeer': 'false',
        #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36 Edg/88.0.705.74'
        # }
        # playlist = create_playlist(response, idfile, domains, header)
        # url = PasteBin().dpaste(playlist, name='playoffsite', expire=60)
        # playlist = create_master_playlist(url)
        # url = PasteBin().dpaste(playlist, name='playoffsite', expire=60)
        # media['originUrl'] = link
        # return streamlink.get_link(url, media)
        return url + "|%s" % urlencode(header), 'hl3'

    return url, 'Tvhay'
