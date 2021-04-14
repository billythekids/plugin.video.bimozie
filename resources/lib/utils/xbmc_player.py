import json
import re

import xbmc
import xbmcgui
import xbmcplugin

from . import xbmc_helper as helper
from .media_helper import MediaHelper
from .. import app

plugin = app.plugin


class PlayerHandler:
    def play(query=None):
        if not query:
            query = json.loads(plugin.args['query'][0])
        play_item = xbmcgui.ListItem()

        if int(query.get('direct')) == 0:
            instance, module, class_name = app.load_plugin(query)
            movie_item = query.get('movie_item')
            thumb = helper.text_encode(movie_item.get('thumb'))
            title = helper.text_encode(movie_item.get('title'))
            realtitle = helper.text_encode(movie_item.get('realtitle'))

            movie = instance().getLink(query.get('item'))
            if not movie or 'links' not in movie or len(movie['links']) == 0:
                return
            else:
                blacklist = ['hydrax', 'maya.bbigbunny.ml', 'blob', 'short.icu']

                def filter_blacklist(m):
                    for i in blacklist:
                        if i in m['link']: return False
                    return True

                movie['links'] = list(filter(filter_blacklist, movie['links']))
                if len(movie['links']) > 1:
                    # sort all links
                    try:
                        movie['links'] = sorted(
                            movie['links'], key=lambda elem: re.search(r'(\d+)', elem['title'])
                                                             and int(re.search(r'(\d+)', elem['title']).group(1))
                                                             or 0,
                            reverse=True
                        )
                    except Exception as e:
                        helper.log(e)

                    listitems = []
                    appened_list = []
                    for i in movie['links']:
                        if not next((d for d in appened_list if i.get('link') == d.get('link')), False):
                            listitems.append("%s (%s)" % (i["title"], i["link"]))
                            appened_list.append(i)

                    index = xbmcgui.Dialog().select("Select stream", listitems)
                    if index == -1:
                        return None
                    else:
                        movie = appened_list[index]
                else:
                    movie = movie['links'][0]

                play_item.setArt({'thumb': thumb})
                play_item.setLabel(title)
                play_item.setLabel2(realtitle)
                play_item.setInfo('Video', {
                    'title': title,
                    'originaltitle': realtitle,
                    'plot': movie_item.get('intro')
                })
        else:
            movie = query.get('item')

        # Parse link
        mediatype = MediaHelper.resolve_link(movie)

        if not movie['link']: return
        if movie.get('subtitle'):
            if isinstance(movie['subtitle'], list):
                play_item.setSubtitles(movie['subtitle'])
            else:
                play_item.setSubtitles([movie['subtitle']])
        if mediatype == 'inputstream':
            play_item.setProperty('inputstreamaddon', 'inputstream.adaptive')
            play_item.setProperty('inputstream.adaptive.manifest_type', 'hls')
            play_item.setContentLookup(False)
            link = movie['link'].split('|')
            if link and len(link) > 1:
                play_item.setProperty('inputstream.adaptive.stream_headers', link[1])

        play_item.setProperty('IsPlayable', 'true')
        play_item.setProperty('isFolder', 'false')
        play_item.setPath(str(movie['link']))
        xbmcplugin.setResolvedUrl(plugin.handle, True, listitem=play_item)
        # player = Player()
        # player.play(str(movie['link']), listitem=play_item)
        # while not player.isPlaying():
        #     xbmc.sleep(100)
        xbmcplugin.endOfDirectory(plugin.handle)


class Player(xbmc.Player):
    def __init__(self):
        self.playing = False
        self.last_file = None
        xbmc.Player.__init__(self)

    def setLastFile(self, file):
        self.last_file = file

    def getLastFile(self):
        return self.last_file

    def setPlaying(self, playing):
        self.playing = playing

    def isPlaying(self):
        return self.playing

    def onAVStarted(self):
        if self.isPlayingVideo():
            self.playing = True

    def onPlayBackStopped(self):
        self.playing = False
        self.last_file = None

    def onPlayBackEnded(self):
        self.playing = False
        self.last_file = None
