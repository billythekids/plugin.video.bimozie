# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('ul#menu-menu > li')

        for item in cats:
            menu = item.select_one('a')
            if menu.get("href") == '/': continue # skip 1st
            category.append({
                'title': py2_encode(menu.text.strip()),
                'link': menu.get("href")
                # 'subcategory': Parser.getsubmenu(item)
            })
        return category
