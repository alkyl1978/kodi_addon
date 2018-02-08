#!/usr/bin/python
# -*- coding: utf-8 -*-

# *  Copyright (C) 2016 TDW

import xbmc, xbmcgui, xbmcplugin, xbmcaddon, os, urllib, urllib2, time, codecs, httplib

PLUGIN_NAME   = 'Torrentino'
siteUrl = __settings__.getSetting("UrlSite")
httpSiteUrl = 'http://' + siteUrl
handle = int(sys.argv[1])
addon = xbmcaddon.Addon(id='plugin.video.torrentino.me')
__settings__ = xbmcaddon.Addon(id='plugin.video.torrentino.me')
xbmcplugin.setContent(int(sys.argv[1]), 'movies')

icon  = os.path.join( addon.getAddonInfo('path'), 'icon.png')
dbDir = addon.getAddonInfo('path')
LstDir = addon.getAddonInfo('path')
from  ttnmenu import*

#======================== стандартные функции ==========================
def fs_enc(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode('utf-8').encode(sys_enc)

def fs_dec(path):
	sys_enc = sys.getfilesystemencoding() if sys.getfilesystemencoding() else 'utf-8'
	return path.decode(sys_enc).encode('utf-8')

def fs(s):return s.decode('windows-1251').encode('utf-8')
def ru(x):return unicode(x,'utf8', 'ignore')
def xt(x):return xbmc.translatePath(x)
def rt(x):#('&#39;','’'), ('&#145;','‘')
	L=[('&amp;',"&"),('&#133;','…'),('&#38;','&'),('&#34;','"'), ('&#39;','"'), ('&#145;','"'), ('&#146;','"'), ('&#147;','“'), ('&#148;','”'), ('&#149;','•'), ('&#150;','–'), ('&#151;','—'), ('&#152;','?'), ('&#153;','™'), ('&#154;','s'), ('&#155;','›'), ('&#156;','?'), ('&#157;',''), ('&#158;','z'), ('&#159;','Y'), ('&#160;',''), ('&#161;','?'), ('&#162;','?'), ('&#163;','?'), ('&#164;','¤'), ('&#165;','?'), ('&#166;','¦'), ('&#167;','§'), ('&#168;','?'), ('&#169;','©'), ('&#170;','?'), ('&#171;','«'), ('&#172;','¬'), ('&#173;',''), ('&#174;','®'), ('&#175;','?'), ('&#176;','°'), ('&#177;','±'), ('&#178;','?'), ('&#179;','?'), ('&#180;','?'), ('&#181;','µ'), ('&#182;','¶'), ('&#183;','·'), ('&#184;','?'), ('&#185;','?'), ('&#186;','?'), ('&#187;','»'), ('&#188;','?'), ('&#189;','?'), ('&#190;','?'), ('&#191;','?'), ('&#192;','A'), ('&#193;','A'), ('&#194;','A'), ('&#195;','A'), ('&#196;','A'), ('&#197;','A'), ('&#198;','?'), ('&#199;','C'), ('&#200;','E'), ('&#201;','E'), ('&#202;','E'), ('&#203;','E'), ('&#204;','I'), ('&#205;','I'), ('&#206;','I'), ('&#207;','I'), ('&#208;','?'), ('&#209;','N'), ('&#210;','O'), ('&#211;','O'), ('&#212;','O'), ('&#213;','O'), ('&#214;','O'), ('&#215;','?'), ('&#216;','O'), ('&#217;','U'), ('&#218;','U'), ('&#219;','U'), ('&#220;','U'), ('&#221;','Y'), ('&#222;','?'), ('&#223;','?'), ('&#224;','a'), ('&#225;','a'), ('&#226;','a'), ('&#227;','a'), ('&#228;','a'), ('&#229;','a'), ('&#230;','?'), ('&#231;','c'), ('&#232;','e'), ('&#233;','e'), ('&#234;','e'), ('&#235;','e'), ('&#236;','i'), ('&#237;','i'), ('&#238;','i'), ('&#239;','i'), ('&#240;','?'), ('&#241;','n'), ('&#242;','o'), ('&#243;','o'), ('&#244;','o'), ('&#245;','o'), ('&#246;','o'), ('&#247;','?'), ('&#248;','o'), ('&#249;','u'), ('&#250;','u'), ('&#251;','u'), ('&#252;','u'), ('&#253;','y'), ('&#254;','?'), ('&#255;','y'), ('&laquo;','"'), ('&raquo;','"'), ('&nbsp;',' '), ('&ndash;','-')]
	for i in L:
		x=x.replace(i[0], i[1])
	return x

def FC(s, color="FFFFFF00"):
	s="[COLOR "+color+"]"+s+"[/COLOR]"
	return s

def lower(s):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.lower().encode('utf-8')
	return s

def mfindal(http, ss, es):
	L=[]
	while http.find(es)>0:
		s=http.find(ss)
		e=http.find(es)
		i=http[s:e]
		L.append(i)
		http=http[e+2:]
	return L

def mfind(t,s,e):
	r=t[t.find(s)+len(s):]
	r2=r[:r.find(e)]
	return r2

def mid(s, n):
	try:s=s.decode('utf-8')
	except: pass
	try:s=s.decode('windows-1251')
	except: pass
	s=s.center(n)
	try:s=s.encode('utf-8')
	except: pass
	return s

def mids(s, n):
	l="                                              "
	s=l[:n-len(s)]+s+l[:n-len(s)]
	return s

def debug(s):
	fl = open(ru(os.path.join( addon.getAddonInfo('path'),"test.txt")), "wb")
	fl.write(s)
	fl.close()

def inputbox():
	skbd = xbmc.Keyboard()
	skbd.setHeading('Поиск:')
	skbd.doModal()
	if skbd.isConfirmed():
		SearchStr = skbd.getText()
		return SearchStr
	else:
		return ""

def showMessage(heading, message, times = 3000):
	xbmc.executebuiltin('XBMC.Notification("%s", "%s", %s, "%s")'%(heading, message, times, icon))

def showText(heading, text):
	id = 10147
	xbmc.executebuiltin('ActivateWindow(%d)' % id)
	xbmc.sleep(500)
	win = xbmcgui.Window(id)
	retry = 50
	while (retry > 0):
		try:
			xbmc.sleep(10)
			retry -= 1
			win.getControl(1).setLabel(heading)
			win.getControl(5).setText(text)
			return
		except:
			pass
def deb_print (s): 
	print s
#============================== основная часть ============================
def save_strm(url, ind=0, id='0'):
		info=eval(xt(get_inf_db(id)))
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		originaltitle=info['originaltitle']
		name = originaltitle.replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		
		uri = sys.argv[0] + '?mode=PlayTorrent'
		uri = uri+ '&url='+urllib.quote_plus(url)
		uri = uri+ '&ind='+str(ind)
		uri = uri+ '&id='+str(id)
		
		fl = open(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".strm")), "w")
		fl.write(uri)
		fl.close()
		
		xbmc.executebuiltin('UpdateLibrary("video", "", "false")')

