# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('ul.nav__list > li.nav__list-item')
        for item in cats:
            menu = item.select_one('a')
            if menu:
                category.append({
                    'title': py2_encode(menu.find(text=True, recursive=False).strip()),
                    'link': menu.get("href"),
                    'subcategory': self.getsubmenu(item)
                })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.nav__sub-list > li > a'):
            category.append({
                'title': py2_encode(item.find(text=True, recursive=False).strip()),
                'link': item.get('href')
            })

        return category
