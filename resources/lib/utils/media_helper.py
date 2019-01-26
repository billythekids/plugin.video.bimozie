from utils.link_parser import LinkParser
import re


class MediaHelper:
    def __init__(self, media):
        self.media = media

    def resolve_link(self):
        link = self.media['link']
        if 'resolve' in self.media and self.media['resolve'] is not True:
            if self.media and 'link' in self.media:
                link =  LinkParser(link).get_link()[0]

        r = re.search('^https?:', link)
        if not r:
            link = 'http:%s' % link

        return link

    def resolve_subtitle(self):
        if 'subtitle' in self.media:
            pass
