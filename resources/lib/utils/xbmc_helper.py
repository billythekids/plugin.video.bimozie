# -*- coding: utf-8 -*-
import xbmc
import xbmcaddon

addon = xbmcaddon.Addon()


def s2u(s): return s.decode('utf-8') if isinstance(s, str) else s


def getSetting(key):
    return addon.getSetting(key)


def message(message='', title='', timeShown=5000):
    if message:
        title = ': [COLOR blue]%s[/COLOR]' % title if title else ''
        s0 = '[COLOR green][B]Bimozie[/B][/COLOR]' + title
        message = s2u(message)
        s1 = u'[COLOR %s]%s[/COLOR]' % ('red' if '!' in message else 'gold', message)
        message = u'XBMC.Notification(%s,%s,%s)' % (s0, s1, timeShown)
        xbmc.executebuiltin(message.encode("utf-8"))
    else:
        xbmc.executebuiltin("Dialog.Close(all, true)")

