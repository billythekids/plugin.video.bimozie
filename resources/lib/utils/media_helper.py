from utils.link_parser import LinkParser


class MediaHelper:
    def __init__(self, media):
        self.media = media

    def resolve_link(self):
        if self.media and 'link' in self.media:
            return LinkParser(self.media['link']).get_link()[0]

    def resolve_subtitle(self):
        if 'subtitle' in self.media:
            pass
