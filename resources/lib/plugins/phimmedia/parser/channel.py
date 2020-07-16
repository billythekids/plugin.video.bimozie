from bs4 import BeautifulSoup
import re
import urllib


class Parser:
    def get(self, response, domain="https://www.phim.media", replace_domain="https://www.phimmedia.tv"):

        channel = {
            'page': 1,
            'page_patten': None,
            'movies': []
        }

        soup = BeautifulSoup(response, "html.parser")
        # get total page
        pages = soup.select('div.Paging ul > li > a')
        print("*********************** Get pages ")
        for page in pages:
            if re.compile("(\d+)").match(page.text.strip()):
                channel['page'] = int(page.text)
                link_pattern = re.search("(.*)&page=\d+$", page.get('href'))
                if link_pattern is not None:
                    channel['page_patten'] = self.create_link(link_pattern.group(1).encode('utf-8'))

        for movie in soup.select('ul.list-film > li > div'):
            title = movie.select_one('a').get('title').strip()
            type = ""
            if movie.select_one('div.status') is not None:
                type = movie.select_one('div.status').text.strip()
            if movie.select_one('div.name2') is not None:
                realtitle = movie.select_one('div.name2').text.strip()
            if realtitle is not None:
                label = "[%s] %s - %s" % (type, title, realtitle)
            else:
                label = "[%s] %s" % (type, title)

            thumbnail = movie.select_one('img').get('src').replace(replace_domain, domain)

            channel['movies'].append({
                'id': movie.select_one('a').get('href').replace(replace_domain, domain),
                'label': label.encode("utf-8"),
                'title': title.encode("utf-8"),
                'realtitle': realtitle.encode("utf-8"),
                'thumb': thumbnail,
                'type': type.encode("utf-8"),
            })

        return channel

    def create_link(self, link):
        link = urllib.quote(link)
        link = link.replace("%3F", "?")
        link = link.replace("%3D", "=")
        link = link.replace("%26", "&")
        link = link.replace("%25", "%")
        return link
