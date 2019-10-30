# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('div.navbar-start > div.navbar-item.has-dropdown')

        for item in cats:
            menu = item.select_one('> a.navbar-link')
            category.append({
                'title': menu.text.strip().encode("utf-8"),
                'link': None,
                'subcategory': self.getsubmenu(item)
            })
            break
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('a.navbar-item'):
            category.append({
                'title': item.text.encode("utf-8"),
                'link': item.get('href')
            })

        return category
