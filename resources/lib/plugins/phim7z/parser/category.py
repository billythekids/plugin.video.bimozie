from bs4 import BeautifulSoup


class Parser:
    def get(self, response):
        category = []
        soup = BeautifulSoup(response, "html.parser")

        for item in soup.select('ul.top-menu > li')[1:-2]:
            category.append({
                'title': item.select_one('a').text.encode("utf8"),
                'link': item.select_one('a').get('href'),
                'subcategory': self.getsubmenu(item)
            })

        return category

    def getsubmenu(self, xpath):
        category = []
        for item in xpath.select('ul.sub-menu > li > a'):
            category.append({
                'title': item.text.encode("utf8"),
                'link': item.get('href')
            })
        return category
