#!/usr/bin/env python
# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('ul.nav-tabs > li'):
            menu = item.select_one('a')
            category.append({
                'title': py2_encode(menu.text),
                'link': menu.get("href")
            })
        return category

