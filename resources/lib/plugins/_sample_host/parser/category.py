# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
from utils.xbmc_helper import text_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")
        for item in soup.select('ul#mega-menu-1 > li'):
            menu = item.select_one('a')

            category.append({
                'title': text_encode(menu.text),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li'):
            category.append({
                'title': text_encode(item.select_one('a').text),
                'link': item.select_one('a').get('href')
            })

        return category

