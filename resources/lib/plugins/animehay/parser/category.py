# coding=utf-8
from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('div#ah-cat ul.nav > ul.ah-ulsm > li')
        subcats = soup.select('div#ah-cat ul.nav > ul.ah-ulsm > ul.ah-ulsm')

        for idx, item in enumerate(cats):
            menu = item.select_one('a')
            category.append({
                'title': py2_encode(menu.text),
                'link': menu.get("href"),
                'subcategory': idx < len(subcats) and self.getsubmenu(subcats[idx]) or []
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('li > a'):
            category.append({
                'title': py2_encode(item.text),
                'link': item.get('href')
            })

        return category
