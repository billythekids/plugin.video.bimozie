# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('ul#mega-menu-1 > li')

        for item in cats:
            menu = item.select_one('a')
            if menu.get("href") == '/': continue # skip 1st
            category.append({
                'title': py2_encode(menu.text.strip()),
                'link': menu.get("href"),
                'subcategory': Parser.getsubmenu(item)
            })
        return category

    @staticmethod
    def getsubmenu(xpath):
        category = []
        if xpath.select('ul'):
            for item in xpath.select('ul > li > a'):
                category.append({
                    'title': py2_encode(item.text),
                    'link': item.get('href')
                })

        return category
