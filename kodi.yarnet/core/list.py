# -*- coding: utf-8 -*-

import os, re, sys, json, urllib, hashlib, traceback
import xbmcup.app, xbmcup.db, xbmcup.system, xbmcup.net, xbmcup.parser, xbmcup.gui
import xbmc, cover, xbmcplugin, xbmcgui
from http import HttpData
from defines import *

try:
    from sqlite3 import dbapi2 as sqlite
except:
    from pysqlite2 import dbapi2 as sqlite

CACHE = xbmcup.db.Cache(xbmcup.system.fs('sandbox://'+CACHE_DATABASE))
SQL = xbmcup.db.SQL(xbmcup.system.fs('sandbox://'+CACHE_DATABASE))

#класс выводящий список районов в котоых есть камеры.
class RayonList():
    def handle(self):
        pass
