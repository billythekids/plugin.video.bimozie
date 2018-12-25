#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
import urllib
import re


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('ul.menu > li'):
            menu = item.select_one('h3 > a')
            if menu.get('href') == 'http://tvhay.org': continue
            category.append({
                'title': menu.text.encode("utf-8"),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li > h3 > a'):
            category.append({
                'title': item.text.encode("utf-8"),
                'link': item.get('href')
            })

        return category

