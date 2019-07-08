# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('ul#mega-menu-1 > li')

        for item in cats:
            menu = item.select_one('> a')
            if menu.get("href") == '/': continue # skip 1st
            category.append({
                'title': menu.text.strip().encode("utf-8"),
                'link': menu.get("href"),
                'subcategory': self.getsubmenu(item)
            })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('> ul > li > a'):
            category.append({
                'title': item.text.encode("utf-8"),
                'link': item.get('href')
            })

        return category
