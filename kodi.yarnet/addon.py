# -*- coding: utf-8 -*-

import sys
import os
from xbmcswift2 import Plugin
import requests , re
from bs4 import BeautifulSoup

url_root=u'http://yar-net.ru/video/autovokzal'
url_saf = u'http://saferegion.net/cams/iframe/'
header = {
                'Content-Type': 'text/html; charset=utf-8' ,
                'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0' ,
                'Accept-Encoding':      'gzip, deflate' ,
                'Accept-Language':      'en-US,en;q=0.5',
                'Connection':   'keep-alive'
         }

def get_http(url , ses):
        r = ses.get(url , headers = header)
        return r.content

def strip_scripts(html):
        #удаляет все теги <script></script> и их содержимое
        #сделал для того, что бы html parser не ломал голову на тегах в js
        return re.compile(r'<script[^>]*>(.*?)</script>', re.S).sub('', html)


# Создаем объект plugin
plugin = Plugin()
# Получаем путь к плагину
addon_path = plugin.addon.getAddonInfo('path').decode('utf-8')
# Комбинируем путь к значкам
thumbpath = os.path.join(addon_path, 'res', 'thumbnails')
# Комбинируем путь к фанарту
fanart = os.path.join(addon_path, 'fanart.jpg')
# Импортируем собственный модуль
sys.path.append(os.path.join(addon_path, 'core'))

@plugin.cached(30)
def raion_parser(url):
	raion_list =[]
	ses = requests.session()
        http=get_http(url_root,ses)
        http = strip_scripts(http)
        soup = BeautifulSoup(http, 'html.parser')
        raions = soup.findAll('div', class_='rayon')
        for raion in raions:
                ra={'raion_name': raion.find(class_='name').string , 'soup': raion}
		raion_list.append(ra)
	return ra

@plugin.route('/')
def raion_index():
	raion_list = []
	ras=raion_parser(url_root)
	for i in range(len(ras)):
		index = {'label': ras[i]['raion_name'] , 'path': plugin.url_for('cam_index', cam_soup=ras[i]['soup']) }
		raion_list.append(index)
	return plugin.finish(raion_list, sort_methods=['label'], view_mode=500)

@plugin.route('/raion_list/<cam_soup>')
def cam_index(cam_soup):
	pass


if __name__ == '__main__':
    # Запускаем плагин.
    plugin.run()