def save_film_nfo(id):
		#get_posters(id)
		info=eval(xt(get_inf_db(id)))
		title=info['title']
		fanart=info['fanart']
		cover=info['cover']
		#try: fanarts=info["fanarts"]
		#except: 
		fanarts=[fanart,cover]
		#posters=get_posters(id)
		#fanarts.extend(posters)
		
		year=info['year']
		plot=info['plot']
		rating=info['rating']
		originaltitle=info['originaltitle']
		#duration=info["duration"]
		#try:genre=info["genre"].replace(', ', '</genre><genre>')
		#except:genre=''
		#studio=info["studio"]
		#director=info["director"]
		cast=info["cast"]
		#try: actors=info["actors"]
		#except: 
		actors={}
		
		name = originaltitle.replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		cn=name.find(" (")
		#if cn>0:
		#	name=name[:cn]
		#	rus=1
		#else: rus=0
		
		#trailer=get_trailer(id)
		
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		
		nfo='<?xml version="1.0" encoding="UTF-8" standalone="yes" ?>'+chr(10)
		nfo+='<movie>'+chr(10)
		
		nfo+="	<title>"+title+"</title>"+chr(10)
		nfo+="	<originaltitle>"+originaltitle+"</originaltitle>"+chr(10)
		#nfo+="	<genre>"+genre+"</genre>"+chr(10)
		#nfo+="	<studio>"+studio+"</studio>"+chr(10)#nfo+="	<director>"+director+"</director>"+chr(10)
		nfo+="	<year>"+str(year)+"</year>"+chr(10)
		nfo+="	<plot>"+plot+"</plot>"+chr(10)
		nfo+='	<rating>'+str(rating)+'</rating>'+chr(10)#nfo+='	<runtime>'+duration+' min.</runtime>'+chr(10)
		
		nfo+="	<fanart>"+chr(10)
		for fan in fanarts:
			nfo+="		<thumb>"+fan+"</thumb>"+chr(10)
		nfo+="		<thumb>"+cover+"</thumb>"+chr(10)
		nfo+="	</fanart>"+chr(10)
		
		nfo+="	<thumb>"+cover+"</thumb>"+chr(10)
		
		for actor in cast:
			nfo+="	<actor>"+chr(10)
			nfo+="		<name>"+actor+"</name>"+chr(10)
			#try:
			#	aid=actors[actor]
			#	actor_img="http://st.kp.yandex.net/images/actor_iphone/iphone360_"+aid+".jpg"
			#	nfo+="		<thumb>"+actor_img+"</thumb>"+chr(10)
			#except: pass
			nfo+="	</actor>"+chr(10)
		
		nfo+="</movie>"+chr(10)
		
		fl = open(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".nfo")), "w")
		fl.write(nfo)
		fl.close()

def play(url, ind=0, id='0'):
	#print url
	engine=__settings__.getSetting("Engine")
	if engine=="0": 
		if play_ace (url, ind) != 'Ok':
			if ind == 0: 
				if play_ace (alter (id, url), 0) != 'Ok': xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.KinoPoisk.ru/?mode=Torrents&id='+id+'", return)')
			else: xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.KinoPoisk.ru/?mode=Torrents&id='+id+'", return)')
	if engine=="1": play_t2h (url, ind, __settings__.getSetting("DownloadDirectory"))
	if engine=="2": play_yatp(url, ind)
	if engine=="3": play_torrenter(url, ind)

def play_ace(torr_link, ind=0):
	try:
		title=get_item_name(torr_link, ind)
		from TSCore import TSengine as tsengine
		TSplayer=tsengine()
		out=TSplayer.load_torrent(torr_link,'TORRENT')
		#print out
		if out=='Ok': TSplayer.play_url_ind(int(ind),title, icon, icon, True)
		TSplayer.end()
		return out
	except: 
		return '0'

def play_t2h(uri, file_id=0, DDir=""):
	try:
		sys.path.append(os.path.join(xbmc.translatePath("special://home/"),"addons","script.module.torrent2http","lib"))
		from torrent2http import State, Engine, MediaType
		progressBar = xbmcgui.DialogProgress()
		from contextlib import closing
		if DDir=="": DDir=os.path.join(xbmc.translatePath("special://home/"),"userdata")
		progressBar.create('Torrent2Http', 'Запуск')
		# XBMC addon handle
		# handle = ...
		# Playable list item
		# listitem = ...
		# We can know file_id of needed video file on this step, if no, we'll try to detect one.
		# file_id = None
		# Flag will set to True when engine is ready to resolve URL to XBMC
		ready = False
		# Set pre-buffer size to 15Mb. This is a size of file that need to be downloaded before we resolve URL to XMBC 
		pre_buffer_bytes = 15*1024*1024
		engine = Engine(uri, download_path=DDir)
		with closing(engine):
			# Start engine and instruct torrent2http to begin download first file, 
			# so it can start searching and connecting to peers  
			engine.start(file_id)
			progressBar.update(0, 'Torrent2Http', 'Загрузка торрента', "")
			while not xbmc.abortRequested and not ready:
				xbmc.sleep(500)
				status = engine.status()
				# Check if there is loading torrent error and raise exception 
				engine.check_torrent_error(status)
				# Trying to detect file_id
				if file_id is None:
					# Get torrent files list, filtered by video file type only
					files = engine.list(media_types=[MediaType.VIDEO])
					# If torrent metadata is not loaded yet then continue
					if files is None:
						continue
					# Torrent has no video files
					if not files:
						break
						progressBar.close()
					# Select first matching file                    
					file_id = files[0].index
					file_status = files[0]
				else:
					# If we've got file_id already, get file status
					file_status = engine.file_status(file_id)
					# If torrent metadata is not loaded yet then continue
					if not file_status:
						continue
				if status.state == State.DOWNLOADING:
					# Wait until minimum pre_buffer_bytes downloaded before we resolve URL to XBMC
					if file_status.download >= pre_buffer_bytes:
						ready = True
						break
					#print file_status
					progressBar.update(100*file_status.download/pre_buffer_bytes, 'Torrent2Http', xt('Предварительная буферизация: '+str(file_status.download/1024/1024)+" MB"), "")
					
				elif status.state in [State.FINISHED, State.SEEDING]:
					#progressBar.update(0, 'T2Http', 'We have already downloaded file', "")
					# We have already downloaded file
					ready = True
					break
				
				if progressBar.iscanceled():
					progressBar.update(0)
					progressBar.close()
					break
				# Here you can update pre-buffer progress dialog, for example.
				# Note that State.CHECKING also need waiting until fully finished, so it better to use resume_file option
				# for engine to avoid CHECKING state if possible.
				# ...
			progressBar.update(0)
			progressBar.close()
			if ready:
				# Resolve URL to XBMC
				item = xbmcgui.ListItem(path=file_status.url)
				xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)
				xbmc.sleep(3000)
				xbmc.sleep(3000)
				# Wait until playing finished or abort requested
				while not xbmc.abortRequested and xbmc.Player().isPlaying():
					xbmc.sleep(500)
	except: pass


