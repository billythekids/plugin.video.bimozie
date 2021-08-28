# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('div.menu-menunew-container ul#menu-menunew > li')

        for item in cats[1:]:
            menu = item.select_one('a')
            category.append({
                'title': py2_encode(menu.text.strip()),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.dropdown-menu > li > a'):
            category.append({
                'title': py2_encode(item.text),
                'link': item.get('href')
            })

        return category
