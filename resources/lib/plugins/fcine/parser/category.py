#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import re
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")
        items = soup.select('li.ipsDrawer_itemParent > h4.ipsDrawer_title')
        for item in items[1:]:
            menu = item.select_one('a')
            category.append({
                'title': py2_encode(menu.text),
                'link': '',
                'subcategory': self.getsubmenu(item.parent)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.ipsDrawer_list > li > a'):
            link = item.get('href')
            if not re.search('https', link): continue
            category.append({
                'title': py2_encode(item.text),
                'link': item.get('href')
            })

        return category