def play_yatp(url, ind):
	purl ="plugin://plugin.video.yatp/?action=play&torrent="+ urllib.quote_plus(url)+"&file_index="+str(ind)
	item = xbmcgui.ListItem(path=purl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def play_torrenter(url, ind):
	purl ="plugin://plugin.video.torrenter/?action=playSTRM&url="+ urllib.quote_plus(url)+"&file_index="+str(ind)
	item = xbmcgui.ListItem(path=purl)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)

def GET(url,Referer = 'http://torrentino.me/'):
	deb_print ('KP GET '+url)
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Opera/10.60 (X11; openSUSE 11.3/Linux i686; U; ru) Presto/2.6.30 Version/10.60')
		req.add_header('Accept', '*/*')
		req.add_header('Accept-Language', 'ru,en;q=0.9')
		req.add_header('Referer', Referer)
		response = urllib2.urlopen(req)
		link=response.read()
		response.close()
		return link
	except:
		import requests
		s = requests.session()
		r=s.get(url).text
		rd=r.encode('windows-1251')
		return rd

def GETtorr(target):
	try:
			req = urllib2.Request(url = target)
			req.add_header('User-Agent', 'Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 5.1; Trident/4.0; Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1) ; .NET CLR 1.1.4322; .NET CLR 2.0.50727; .NET CLR 3.0.4506.2152; .NET CLR 3.5.30729; .NET4.0C)')
			resp = urllib2.urlopen(req)
			return resp.read()
	except Exception, e:
			print 'HTTP ERROR ' + str(e)
			return None

def get_params():
	param=[]
	paramstring=sys.argv[2]
	if len(paramstring)>=2:
		params=sys.argv[2]
		cleanedparams=params.replace('?','')
		if (params[len(params)-1]=='/'):
			params=params[0:len(params)-2]
		pairsofparams=cleanedparams.split('&')
		param={}
		for i in range(len(pairsofparams)):
			splitparams={}
			splitparams=pairsofparams[i].split('=')
			if (len(splitparams))==2:
				param[splitparams[0]]=splitparams[1]
	return param


import sqlite3 as db
db_name = os.path.join( dbDir, "info.db" )
c = db.connect(database=db_name)
cu = c.cursor()
def add_to_db(n, item):
		deb_print ('KP add_to_db '+n)
		item=item.replace("'","XXCC").replace('"',"XXDD")
		err=0
		tor_id="n"+n
		litm=str(len(item))
		try:
			cu.execute("CREATE TABLE "+tor_id+" (db_item VARCHAR("+litm+"), i VARCHAR(1));")
			c.commit()
			deb_print ('KP add_to_db CREATE TABLE '+tor_id)
		except: 
			err=1
			print "Ошибка БД"+ n
		if err==0:
			cu.execute('INSERT INTO '+tor_id+' (db_item, i) VALUES ("'+item+'", "1");')
			c.commit()
			deb_print ('KP add_to_db INSERT INTO '+tor_id)
			#c.close()

def get_inf_db(n):
		deb_print ('KP get_inf_db '+n)
		tor_id="n"+n
		cu.execute(str('SELECT db_item FROM '+tor_id+';'))
		c.commit()
		deb_print ('KP get_inf_db SELECT '+tor_id)
		Linfo = cu.fetchall()
		info=Linfo[0][0].replace("XXCC","'").replace("XXDD",'"')
		deb_print ('KP get_inf_db return_info OK')
		return info

def rem_inf_db(n):
		deb_print ('KP rem_inf_db '+n)
		tor_id="n"+n
		try:
			cu.execute("DROP TABLE "+tor_id+";")
			c.commit()
			deb_print ('KP rem_inf_db DROP TABLE '+n)
		except: pass



def AddItem(Title = "", mode = "", id='0', url='', total=60):
			if id !='0':
					try:    info=get_info(url)
					except: info={}
					try:    cover = info["cover"]
					except: cover = icon
					try:    fanart = info["fanart"]
					except: fanart = ''
			else:
				cover = icon
				fanart = ''
				info={'id':id}
			listitem = xbmcgui.ListItem(Title, iconImage=cover, thumbnailImage=cover)
			listitem.setInfo(type = "Video", infoLabels = info)
			try: listitem.setArt({ 'poster': cover, 'fanart' : fanart, 'thumb': cover, 'icon': cover})
			except: pass
			listitem.setProperty('fanart_image', fanart)
			
			purl = sys.argv[0] + '?mode='+mode+'&id='+id
			if url !="": purl = purl +'&url='+urllib.quote_plus(url)
			
			if mode=="Torrents":
				listitem.addContextMenuItems([('[B]Персоны[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Person&id='+id+'&url='+urllib.quote_plus(url)+'")'), ('[B]Трейлер[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=PlayTrailer&id='+id+'&url='+urllib.quote_plus(url)+'")'), ('[B]Список раздач[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Torrents2&id='+id+'&url='+urllib.quote_plus(url)+'")'), ('[B]Обновить описание[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=update_info&id='+id+'&url='+urllib.quote_plus(url)+'")')])
			#('[B]Hайти похожие[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Recomend&id='+id+'&url='+urllib.quote_plus(url)+'")'),('[B]Рецензии[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Review&id='+id+'&url='+urllib.quote_plus(url)+'")'), ('[B]Буду смотреть[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Add2List&id='+id+'&url='+urllib.quote_plus(url)+'")'), 
			#if mode=="PlayTorrent" or mode=="PlayTorrent2":
				#listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
			if mode=="OpenTorrent":
				try:type=info["type"]
				except:type=''
				if type != 'movie': listitem.addContextMenuItems([('[B]Сохранить сериал[/B]', 'Container.Update("plugin://plugin.video.torrent.checker/?mode=save_episodes_api&url='+urllib.quote_plus(url)+'&name='+urllib.quote_plus(info['originaltitle'])+ '&info=' + urllib.quote_plus(repr(info))+'")'),])
				else: listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.torrentino.me/?mode=Save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
				
			try:type=info["type"]
			except:type=''
			if __settings__.getSetting("Autoplay") == 'true' and mode=="Torrents" and type=="":
				listitem.setProperty('IsPlayable', 'true')
				purl = sys.argv[0] + '?mode=Autoplay&id='+id
				xbmcplugin.addDirectoryItem(handle, purl, listitem, False, total)
			else:
				xbmcplugin.addDirectoryItem(handle, purl, listitem, True, total)

