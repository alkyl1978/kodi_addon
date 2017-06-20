#!/usr/bin/python
# -*- coding: utf-8 -*-

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


if (__name__ == "__main__" ):
	ses = requests.session()
        http=get_http(url_root,ses)
	#print http
        http = strip_scripts(http)
	soup = BeautifulSoup(http, 'html.parser')
	#print soup
	#print dir(soup)
	raions = soup.findAll('div', class_='rayon')
	for raion in raions:
		print raion.find(class_='name').string
		print '================================================='
		for cam in raion.findAll('a'):
			print cam.string
			#print """rtmpdump --rtmp "rtmp://data-server" --playpath "data-stream""""
			
		#links = soup.findAll('a')
	#for link in links:
		#print link.attrs['href']
		#print dir(link.attrs)
	#	if link.get('data-id'):
	#		#print link.attrs
	#		url=url_saf+link.get('data-stream')+'/'+link.get('data-hash')+'/hls/'
	#		print url
	#		http=get_http(url,ses)
	#		http = strip_scripts(http)
	#		cam = BeautifulSoup(http, 'html.parser')
	#		cas = cam.find('div', class_="iframe_cam_json")
	#		print '+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++'
	#		print cas
