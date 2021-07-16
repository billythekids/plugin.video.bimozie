# -*- coding: utf-8 -*-
import re

from . import xbmc_helper as helper
from .link_parser import LinkParser
from six.moves.urllib.parse import quote

try:
    from urllib.parse import urlencode
except ImportError:
    from urllib import urlencode


class MediaHelper:
    @staticmethod
    def resolve_link(media):
        link = media['link']
        mediatype = '720'

        link = MediaHelper.build_url(link)
        media['link'] = link

        if 'resolve' in media and not media['resolve']:
            if media and 'link' in media:
                link, mediatype = LinkParser(media).get_link()

        if not link:
            helper.message('Cannot find media url %s' % media['link'], 'Link not found')
            media['link'] = None
            return

        link = MediaHelper.build_url(link)
        media['link'] = link
        return mediatype

    @staticmethod
    def resolve_subtitle(media):
        if 'subtitle' in media:
            pass

    @staticmethod
    def build_url(link):
        r = re.search('^https?:', link)
        if not r:
            return 'https:%s' % link
        return link
