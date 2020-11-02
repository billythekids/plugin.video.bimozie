# -*- coding: utf-8 -*-
import re, json
from utils.mozie_request import Request
import utils.xbmc_helper as helper
from urlparse import urlparse, parse_qs
from urllib import urlencode
from utils.pastebin import PasteBin


def create_playlist(text, idfile, domains):
    data = json.loads(text)
    domains = json.loads(domains)

    play_list = "#EXTM3U\n#EXT-X-VERSION:3\n#EXT-X-TARGETDURATION:{}\n#EXT-X-PLAYLIST-TYPE:VOD\n".format(
        data.get('tgdr'))

    j = 0
    for i in range(len(data.get('data')[0])):
        domain = domains[j]
        j+=1
        if j >= len(domains): j = 0
        play_list += "#EXTINF:{},\n".format(data.get('data')[0][i])
        play_list += "https://{}/stream/linkv2/{}/{}/{}/{}.html\n".format(domain, data.get('quaity'),
                                                                          data.get('idplay'),
                                                                          idfile, data.get('data')[1][i])

    play_list += "#EXT-X-ENDLIST"
    return play_list


def get_link(url, media):
    # https://play.playoffsite.xyz/play/v1/5f753b4889b8c5269a591e29
    # https://play.playoffsite.xyz/apiv1/playhq/5f6581f43036707a6803e61c
    m_id = re.search(r'v1/(.*)', url)
    header = {
        'Referer': url
    }

    req = Request()

    if m_id:
        m_id = m_id.group(1)

        # get domain list https://play.playoffsite.xyz/play/v1/5f6581f43036707a6803e61c
        # var DOMAIN_LIST =
        response = req.get("https://play.playoffsite.xyz/play/v1/{}".format(m_id), headers=header)
        domains = re.search(r'var DOMAIN_LIST = (\[.*\])', response).group(1)
        idfile = re.search(r'var idfile = "(.*)";', response).group(1)

        response = req.post("https://play.playoffsite.xyz/apiv1/playhq/{}".format(m_id), headers=header, data="")
        playlist = create_playlist(response, idfile, domains)
        url = PasteBin().dpaste(playlist, name='playoffsite', expire=60)
        # url = helper.write_file('playlist.strm', url)

    return url, 'Tvhay'