def get_info(url):
	if 'http:' not in url: url=httpSiteUrl+"/"+url
	if '/movie/' in url: type  = 'movie'
	else: type  = 'serial'
	id    = mfind(url.replace('//','/')[25:],'/','-')
	try:
		info=eval(xt(get_inf_db(id)))
		deb_print ('TT get_info ОК')
		return info
	except:
		
		hp=GET(url)
		i=mfind(hp,'button rounded middle link trigger-popup add-to-favorites','<div class="scroll-anchors">')
		
		title = mfind(i,'itemprop="name">','<')
		if 'alternateName">' in i: originaltitle = mfind(i,'alternateName">','<')
		else: originaltitle = title
		cover = mfind(i,'<img src="','"')
		if 'ratingValue' in i: 
			rating = mfind(i,'content="','"')
			if '.' not in rating: rating=rating+'.0'
		else: 
			rating='0.0'
		year  = mfind(i,'copyrightYear">','<')
		director  = mfind(i,'directors=','">').strip()
		Lc=mfindal(i,'actors=','">')
		cast=[]
		for c in Lc:
			if c!="": cast.append(c.replace('actors=',''))
		tmp=i.replace('\t','').replace('\n','')
		tmp=tmp[tmp.rfind('</tr>'):]
		#print tmp
		plot  = rt(mfind(tmp,'</div>','</div>').strip()).replace('<p>','')
		if '">' in plot: plot=plot[plot.find('">')+2:]
		art  = get_art(hp)
		fanart = art['fanart']
		trailer = art['trailer']
		
		info={
			'title': title,
			'originaltitle': originaltitle,
			'type': type,
			'id': id,
			'rating': rating,
			'year': year,
			'director': director,
			'cast': cast,
			'cover': cover,
			'fanart': fanart,
			'trailer': trailer,
			'plot': plot,
			'url': url
		}
		
		try: add_to_db(id, repr(info))
		except: print "ERR: " + id
		deb_print ('TT return info')
		return info



def get_art(hp):
	tmp=mfind(hp,'fotoOptions','fotorama')
	Li=mfindal(tmp,'thumb: "','.jpg')
	fanarts=[]
	for i in Li:
		thumb=i.replace('thumb: "','')
		if thumb!='': fanarts.append(thumb+'.jpg')
	if len(fanarts)>0:
		fanart=fanarts[0]
	else:
		fanart=''
	if '.mp4' in tmp:
		trailer=mfind(tmp,'video: "','.mp4')+'.mp4'
	else:
		trailer=''
	return {'fanart': fanart, 'fanarts': fanarts, 'trailer': trailer}

#get_info('http://torrentino.me/movie/843736-inhumans')

#==============  Menu  ====================
def Root():
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	AddItem("Поиск", "Search")
	AddItem("Навигатор", "Navigator")
	AddItem("Фильмы", "movies")
	AddItem("Сериалы", "serials")
	#AddItem("Самые ожидаемые", "Future")
	#AddItem("Списки", "TopLists")
	#AddItem("Персоны", "PersonList")
	#if len(L)>0: AddItem("Буду смотреть", "Wish_list")
	#if __settings__.getSetting("DebMod")=='true': AddItem("Проверить список", "check")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

def Nav(url=''):
	if 'http:' not in url: url=httpSiteUrl+"/"+url
	hp =  GET(url)
	hp=hp[hp.find('<div class="plate showcase">'):]
	#debug(hp)
	L=mfindal(hp,'<div class="tile"','</h2>')
	for i in L:
		title = mfind(i,'itemprop="name">',' · ').replace('</span>','').strip()
		cover = mfind(i,'<img src="','"')
		if 'ratingValue' in i: rating= mfind(i,'content="','"')
		else: rating='0.0'
		year  = mfind(i,'copyrightYear">','</span>')
		qual  = mfind(i,'class="quality">','</span>').strip()
		curl  = mfind(i,'href="','"')
		id    = mfind(curl[1:],'/','-')
		type  = mfind(curl,'/','/')
		if '.' not in rating: rating=rating+'.0'
		
		name = '[ '+rating+' ] '+title#+' ('+year+') '+qual+' '+type
		AddItem(name, 'Torrents', id, curl, 60)
		
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

def Navigator():
	AddItem("Тип: "+__settings__.getSetting("type_t"), "SetType")
	AddItem("Качество: "+__settings__.getSetting("qual_t"), "SetQual")
	AddItem("Год: "+__settings__.getSetting("year_t"), "SetYear")
	AddItem("Страна: "+__settings__.getSetting("country_t"), "SetCountry")
	AddItem("Рейтинг: "+__settings__.getSetting("rating_t"), "SetRating")
	AddItem("Жанр: "+__settings__.getSetting("genre_t"), "SetGenre")
	AddItem("Сортировка: "+__settings__.getSetting("sort_t"), "SetSort")
	AddItem("[B][ ИСКАТЬ ][/B]", "RunNavigator")

def Person(url):
	info=get_info(url)
	
	director=info['director']
	curl='http://www.torrentino.me/movies?actors='+director.replace(' ', '%20')
	AddItem(director+"  (режиссер)", "PersonMovie", '0', curl)
	
	cast=info['cast']
	for i in cast:
		curl='http://www.torrentino.me/movies?actors='+i.replace(' ', '%20')
		AddItem(i, "PersonMovie", '0', curl)

def PersonMovie(url):
	Nav(url)

def Search():
	t=inputbox()
	url='http://www.torrentino.me/search?search='+t.replace(' ','%20')
	Nav(url)

def TopLists():
	for i in get_top_list():
		id=i[0]
		title=i[1]
		AddItem(title, "OpenTopList", id)

