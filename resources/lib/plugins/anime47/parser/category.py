# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup
import urllib
import re


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")
        for item in soup.select('ul#mega-menu-1 > li'):
            menu = item.select_one('a')
            if menu.get('href') == '/': continue
            if menu.get('href') and menu.get('href').endswith('huong-dan.html'): continue

            category.append({
                'title': u''.join(menu.text).encode('latin1').strip(),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li'):
            category.append({
                'title': item.select_one('a').text.encode("latin1"),
                'link': item.select_one('a').get('href')
            })

        return category

