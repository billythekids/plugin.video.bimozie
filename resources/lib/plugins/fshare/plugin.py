import utils.xbmc_helper as helper
import xbmcaddon
from fshare.parser.channel import Parser as Channel
from utils.hosts.fshare import FShareVN


class FShare:
    api: FShareVN

    def __init__(self):
        if not helper.getSetting('fshare.username'):
            helper.message('Required username/password to get fshare.vn link, open addon settings', 'Login Required')
            xbmcaddon.Addon().openSettings()

        self.api = FShareVN(
            username=helper.getSetting('fshare.username'),
            password=helper.getSetting('fshare.password')
        )

    def getCategory(self):
        response = self.api.get_my_favorite()
        channel = Channel().get(response)
        return [], channel
