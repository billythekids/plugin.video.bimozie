#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup

class Parser:
    def get(self, response):

        category = []
        try:
            response = response.encode('latin-1')
        except: pass
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('div#menu > ul.top-menu > li')[1:-1]:
            category.append({
                'title': item.select_one('a').text.encode('utf8'),
                'link': item.select_one('a').get('href'),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.sub-menu > li'):
            category.append({
                'title': item.select_one('a').text.encode('utf8'),
                'link': item.select_one('a').get('href')
            })
        return category
