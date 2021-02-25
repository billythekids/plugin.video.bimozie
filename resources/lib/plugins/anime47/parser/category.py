# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


def text(txt):
    try:
        return txt.encode('latin1').decode('utf-8').strip()
    except:
        return py2_encode(txt, 'latin1').decode('utf-8').strip()


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")
        for item in soup.select('ul#mega-menu-1 > li'):
            menu = item.select_one('a')
            if menu.get('href') == '/': continue
            if menu.get('href') and menu.get('href').endswith('huong-dan.html'): continue

            category.append({
                'title': text(menu.text),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li'):
            category.append({
                'title': text(item.select_one('a').text),
                'link': item.select_one('a').get('href')
            })

        return category

