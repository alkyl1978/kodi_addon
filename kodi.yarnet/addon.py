# -*- coding: utf-8 -*-

import xbmcup.app
from core.index import Index
from core.list import RayonList

plugin = xbmcup.app.Plugin()
plugin.route(None, Index)
plugin.route('ray-list', RayonList)
plugin.run()
