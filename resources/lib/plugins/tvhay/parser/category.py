#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('ul.menu > li'):
            menu = item.select_one('h3 > a')
            if menu.get('href') == 'http://tvhay.org': continue
            category.append({
                'title': py2_encode(menu.text),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        if xpath.select('ul > li'):
            for item in xpath.select('ul > li > h3 > a'):
                category.append({
                    'title': py2_encode(item.text),
                    'link': item.get('href')
                })

        return category

