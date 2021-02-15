#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('div#nav > ul > li'):
            if item.get('class') is not None: continue
            menu = item.select_one('a')
            link = self.getLink(menu)
            cat = {
                'title': menu.text.encode("utf-8"),
                'link': link,
            }
            if not link:
                cat['subcategory'] = self.getsubmenu(item)
            category.append(cat)
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li > a'):

            category.append({
                'title': item.text.encode("utf-8"),
                'link': self.getLink(item)
            })

        return category

    def getLink(self, menu):
        return menu.get("href") is not None and menu.get("href")[0].encode("utf-8") is '/' \
                   and menu.get("href")[1:] or menu.get("href")
