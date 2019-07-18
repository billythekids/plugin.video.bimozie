# coding=utf-8
import json


class Parser:
    def get(self, response):
        category = []
        response = json.loads(response)

        i = [3, 5, 54, 6, 7, 13, 14, 15]

        for menu in response['result']:
            if menu['priority'] in i:
                link = '/danh-muc/%s/%s' % (menu['slug'], menu['_id'])
                category.append({
                    'title': menu['name'].encode("utf-8"),
                    # 'link': link,
                    'link':  menu['_id'],
                    # 'subcategory': self.getsubmenu(item)
                })

        return category
