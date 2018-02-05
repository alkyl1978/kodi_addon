# -*- coding: utf-8 -*-

import xbmcup.app
import xbmcup.parser
from http import HttpData
from defines import *

class Index(xbmcup.app.Handler ,HttpData):
    def handle(self):
	html=self.load(SITE_URL)
	soup = xbmcup.parser.html(self.strip_scripts(html))
	raions = soup.findAll('div', class_='rayon')	
	for raion in raions:
		self.item(raion.find(class_='name').string, self.link('ray-list'), folder=True )