def Torrents(url):
	info=get_info(url)
	#url=info['url']
	type=info['type']
	if 'http:' not in url: url=httpSiteUrl+"/"+url
	hp=GET(url)
	hp=hp[hp.find('<div class="scroll-anchors">'):]
	
	if type=='movie': 
		L=torrents_m(hp)
	else: 
		L=torrents_s(hp)
	
	Lz=[]
	for i in L:
		#if type=='movie': title=get_label(i['title'])+" "+i['title']
		#else : title=i['title']
		#AddItem(title, "OpenTorrent", id, i['url'])

		size = i['size']
		if 'MB' in size and '.' in size: 
			size=size[:size.find('.')]
		size = size.replace('GB','').replace('MB','').strip()
		if size not in Lz or __settings__.getSetting("CutSize") == 'false':
						Lz.append(size)
						Z=i['size']
						if 'GB' in Z and Z.find('.') == 2: Z=Z[:3]+Z[4:]
						
						
						if type=='movie': 
							title=xt(mid(Z, 10))+" | "+xt(mids(i['sids'], 6))+" | "+xt(i['title'])
							title=get_label(xt(i['title']))+" "+title
						else : 
							t=i['title']
							sez=t[t.find('сезон')-2:t.find('сезон')]+'c.'
							title=xt(sez)+' '+get_label(xt(i['title']))+" "+xt(mid(Z, 10))+" | "+xt(mids(i['sids'], 6)+" | "+i['label'])
							
						if __settings__.getSetting("SortLst") == 'true' and info['type']=='':
								pr=fnd(D)
								#ratio=str(get_rang(D))+" "
								if pr: title=FC(title, 'FEFFFFFF')
								else:  title=FC(title.replace("[COLOR F", "[COLOR 7"), 'FF777777')
						AddItem(title, "OpenTorrent", id, i['url'])


def torrents_m(hp):
	L=mfindal(hp, '<tr data-group="group', 'href="javascript:void(0);" >Скачать</a>')
	Lout=[]
	for k in L:
		#print k
		L2=k.splitlines()
		seed='0'
		size='0'
		quality=''
		quality2=''
		sound=''
		torrent=''
		for j in L2:
			if 'column size'  in j: size   =j[j.find('">')+2:j.find('</')]
			if 'class="seed"' in j: seed   =j[j.find('">')+2:j.find('</')]
			if 'data-torrent' in j: torrent=j[j.find('="')+2:-1]
			if 'column audio' in j: sound  =j[j.find('">')+2:j.find('</')]
			if 'title="'      in j: quality=j[j.find(' в  ')+3:j.find(' качестве"')].strip()
			if '1920x'        in j: quality2= ' 1080p'
			if '1280x'        in j: quality2= ' 720p'
		if 'class="label-3d"' in k: quality2 += ' 3D'
		if 'не установ' in quality: quality=""
		if size.find("М")>0: size=size[:size.find(".")]+" MB"
		size=size.replace('ГБ', "GB")
		title=size+" "+quality+quality2+" "+sound
		if size!="0" and torrent!='': Lout.append({"sids":seed, "size":size, "title":xt(title),"url":torrent, "quality": quality})
	return Lout

def torrents_s(hp):
	L=mfindal(hp, '<h4>', '</h4>')
	Lout=[]
	Lt=[]
	for s in L:
		url=mfind(s,'href="','"')+'/episode-1'
		#title=mfind(s,'«','»').replace('сезона','сезон')
		ep=GET(url)
		Le=torrents_e(ep)
		for e in Le:
			t=e["url"]
			if t not in Lt:
				Lout.append(e)
				Lt.append(t)
	return Lout

def torrents_e(hp):
	hp=hp[hp.find('<div class="scroll-anchors">'):]
	#debug (hp)
	L=mfindal(hp, '<tr class="item">', '>Скачать<')
	Lout=[]
	Lt=[]
	for k in L:
		if 'data-torrent=""' not in k:
			
			L2=k.splitlines()
			seed='0'
			size='0'
			quality=''
			quality2=''
			torrent=''
			title=''
			title2=''
			for j in L2:
				if 'column size'  in j: size   =j[j.find('">')+2:j.find('</')]
				if 'class="seed"' in j: seed   =j[j.find('">')+2:j.find('</')]
				if 'data-torrent' in j: torrent=j[j.find('="')+2:-1]
				if 'title="'      in j: title=j[j.find('="')+2:j.find('сезон')+10].replace('Скачать ',"")
				if 'data-default' in j: title2=j[j.find('&dn=')+4:j.find('&tr=')]
				if '1920x'        in j: quality= ' 1080p'
				if '1280x'        in j: quality= ' 720p'
				if 'column updated' in j: upd  =j[j.find('">')+2:j.find('</')]
			if 'class="label-3d"' in k: quality += ' 3D'
			if size.find("М")>0: size=size[:size.find(".")]+" MB"
			size=size.replace('ГБ', "GB")
			label=urllib.unquote_plus(title2).replace(title,"")
			title=title+"  /  "+label+" "+quality
			if size!="0" and torrent!='' and torrent not in Lt: 
				Lout.append({"sids":seed, "size":size, "title":xt(title),"url":torrent, "quality": quality, 'upd': upd, 'label': label})
				Lt.append(torrent)
	return Lout

def Torrents_old(id, additm=True):
	offlist=[]
	if __settings__.getSetting("Serv1")=='false': offlist.append('rutor')
	if __settings__.getSetting("Serv2")=='false': offlist.append('fasttor')
	if __settings__.getSetting("Serv3")=='false': offlist.append('freebfg')
	if __settings__.getSetting("Serv4")=='false': offlist.append('torrentino')
	info=get_info(id)
	sys.path.append(os.path.join(addon.getAddonInfo('path'),"src"))
	ld=os.listdir(os.path.join(addon.getAddonInfo('path'),"src"))
	L2=[]
	Lz=[]
	for i in ld:
		off = True
		for sr in offlist:
			if sr in i: off = False
		if i[-3:]=='.py' and off: 
			exec ("import "+i[:-3]+"; skp="+i[:-3]+".Tracker()")
			try:
				exec ("import "+i[:-3]+"; skp="+i[:-3]+".Tracker()")
				L = skp.Search(info)
			except: L=[]
			for D in L:
				url = D['url']
				try:    tor_title=D['title'].encode('utf-8').replace("«",'').replace("»",'').replace('"', '')
				except: tor_title=D['title'].replace("«",'').replace("»",'').replace('"', '')
				deb_print (lower(tor_title))
				ru_title=xt(info['title']).replace("«",'').replace("»",'').replace('"', '')
				deb_print (lower(ru_title))
				en_title=info['originaltitle'].replace("«",'').replace("»",'').replace('"', '')
				year=str(info['year'])
				year2=str(int(info['year'])+1)
				
				if (lower(ru_title) in lower(tor_title) or ru_title in tor_title) and (year in tor_title or year2 in tor_title or info['type']!=''):
					deb_print ('Название соответствует')
					size = D['size']
					if 'MB' in size and '.' in size: size=size[:size.find('.')]
					size = size.replace('GB','').replace('MB','').strip()
					if size not in Lz or __settings__.getSetting("CutSize") == 'false':
						Lz.append(size)
						Z=D['size']
						if 'GB' in Z and Z.find('.') == 2: Z=Z[:3]+Z[4:]
						title=xt(mid(Z, 10))+" | "+xt(mids(D['sids'], 6))+" | "+xt(D['title'])
						title=get_label(xt(D['title']))+" "+title
						if additm:
							if __settings__.getSetting("SortLst") == 'true' and info['type']=='':
								pr=fnd(D)
								#ratio=str(get_rang(D))+" "
								if pr: title=FC(title, 'FEFFFFFF')
								else:  title=FC(title.replace("[COLOR F", "[COLOR 7"), 'FF777777')
							AddItem(title, "OpenTorrent", id, url)
						L2.append(D)
				#print D
	return L2

