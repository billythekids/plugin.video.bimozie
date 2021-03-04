from bs4 import BeautifulSoup
from kodi_six.utils import py2_encode


class Parser:
    def get(self, response):

        category = []

        soup = BeautifulSoup(response, "html.parser")
        items = soup.select('ul#mega-menu-1 > li')[1:]
        for item in items:
            category.append({
                'title': py2_encode(item.select_one('a').text),
                'link': item.select_one('a').get('href'),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li'):
            category.append({
                'title': py2_encode(item.select_one('a').text),
                'link': item.select_one('a').get('href')
            })
        return category
