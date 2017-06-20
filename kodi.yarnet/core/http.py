# -*- coding: utf-8 -*-

import os, re, sys, json, urllib, hashlib, traceback,base64,math
import xbmcup.app, xbmcup.db, xbmcup.system, xbmcup.net, xbmcup.parser, xbmcup.gui
import xbmc, cover, xbmcplugin, xbmcgui
from common import Render
from defines import *

try:
    cache_minutes = 60*int(xbmcup.app.setting['cache_time'])
except:
    cache_minutes = 0

class HttpData:
    # Загружает страницу
    def load(self, url):
        try:
            response = xbmcup.net.http.get(url)
        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            if(response.status_code == 200):
                return response.text
            return None
    # POST запрос 
    def post(self, url, data):
        try:
            data
        except:
            data = {}
        try:
            response = xbmcup.net.http.post(url, data)
        except xbmcup.net.http.exceptions.RequestException:
            print traceback.format_exc()
            return None
        else:
            if(response.status_code == 200):
                return response.text
            return None


    def strip_scripts(self, html):
        #удаляет все теги <script></script> и их содержимое
        #сделал для того, что бы html parser не ломал голову на тегах в js
        return re.compile(r'<script[^>]*>(.*?)</script>', re.S).sub('', html)

