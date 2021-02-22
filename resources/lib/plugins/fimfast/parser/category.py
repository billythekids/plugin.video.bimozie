#!/usr/bin/env python
# coding=utf-8
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('div#navbar-left > div.navbar-menu > li.navbar-menu-item')[:-1]:
            menu = item.select_one('a')
            category.append({
                'title': py2_encode(menu.text),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.navbar-submenu > li > a'):
            category.append({
                'title': py2_encode(item.text),
                'link': item.get('href')
            })

        return category

