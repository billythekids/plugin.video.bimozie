import urllib
from utils.mozie_request import Request
from xemphim.parser.category import Parser as Category
from xemphim.parser.channel import Parser as Channel
from xemphim.parser.movie import Parser as Movie
from datetime import datetime


class Xemphim:
    domain = "https://xemphim.plus"

    def getCategory(self):
        response = Request().get(self.domain)
        cat = Category().get(response)

        payload = """
        query Titles($first: Int!, $after: String, $page: String, $genre: String, $country: String, $year: String, $duration: String, $watchable: Boolean, $sort: String) {
          titles(first: $first, after: $after, page: $page, genre: $genre, country: $country, year: $year, duration: $duration, watchable: $watchable, sort: $sort, types: ["movie", "show"]) {
            nodes {
              ...TitleBasics
              __typename
            }
            hasNextPage
            endCursor
            total
            __typename
          }
        }
        
        fragment TitleBasics on Title {
          id
          nameEn
          nameVi
          type
          postedAt
          tmdbPoster
          publishDate
          intro
          imdbRating
          countries
          genres {
            nameVi
            slug
            __typename
          }
          __typename
        }
        """

        response = Request().post("https://b.xemphim.plus/g", json={
            "operationName": "Titles",
            "variables": {"watchable": True, "sort": "postedAt", "first": 15},
            "query": payload
        })

        movies = Channel().get(response, 1)
        movies['page'] = 1
        return cat, movies

    def getChannel(self, channel, page=1):
        payload = """
                query Titles($first: Int!, $after: String, $page: String, $genre: String, $country: String, $year: String, $duration: String, $watchable: Boolean, $sort: String) {
                  titles(first: $first, after: $after, page: $page, genre: $genre, country: $country, year: $year, duration: $duration, watchable: $watchable, sort: $sort, types: ["movie", "show"]) {
                    nodes {
                      ...TitleBasics
                      __typename
                    }
                    hasNextPage
                    endCursor
                    total
                    __typename
                  }
                }
                
                fragment TitleBasics on Title {
                  id
                  nameEn
                  nameVi
                  type
                  postedAt
                  tmdbPoster
                  publishDate
                  intro
                  imdbRating
                  countries
                  genres {
                    nameVi
                    slug
                    __typename
                  }
                  __typename
                }
        """

        channel = channel.replace('/country/', '')
        response = Request().post("https://b.xemphim.plus/g", json={
            "operationName": "Titles",
            "variables": {"country": channel, "watchable": True, "sort": "postedAt", "first": 15,  "page": "{}".format(page)},
            "query": payload
        })

        return Channel().get(response, page)

    def getMovie(self, id):
        payload = """
            query TitleWatch($id: String!) {
              title(id: $id) {
                id
                nameEn
                nameVi
                intro
                publishDate
                tmdbPoster
                tmdbBackdrop
                fileServer
                srcUrl
                spriteUrl
                useVipLink
                reachedWatchLimit
                needImproveSubtitle
                needImproveVideo
                downloadable
                type
                number
                movieInfo {
                  width
                  height
                  __typename
                }
                hasDualSubtitles
                dualSubtitleNeedResync
                parent {
                  id
                  number
                  intro
                  publishDate
                  tmdbPoster
                  parent {
                    id
                    nameEn
                    nameVi
                    tmdbBackdrop
                    __typename
                  }
                  __typename
                }
                children {
                  id
                  number
                  __typename
                }
                __typename
              }
            }
            """

        response = Request().post("https://b.xemphim.plus/g", json={
            "operationName": "TitleWatch",
            "variables": {"id": id},
            "query": payload
        })

        return Movie().get(response)

    def search(self, text):
        today = datetime.now()
        d = today.strftime("%Y-%m-%d-%H")

        url = "https://b.xemphim.plus/suggestions/titles-%s.js" % d
        response = Request().get(url)
        result = Channel().search_result(response, text)
        return result
