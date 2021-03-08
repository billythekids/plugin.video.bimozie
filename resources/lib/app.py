# -*- coding: utf-8 -*-
import routing
from kodi_six import xbmc

plugin = routing.Plugin()

from importlib import import_module
from .utils import xbmc_helper as helper
from .utils.xbmc_search import Search
from .utils.xbmc_sites import SiteHandler
from .utils.xbmc_movie import MovieHandler
from .utils.xbmc_fshare import FshareHandler
from .utils.xbmc_player import PlayerHandler


def globalContextMenu():
    commands = list()
    commands.append(('Settings', 'Addon.OpenSettings(%s)' % helper.ADDON_ID,))
    return commands


@plugin.route('/')
def index():
    SiteHandler.index()


@plugin.route('/group/<group_index>')
def show_site_group(group_index):
    SiteHandler.show_site_group(group_index)


@plugin.route('/category')
def show_site_category():
    SiteHandler.show_site_category()


@plugin.route('/subcategory')
def show_site_subcategory():
    SiteHandler.show_site_subcategory()


@plugin.route('/movies')
def show_movies(movies=None, link=None, page=0, cat_name="", module=None, class_name=None):
    MovieHandler.show_movies(movies, link, page, cat_name, module, class_name)


@plugin.route('/movie')
def show_movie():
    MovieHandler.show_movie()


@plugin.route('/movieItemFolder')
def show_fshare_folder():
    FshareHandler.show_fshare_folder()


@plugin.route('/server_group')
def show_movie_server_group():
    MovieHandler.show_movie_server_group()


@plugin.route('/play')
def play(query=None):
    PlayerHandler.play(query)


@plugin.route('/searchAll')
def global_search():
    Search.global_search()


@plugin.route('/searchingAll')
def searching_all():
    Search.searching_all()


@plugin.route('/search')
def search():
    Search.search()


@plugin.route('/searching')
def searching():
    Search.searching()


@plugin.route('/clearSearch')
def clear_search():
    Search.clear_search()


@plugin.route('/lastWatched')
def show_last_watched():
    Search.show_last_watched()


@plugin.route('/clearWatched')
def clear_last_watched():
    Search.clear_last_watched()


@plugin.route('/fshareCode')
def play_with_fshare_code():
    FshareHandler.play_with_fshare_code()


@plugin.route('/playFshareCode')
def playing_with_fshare_code():
    FshareHandler.playing_with_fshare_code()


@plugin.route('/clearFshareCode')
def clear_with_fshare_code():
    FshareHandler.clear_with_fshare_code()


def load_plugin(args):
    class_name = args.get('className', None)
    module = args.get('module', None)
    helper.log("*********************** Run module: {} - plugin: {}".format(module, class_name))
    return getattr(import_module(module), class_name), module, class_name


def main():
    try:
        plugin.run()
    except Exception as ex:
        helper.log(ex.__class__, xbmc.LOGERROR)
        print(ex)
        raise ex
