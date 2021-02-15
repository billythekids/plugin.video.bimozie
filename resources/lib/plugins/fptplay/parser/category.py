# coding=utf-8
import json


class Parser:
    def get(self, response):
        category = []
        response = json.loads(response)

        # i = [1, 2, 3, 4, 8, 9, 10]
        # i = [3]
        ids = [
            "55701c1517dc1321ee85857a", #Phim bộ
            "52847232169a585a2449c48c", #TV show
            "5587c83b17dc1353a3624a22", #Anime
            "5841452d17dc130a9ab827d4", #Phim lẻ
            # "59e445675583204c11c185c7", #Phim chiếu rạp
            # "59d44bf9558320263bc1a42f", #Gói đặc sắc
            "57b16bdc17dc1302d24da6c5", #Ngoại hạng Anh
            "5b6d415155832008ff700be6", #Serie A
            "54fd271917dc136162a0cf2d", #Thiếu nhi
            "52842df7169a580a79169efd", #Thể thao
            "591408a2558320658eb88e48", #Hài

        ]

        for menu in response['result']:
            if menu['_id'] in ids:
                category.append({
                    'title': menu['name'].encode("utf-8"),
                    # 'link': link,
                    'link': menu['_id'],
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
