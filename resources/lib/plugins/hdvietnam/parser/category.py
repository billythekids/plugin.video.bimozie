# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self):
        category = [
            {
                'title': 'Fshare.vn',
                'link': 'http://www.hdvietnam.com/forums/fshare-vn.33/'
            },
            {
                'title': 'WEB-DL, HDTV',
                'link': 'http://www.hdvietnam.com/forums/web-dl-hdtv.271/'
            },
            {
                'title': 'Bluray Remux',
                'link': 'http://www.hdvietnam.com/forums/bluray-remux.324/'
            },
            {
                'title': 'HD, SD',
                'link': 'http://www.hdvietnam.com/forums/mhd-sd.77/'
            },
            {
                'title': 'Bluray nguyên gốc',
                'link': 'http://www.hdvietnam.com/forums/bluray-nguyen-goc.78/'
            },
        ]

        return category