def get_label(text):
	text=lower(text)#.lower()
	#print text
	if 'трейлер'  in text: return FC('[ Трейл.]',    'FF999999')
	if ' кпк'     in text: return FC('[   КПК  ]',   'FFF8888F')
	if 'telesyn'  in text: return FC('[    TS    ]', 'FFFF2222')
	if 'telecin'  in text: return FC('[    TS    ]', 'FFFF2222')
	if 'camrip'   in text: return FC('[    TS    ]', 'FFFF2222')
	if ' ts'      in text: return FC('[    TS    ]', 'FFFF2222')
	if 'dvdscr'   in text: return FC('[    Scr   ]', 'FFFF2222')
	if ' 3d'      in text: return FC('[    3D    ]', 'FC45FF45')
	if '720'      in text: return FC('[  720p  ]',   'FBFFFF55')
	if '1080'     in text: return FC('[ 1080p ]',    'FAFF9535')
	if 'blu-ray'  in text: return FC('[  BRay  ]',   'FF5555FF')
	if 'bdremux'  in text: return FC('[    BD    ]', 'FF5555FF')
	if ' 4k'      in text: return FC('[    4K    ]', 'FF5555FF')
	if 'bdrip'    in text: return FC('[ BDRip ]',    'FE98FF98')
	if 'drip'     in text: return FC('[ BDRip ]',    'FE98FF98')
	if 'hdrip'    in text: return FC('[ HDRip ]',    'FE98FF98')
	if 'webrip'   in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'WEB'      in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'web-dl'   in text: return FC('[  WEB   ]',   'FEFF88FF')
	if 'hdtv'     in text: return FC('[ HDTV ]',     'FEFFFF88')
	if 'tvrip'    in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'satrip'   in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'dvb '     in text: return FC('[    TV    ]', 'FEFFFF88')
	if 'dvdrip'   in text: return FC('[DVDRip]',     'FE88FFFF')
	if 'dvd5'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'xdvd'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd-5'    in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd-9'    in text: return FC('[  DVD   ]',   'FE88FFFF')
	if 'dvd9'     in text: return FC('[  DVD   ]',   'FE88FFFF')
	return FC('[   ????  ]', 'FFFFFFFF')

def OpenTorrent(url, id):
	#print url
	torrent_data = GETtorr(url)
	if torrent_data != None:
		import bencode
		torrent = bencode.bdecode(torrent_data)
		cover = icon#get_info(id)['cover']
		try:
			L = torrent['info']['files']
			ind=0
			for i in L:
				name=ru(i['path'][-1])
				#size=i['length']
				listitem = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
				listitem.setProperty('IsPlayable', 'true')
				uri = sys.argv[0]+'?mode=PlayTorrent2&id='+id+'&ind='+str(ind)+'&url='+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle, uri, listitem)
				ind+=1
		except:
				ind=0
				name=torrent['info']['name']
				listitem = xbmcgui.ListItem(name, iconImage=cover, thumbnailImage=cover)
				listitem.setProperty('IsPlayable', 'true')
				listitem.addContextMenuItems([('[B]Сохранить фильм(STRM)[/B]', 'Container.Update("plugin://plugin.video.KinoPoisk.ru/?mode=Save_strm&id='+id+'&url='+urllib.quote_plus(url)+'")'),])
				uri =sys.argv[0]+'?mode=PlayTorrent2&id='+id+'&ind='+str(ind)+'&url='+urllib.quote_plus(url)
				xbmcplugin.addDirectoryItem(handle, uri, listitem)

def get_item_name(url, ind):
	torrent_data = GETtorr(url)
	if torrent_data != None:
		import bencode
		torrent = bencode.bdecode(torrent_data)
		try:
			L = torrent['info']['files']
			name=L[ind]['path'][-1]
		except:
			name=torrent['info']['name']
		return name
	else:
		return ' '

def check():
	deb_print ("check")
	SaveDirectory = __settings__.getSetting("SaveDirectory")
	if SaveDirectory=="":SaveDirectory=LstDir
	
	try:L=eval(__settings__.getSetting("W_list"))
	except: L=[]
	for id in L:
		info=get_info(id)
		year=info["year"]
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		if os.path.isfile(os.path.join(fs_enc(SaveDirectory),fs_enc(name+".strm")))==False:
			L=Torrents(id, False)
			url=''
			rang=0
			for i in L:
				if fnd(i):
					rang_i=get_rang(i)
					if rang_i>rang:
						rang=rang_i
						deb_print (str(rang)+": "+i['title']+" "+i['size'])
						deb_print (i['url'])
						url=i['url']
			
			if url != "":
					if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
					save_strm (url, 0, id)
		else:
			if __settings__.getSetting("AREM")=='true': # автоудаление из желаний
					try:Lt=eval(__settings__.getSetting("W_list"))
					except: Lt=[]
					Lt.remove(id)
					__settings__.setSetting("W_list", repr(Lt))


def alter(id, url=''):
		SaveDirectory = __settings__.getSetting("SaveDirectory")
		if SaveDirectory=="":SaveDirectory=LstDir
		info=get_info(id)
		year=info["year"]
		name = info['originaltitle'].replace("/"," ").replace("\\"," ").replace("?","").replace(":","").replace('"',"").replace('*',"").replace('|',"")+" ("+str(info['year'])+")"
		L=Torrents(id, False)
		try:W_list=eval(__settings__.getSetting("W_list"))
		except: W_list=[]
		for i in L:
			newurl=i['url'].replace('new-ru.org','').replace('open-tor.org','')
			oldurl=url.replace('new-ru.org','').replace('open-tor.org','')
			if fnd(i) and newurl!=oldurl:
				if id in W_list:
					if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
					save_strm (i['url'], 0, id)
				return i['url']

def autoplay(id):
		L=Torrents(id, False)
		url=''
		for i in L:
			if fnd(i): 
				url=i['url']
				break
		if url !='': play(url,0,id)
		else: 
			if len(L)== 0: showMessage("Кинопоиск", "Фильм не найден")
			else: showMessage("Кинопоиск", "Нет нужного качества")

