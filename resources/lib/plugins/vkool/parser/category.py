from bs4 import BeautifulSoup


class Parser:
    def get(self, response):

        category = []

        soup = BeautifulSoup(response, "html.parser")
        items = soup.select('ul#mega-menu-1 > li')[1:]
        for item in items:
            category.append({
                'title': item.select_one('a').text.encode("utf-8"),
                'link': item.select_one('a').get('href'),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul > li'):
            category.append({
                'title': item.select_one('a').text.encode("utf-8"),
                'link': item.select_one('a').get('href')
            })
        return category
