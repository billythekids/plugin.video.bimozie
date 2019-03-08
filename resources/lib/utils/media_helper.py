from utils.link_parser import LinkParser
import re


class MediaHelper:
    @staticmethod
    def resolve_link(media):
        link = media['link']
        mediatype = '720'
        if 'resolve' in media and not media['resolve']:
            print('Resolve %s' % link)
            if media and 'link' in media:
                link, mediatype = LinkParser(link).get_link()

        r = re.search('^https?:', link)
        if not r:
            link = 'http:%s' % link

        media['link'] = link
        return mediatype

    @staticmethod
    def resolve_subtitle(media):
        if 'subtitle' in media:
            pass
