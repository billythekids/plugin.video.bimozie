#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")
        for item in soup.select('ul.navbar-nav > li'):
            menu = item.select_one('a')
            if menu.get('target') is None:
                category.append({
                    'title': py2_encode(menu.text),
                    'link': "",
                    'subcategory': self.getsubmenu(item)
                })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li > a'):
            link = item.get('href')
            category.append({
                'title': py2_encode(item.text),
                'link': link
            })

        return category

