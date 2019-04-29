# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('ul.nav__list > li.nav__list-item')
        for idx, item in enumerate(cats):
            menu = item.select_one('> a')
            if menu:
                category.append({
                    'title': menu.find(text=True, recursive=False).strip().encode("utf-8"),
                    'link': menu.get("href"),
                    'subcategory': self.getsubmenu(item)
                })
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('> ul.nav__sub-list > li > a'):
            category.append({
                'title': item.find(text=True, recursive=False).strip().encode("utf-8"),
                'link': item.get('href')
            })

        return category
