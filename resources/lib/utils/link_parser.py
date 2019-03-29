# -*- coding: utf-8 -*-
import re
import utils.xbmc_helper as helper
from .hosts import fshare, imacdn, phimmoi, hydrax, fptplay, ok


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
        elif re.search('fptplay.net', self.url):

            return fptplay.get_link(self.url)
        elif re.search('sstreamgg.xyz', self.url) \
                or re.search('ggstream.me', self.url) \
                or re.search('hhstream.xyz', self.url) \
                or re.search('116.203.139.97', self.url) \
                or re.search('tstream.xyz', self.url):

            return self.get_sstreamgg()
        elif re.search('hls.phimmoi.net', self.url):
            helper.message('Phimmoi hls link parsing', 'Get Link')
            return phimmoi.get_link(self.url, self.media['origin_url'])
        elif re.search('hydrax.html', self.url):
            helper.message('hydrax link is not full supported yet', 'Get Link')
            return hydrax.get_link(self.url)
        elif re.search('youtube.com', self.url):

            return self.get_youtube()
        elif re.search('imacdn.com', self.url):

            return imacdn.get_link(self.url)
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

        return self.url, 'hls'

    def get_sstreamgg(self):
        url = self.url + "|Referer=https://vuviphim.com/"
        return url, '720'
