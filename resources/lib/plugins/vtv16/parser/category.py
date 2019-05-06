# coding=utf-8
from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        cats = soup.select('div#menu > ul.container > li')

        for item in cats[1:]:
            menu = item.select_one('> a')
            cat = {
                'title': menu.text.strip().encode("utf-8"),
                'link': menu.get("href"),
                'subcategory': []
            }

            if menu.get("href") is None:
                cat['subcategory'] = self.getsubmenu(item)
            category.append(cat)
        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('> ul.sub > li > a'):
            category.append({
                'title': item.text.encode("utf-8"),
                'link': item.get('href')
            })

        return category
