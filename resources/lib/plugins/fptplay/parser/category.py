# coding=utf-8
import json


class Parser:
    def get(self, response):
        category = []
        response = json.loads(response)

        i = [3, 5, 54, 6, 7, 13, 14, 15]
        # i = [3]

        for menu in response['result']:
            if menu['priority'] in i:
                # link = '/danh-muc/%s/%s' % (menu['slug'], menu['_id'])
                category.append({
                    'title': menu['name'].encode("utf-8"),
                    # 'link': link,
                    'link':  menu['_id'],
                    'subcategory': self.getsubmenu(menu['active_children'])
                })

        return category

    def getsubmenu(self, subs):
        category = []
        for menu in subs:
            if 'banner' in menu['name'].encode("utf-8"): continue
            category.append({
                'title': menu['name'].encode("utf-8"),
                'link': menu['_id']
            })

        return category


