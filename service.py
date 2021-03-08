# -*- coding: utf-8 -*-

import xbmc
import xbmcaddon
import xbmcgui

from resources.lib.utils.xbmc_player import Player

addon = xbmcaddon.Addon()
monitor = xbmc.Monitor()
dialog = xbmcgui.Dialog()
player = Player()


while not monitor.abortRequested():
    if monitor.waitForAbort(1):
        break
    if player.isPlaying():
        last_file = player.getLastFile()
        try:
            current_file = player.getPlayingFile()
        except Exception:
            player.setPlaying(False)
            continue

        log(last_file)
        log(current_file)
