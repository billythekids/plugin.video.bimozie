from utils.link_parser import LinkParser
import utils.xbmc_helper as helper
import re


class MediaHelper:
    @staticmethod
    def resolve_link(media):
        link = media['link']
        mediatype = '720'

        r = re.search('^https?:', link)
        if not r:
            link = 'http:%s' % link
            media['link'] = link

        if 'resolve' in media and not media['resolve']:
            print('Resolve %s' % link)
            if media and 'link' in media:
                link, mediatype = LinkParser(media).get_link()

        if not link:
            helper.message('Cannot find media url %s' % media['link'], 'Link not found')
            return

        media['link'] = link
        return mediatype

    @staticmethod
    def resolve_subtitle(media):
        if 'subtitle' in media:
            pass