def review(id):
	url='https://m.kinopoisk.ru/reviews/'+id
	url='https://www.kinopoisk.ru/rss/comment-'+id+'.rss'
	http=GET(url)
	#debug(http)
	ss='<item>'
	es='</item>'
	L=mfindal(http,ss,es)
	#debug(L[0])
	Lt=[]
	Lu=[]
	for i in L:
		#if "hand_good.gif" in i: rating = FC('+', 'FF33FF33')
		#elif "hand_bad.gif" in i: rating = FC(' - ', 'FFFF3333')
		#else: rating = FC(' - ', '01003333')
		rating =''
		
		ss='<pubDate>'
		es='</pubDate>'
		date=mfindal(i,ss,es)[0][len(ss):]
		
		ss='&lt;i&gt;'
		es='&lt;/i&gt;&lt;'
		try:head=mfindal(i,ss,es)[0][len(ss):]
		except: head=''
		
		ss='<guid>'
		es='</guid>'
		url=mfindal(i,ss,es)[0][len(ss):]
		if head!='':
			Lt.append(rt(fs(head)))
			Lu.append(url)
	sel = xbmcgui.Dialog()
	r = sel.select("Рецензии:", Lt)
	if r >=0:
		http2=GET(Lu[r])
		#debug (http2)
		n=http2.find('itemprop="reviewBody">')
		k=http2.find('</span></p>')
		text=http2[n+22:k].replace('<b>','').replace('</b>','').replace('<i>','').replace('</i>','').replace('<p>','').replace('</p>','').replace('<br>','').replace('<br />','').replace('&nbsp;',' ')
		text=rt(fs(text))
		heading=Lt[r]
		showText(heading, text)



def fnd(D):
	BL=['Трейлер', "Тизер", 'трейлер', "тизер", 'ТРЕЙЛЕР', "ТИЗЕР"]
	if __settings__.getSetting("F_Qual") != "0":BL.extend([' TS','TeleSyn','TeleCin','TELECIN',' CAM',' CamRip','screen','Screen', 'звук из кинотеатра'])
	WL=[]
	if __settings__.getSetting("F_Qual1") == 'true': WL.append("dvdrip")
	if __settings__.getSetting("F_Qual2") == 'true': WL.append("webrip")
	if __settings__.getSetting("F_Qual3") == 'true': WL.append("web-dl")
	if __settings__.getSetting("F_Qual4") == 'true': WL.append("bdrip")
	if __settings__.getSetting("F_Qual5") == 'true': WL.append("hdrip")
	if __settings__.getSetting("F_Qual6") == 'true': WL.append("tvrip")
	if __settings__.getSetting("F_Qual7") == 'true': WL.append("hdtv")
	if __settings__.getSetting("F_Qual8") == 'true': WL.append("blu-ray")
	if __settings__.getSetting("F_Qual9") == 'true': WL.append("720p")
	if __settings__.getSetting("F_Qual10")== 'true': WL.append("1080p")
	if __settings__.getSetting("F_Qual") == '0': WL=[]

	size1 = int(__settings__.getSetting("F_Size1"))
	size2 = int(__settings__.getSetting("F_Size2"))
	if size2 == 0: size2 = 999
	
	b=0
	q=0
	z=0
	Title = D['title']
	try:Title=Title+' '+D['quality']
	except:pass
	
	try:Title=Title.encode('utf-8')
	except: Title=xt(Title)
	
	for i in BL:
		if Title.find(i)>0:b+=1
	
	if __settings__.getSetting("F_Qual") == "0":
		q=1
	else:
		for i in WL:
			if Title.lower().find(i)>0:q+=1
		
	if 'ГБ' in xt(D['size']) or 'GB' in xt(D['size']):
			szs=xt(D['size']).replace('ГБ','').replace('GB','').replace('|','').strip()
			sz=float(szs)
			if sz>size1 and sz<size2 : z=1
	else: z=0
	
	#print Title
	#if b <> 0: print 'Попал в Черный список'
	#if q == 0: print 'Низкое Качество'
	#if z == 0: print 'Не тот Размер'
	
	if b == 0 and q > 0 and z > 0:
		#print 'Файл найден'
		return True
	else: 
		return False

def get_rang(D):
	Title = D['title']
	try:Title=Title+' '+D['quality']
	except:pass
	try:Title=Title.encode('utf-8')
	except: Title=xt(Title)
	Title=Title.lower()
	ratio=0
	WL=[]
	if __settings__.getSetting("F_Qual1") == 'true' and "dvdrip"  in Title:   ratio+=40
	if __settings__.getSetting("F_Qual2") == 'true' and "webrip"  in Title:   ratio+=30
	if __settings__.getSetting("F_Qual3") == 'true' and "web-dl"  in Title:   ratio+=30
	if __settings__.getSetting("F_Qual4") == 'true' and "bdrip"   in Title:   ratio+=80
	if __settings__.getSetting("F_Qual5") == 'true' and "hdrip"   in Title:   ratio+=80
	if __settings__.getSetting("F_Qual6") == 'true' and "tvrip"   in Title:   ratio+=20
	if __settings__.getSetting("F_Qual7") == 'true' and "hdtv"    in Title:   ratio+=70
	if __settings__.getSetting("F_Qual8") == 'true' and "blu-ray" in Title:   ratio+=20
	
	if __settings__.getSetting("F_Qual9") == 'true' and '720p'    in Title:   ratio+=1000
	if __settings__.getSetting("F_Qual10")== 'true' and "1080p"   in Title:   ratio+=2000
	
	size1 = int(__settings__.getSetting("F_Size1"))
	size2 = int(__settings__.getSetting("F_Size2"))
	if size2 == 0: size2 = 10
	size=(size2-size1)/2+size1
	
	if 'ГБ' in xt(D['size']) or 'GB' in xt(D['size']):
			szs=xt(D['size']).replace('ГБ','').replace('GB','').replace('|','').strip()
			sz=float(szs)
			#print size
			#print sz
			#print abs(sz-size)
			#print '----'
			if   abs(sz-size)<1 : ratio+=900
			elif abs(sz-size)<2 : ratio+=800
			elif abs(sz-size)<3 : ratio+=700
			elif abs(sz-size)<4 : ratio+=600
			elif abs(sz-size)<5 : ratio+=500
			elif abs(sz-size)<6 : ratio+=400
			elif abs(sz-size)<7 : ratio+=300
			elif abs(sz-size)<8 : ratio+=200
			elif abs(sz-size)<9 : ratio+=100
	
	sids=D['sids']
	if len(sids)==1: ratio+=11
	if len(sids)==2: ratio+=44
	if len(sids)==3: ratio+=66
	if len(sids)==4: ratio+=88
	if len(sids)==5: ratio+=99
	if sids =='0': ratio-=500
	if sids =='1': ratio-=100
	if sids =='2': ratio-=50
	return ratio

