# -*- coding: utf-8 -*-
import re
import utils.xbmc_helper as helper
from urllib import urlencode
from .hosts import fshare, imacdn, phimmoi, hydrax, fptplay, ok, vtv16, hls_hydrax, dongphim, fembed, hdclub

class LinkParser:
    def __init__(self, media):
        self.media = media
        self.url = media['link']

    def get_link(self):
        print("Find link source of %s" % self.url)
        if re.search('ok.ru', self.url):
            return ok.get_link(self.url)

        elif re.search('openload.co', self.url):
            return self.get_link_openload()

        elif re.search('fshare.vn', self.url):
            return self.get_link_fshare()

        elif re.search('dailymotion.com', self.url):
            return self.get_link_dailymotion()

        elif re.search('fembed.com', self.url):
            return fembed.get_link(self.url)

        elif re.search('24hd.club', self.url):
            return hdclub.get_link(self.url)

        elif re.search('fptplay.net', self.url):
            helper.message('FPTPlay hls link parsing', 'Get Link')
            return fptplay.get_link(self.url)

        elif re.search('sstreamgg.xyz', self.url) \
                or re.search('ggstream.me', self.url) \
                or re.search('hhstream.xyz', self.url) \
                or re.search('116.203.139.97', self.url) \
                or re.search('tstream.xyz', self.url):
            return self.get_sstreamgg()

        elif re.search('hls.phimmoi.[net|link]', self.url):
            helper.message('Phimmoi hls link parsing', 'Get Link')
            return phimmoi.get_link(self.url, self.media['originUrl'])

        elif re.search('hydrax.html', self.url):
            helper.message('hydrax link parsing', 'Get Link')
            return hydrax.get_vip_hydrax(self.url, self.media)
        elif re.search('hydrax.net/watch', self.url):
            helper.message('hydrax link parsing', 'Get Link')
            return hydrax.get_guest_hydrax(self.url, self.media)

        elif re.search('youtube.com', self.url):
            return self.get_youtube()

        elif re.search('imacdn.com', self.url):
            helper.message('imacdn HFF', 'Movie Found')
            return imacdn.get_link(self.url), 'hls5'

        elif re.search('vtv16.com', self.url):
            return vtv16.get_link(self.url)

        elif re.search('hls.hydrax.net', self.url):
            return hls_hydrax.get_link(self.url, self.media), 'hls5'

        elif re.search('dgo.dongphim.net', self.url):
            # return self.url + "|Origin=http://dongphim.net", 'hls1'
            return dongphim.get_link(self.url, self.media)

        elif self.url.endswith('m3u8'):
            return self.get_m3u8()

        return self.url, 'unknow'

    def get_youtube(self):
        self.url = self.url.replace(re.search('^http.*(\?.*)', self.url).group(1), '')
        try:
            import resolveurl
            re.sub('(^http.*)\?', '\1', self.url)
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_openload(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_dailymotion(self):
        try:
            import resolveurl
            stream_url = resolveurl.resolve(self.url)
            return stream_url, '720'
        except:
            return None

    def get_link_fshare(self):
        if not helper.getSetting('fshare.username'):
            helper.message('Required username/password to get fshare.vn link, open addon settings', 'Login Required')

        if helper.getSetting('fshare.enable'):
            return fshare.FShare(
                self.url,
                helper.getSetting('fshare.username'),
                helper.getSetting('fshare.password')
            ).get_link(), '1080'
        else:
            return fshare.FShare(self.url).get_link(), '1080'

    def get_m3u8(self):
        # support to run with inputstream.adaptive
        if re.search('51.15.90.176', self.url):  # skip this for phimbathu & bilutv
            return self.url, 'hls5'

        # hls-streaming.phimgi.net
        if re.search('hls-streaming.phimgi.net', self.url):  # skip this for phimbathu & bilutv
            url = self.url + "|%s" % urlencode({
                'Origin': 'https://phimgi.net',
                'Referer': self.media['originUrl']
            })
            return url, 'hls5'

        return self.url, 'hls'

    def get_sstreamgg(self):
        url = self.url + "|Referer=https://vuviphim.com/"
        return url, '720'