def SetViewMode():
	n = int(__settings__.getSetting("ListView"))
	if n>0:
		xbmc.executebuiltin("Container.SetViewMode(0)")
		for i in range(1,n):
			xbmc.executebuiltin("Container.NextViewMode")



try:    mode = urllib.unquote_plus(get_params()["mode"])
except: mode = None
try:    url = urllib.unquote_plus(get_params()["url"])
except: url = None
try:    info = eval(urllib.unquote_plus(get_params()["info"]))
except: info = {}
try:    id = str(get_params()["id"])
except: id = '0'
try:    ind = int(get_params()["ind"])
except: ind = 0


if mode == None:
	__settings__.setSetting("type", 'movies')
	__settings__.setSetting("type_t", 'Фильм')
	__settings__.setSetting("qual", '')
	__settings__.setSetting("qual_t", 'Любое')
	__settings__.setSetting("year", '')
	__settings__.setSetting("year_t", '')
	__settings__.setSetting("country", '')
	__settings__.setSetting("country_t", '')
	__settings__.setSetting("rating", 'от 5')
	__settings__.setSetting("rating_t", '5')
	__settings__.setSetting("genre", '')
	__settings__.setSetting("genre_t", '')
	__settings__.setSetting("sort", 'rating')
	__settings__.setSetting("sort_t", 'по рейтингу')

	Root()

if mode == "Search":
	Search()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Navigator":
	Navigator()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)
if mode == "RunNavigator":
	type	=	__settings__.getSetting("type")
	qual	=	'quality='+__settings__.getSetting("qual")
	year	=	'&years='+__settings__.getSetting("year")
	rating	=	'&rating-from='+__settings__.getSetting("rating")
	country	=	'&countries='+__settings__.getSetting("country")
	if country=='&countries=':country=''
	genre	=	'&genres='+__settings__.getSetting("genre")
	if genre=='&genres=':genre=''
	sort	=	'&sort='+__settings__.getSetting("sort")
	url='http://www.torrentino.me/'+type+'?'+qual+genre+country+year+rating+sort
	
	Nav(url)

if mode == "movies":
	Nav("movies?sort=popularity")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "serials":
	Nav("serials?sort=popularity")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Person":
	Person(url)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PersonMovie":
	PersonMovie(url)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Recomend":
	SrcNavi("Recomend")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "Torrents" or mode == "Torrents2":
	Torrents(url)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(handle)
	xbmc.sleep(300)
	SetViewMode()
	#xbmc.executebuiltin("Container.SetViewMode(51)")

if mode == "OpenTorrent":
	OpenTorrent(url, id)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(handle)


if mode == "PlayTorrent":
	progressBar = xbmcgui.DialogProgress()
	progressBar.create('Кинопоиск', 'Запуск сохраненного файла')
	cancel=False
	for i in range (0,5):
		progressBar.update(20*i, '', '[B]Нажмите "Отмена" для выбора качества[/B]')
		xbmc.sleep(600)
		if progressBar.iscanceled():
					progressBar.update(0)
					cancel=True
					break
	progressBar.close()
	if cancel: 
		xbmc.executebuiltin('ActivateWindow(10025,"plugin://plugin.video.KinoPoisk.ru/?mode=Torrents&id='+id+'", return)')
		xbmc.executebuiltin("Container.Refresh()")
	else: play(url, ind, id)

if mode == "PlayTorrent2":
	play(url, ind, id)

if mode == "Wish":
	Torrents(id)
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.addSortMethod(handle, xbmcplugin.SORT_METHOD_LABEL)
	xbmcplugin.endOfDirectory(handle)
	xbmc.sleep(300)
	SetViewMode()
	#xbmc.executebuiltin("Container.SetViewMode(51)")

if mode == "update_info":
	rem_inf_db(id)
	xbmc.executebuiltin('Container.Refresh')


if mode == "TopLists":
	TopLists()
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "OpenTopList":
	SrcNavi("OpenTopList")
	xbmcplugin.setPluginCategory(handle, PLUGIN_NAME)
	xbmcplugin.endOfDirectory(handle)

if mode == "PlayTrailer":
	info=get_info(url)
	trailer=info['trailer']
	if trailer!='':
		cover=info['cover']
		title=info['title']
		listitem = xbmcgui.ListItem("trailer", path=trailer,iconImage=cover, thumbnailImage=cover)
		listitem.setInfo(type = "Video", infoLabels = info)
		xbmc.Player().play(trailer, listitem)
		xbmcplugin.endOfDirectory(handle, False, False)

if mode == "Save_strm":
	if __settings__.getSetting("NFO2")=='true': save_film_nfo(id)
	save_strm (url, 0, id)

if mode == "check":
	check()

if mode == "Review":
	review(id)

if mode == "Autoplay":
	autoplay(id)


if mode == "SetType":
	sel = xbmcgui.Dialog()
	l=type_list.keys()
	l.sort()
	r = sel.select("Тип:", l)
	__settings__.setSetting(id="type", value=type_list[l[r]])
	__settings__.setSetting(id="type_t", value=l[r])

if mode == "SetQual":
	sel = xbmcgui.Dialog()
	l=quality_list.keys()
	l.sort()
	r = sel.select("Качество:", l)
	__settings__.setSetting(id="qual", value=quality_list[l[r]])
	__settings__.setSetting(id="qual_t", value=l[r])

if mode == "SetYear":
	sel = xbmcgui.Dialog()
	l=year_list.keys()
	l.sort()
	r = sel.select("Год:", l)
	__settings__.setSetting(id="year", value=year_list[l[r]])
	__settings__.setSetting(id="year_t", value=l[r])

if mode == "SetCountry":
	sel = xbmcgui.Dialog()
	l=country_list.keys()
	l.sort()
	r = sel.select("Страна:", l)
	__settings__.setSetting(id="country", value=country_list[l[r]])
	__settings__.setSetting(id="country_t", value=l[r])

if mode == "SetRating":
	sel = xbmcgui.Dialog()
	l=rating_list.keys()
	l.sort()
	r = sel.select("Рейтинг:", l)
	__settings__.setSetting(id="rating", value=rating_list[l[r]])
	__settings__.setSetting(id="rating_t", value=l[r])

if mode == "SetGenre":
	sel = xbmcgui.Dialog()
	l=genre_list.keys()
	l.sort()
	r = sel.select("Жанр:", l)
	__settings__.setSetting(id="genre", value=genre_list[l[r]])
	__settings__.setSetting(id="genre_t", value=l[r])

if mode == "SetSort":
	sel = xbmcgui.Dialog()
	l=sort_list.keys()
	l.sort()
	r = sel.select("Сортировка:", l)
	__settings__.setSetting(id="sort", value=sort_list[l[r]])
	__settings__.setSetting(id="sort_t", value=l[r])


c.close()
