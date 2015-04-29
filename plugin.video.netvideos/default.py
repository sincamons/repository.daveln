# -*- coding: utf-8 -*-

'''
Copyright (C) 2014                                                     

This program is free software: you can redistribute it and/or modify   
it under the terms of the GNU General Public License as published by   
the Free Software Foundation, either version 3 of the License, or      
(at your option) any later version.                                    

This program is distributed in the hope that it will be useful,        
but WITHOUT ANY WARRANTY; without even the implied warranty of         
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          
GNU General Public License for more details.                           

You should have received a copy of the GNU General Public License      
along with this program. If not, see <http://www.gnu.org/licenses/>  
'''                                                                           

import urllib, urllib2, re, os, sys
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.video.netvideos')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))
homemenu = xbmc.translatePath(os.path.join(home, 'resources', 'playlists', 'netvideos.xml'))
homelink = 'https://raw.githubusercontent.com/daveln/repository.daveln/master/playlists/netvideos.xml'
dict = {'&amp;':'&', '&quot;':'"', '.':' ', '&#39':'\'', '&#038;':'&', '&#039':'\'', '&#8211;':' - ', '&#8220;':'"', '&#8221;':'"', '&#8230':'...'}
dongnai = 'http://www.dnrtv.org.vn'
CaliToday = 'http://truyenhinhcalitoday.com/'
nguoiviettvcom = 'http://nguoiviettv.com'
cailuongus = 'http://phimtailieu.haikich.us'

if not os.path.exists(homemenu):
	try:
		open(homemenu, 'w').close()
	except:
		pass  	
	
status = urllib.urlopen(homelink).getcode()
if status == 200:
	urllib.urlretrieve (homelink, homemenu)

def menulist():
	try:
		mainmenu = open(homemenu, 'r')  
		mlink = mainmenu.read()
		mainmenu.close()
		match = re.compile("<title>([^<]*)<\/title>\s*<link>([^<]+)<\/link>\s*<thumbnail>(.+?)</thumbnail>").findall(mlink)
		return match
	except:
		pass	

def replaceAll(text, dict):
	try:
		for a, b in dict.iteritems():
			text = text.replace(a, b)
		return text
	except:
		pass	

def makeRequest(url):
	try:
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:19.0) Gecko/20100101 Firefox/19.0')
		response = urllib2.urlopen(req, timeout = 60)
		link = response.read()
		response.close()  
		return link
	except urllib2.URLError, e:
		print 'We failed to open "%s".' % url
		if hasattr(e, 'code'):
			print 'We failed with error code - %s.' % e.code	
		if hasattr(e, 'reason'):
			print 'We failed to reach a server.'
			print 'Reason: ', e.reason

def home():
	add_dir('[COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[COLOR yellow]  Home  [COLOR cyan]. .[COLOR red]  ^  [COLOR cyan]. .[/COLOR]', '', None, icon, fanart)
			
def main():
	add_dir('Hải Ngoại', 'HaiNgoai', 1, logos + 'haingoai.png', fanart)
	add_dir('Trong Nước', 'TrongNuoc', 2, logos + 'vietnam.png', fanart)  
      
def trongnuoc():
	home()
	add_dir('Đài Phát Thanh - Truyền Hình Đồng Nai', dongnai, 3, logos + 'dongnai.png', fanart)
  
def haingoai(): 
	home()
	add_dir('nguoiviettv.com', nguoiviettvcom, 4, logos + 'nguoiviet.png', fanart) 
	add_dir('Truyền Hình Cali Today', CaliToday, 3, logos + 'cali.png', fanart)  
  
def mediaStations(url):
	home()
	content = makeRequest(url)
	if 'www.dnrtv.org' in url:
		match = re.compile("tabindex=\"0\"><a href=\"([^\"]+)\">(.+?)<").findall(content)[13:]
		for url, name in match:  	
			add_dir(name, dongnai + url, 5, logos + 'dongnai.png', fanart)
	elif 'truyenhinhcalitoday' in url:
		match = re.compile('href="http://truyenhinhcalitoday.com/category([^>]+)">([^>]+)<').findall(content)[0:12]
		for url, name in match:	
			add_dir(name, CaliToday + 'category' + url, 5, logos + 'cali.png', fanart)			
        
def NguoiViet():
	home()
	for title, url, thumb in menulist():
		if 'nguoiviet.com - ' in title:
			add_dir(title.replace('nguoiviet.com - ', ''), url, 5, logos + thumb, fanart)  
     
def mediaList(url):
	home()
	content = makeRequest(url)
	if 'www.dnrtv.org.vn' in url:
		match = re.compile("img src=\"([^\"]+)\" \/><\/a>\s*<a href=\"([^\"]*)\" class=\"title\">(.+?)<").findall(content)
		for thumb, url, name in match:     
			add_link(name, url, 6, thumb, fanart)
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang đầu<').findall(content)
		for url in match:	
			add_dir('[COLOR yellow]Trang đầu[/COLOR]', url, 5, logos + 'dongnai.png', fanart)    
		match = re.compile('class=\'paging_normal\' href=\'([^\']+)\'>(\d+)<').findall(content)
		for url, name in match:	
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 5, icon, fanart)	
		match = re.compile('class=\'paging_normal\' href=\'([^\']*)\'>Trang cuối<').findall(content)
		for url in match:	
			add_dir('[COLOR red]Trang cuối[/COLOR]', url, 5, logos + 'dongnai.png', fanart)	
	elif 'truyenhinhcalitoday' in url:
		match = re.compile('href="(.+?)">\s*<span class="clip">\s*<img src="(.+?)" alt="(.+?)"').findall(content)
		for url, thumb, name in match:
			name = replaceAll(name, dict)
			add_link(name, url, 6, thumb, fanart)
		match = re.compile("href='([^']*)' class='first'").findall(content)
		for url in match:	
			add_dir('[COLOR yellow]Trang đầu[/COLOR]', url, 5, logos + 'cali.png', fanart)    
		match = re.compile("href='([^']*)' class='page larger'>(\d+)<").findall(content)
		for url, name in match:	
			add_dir('[COLOR lime]Trang ' + name + '[/COLOR]', url, 5, logos + 'cali.png', fanart)	
		match = re.compile("href='([^']*)' class='last'").findall(content)
		for url in match:	
			add_dir('[COLOR red]Trang cuối[/COLOR]', url, 5, logos + 'cali.png', fanart)	
	elif 'nguoiviettv' in url:
		if 'orderby=views' in url:
			match = re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[0:24]
			for name, url, thumb in match:
				name = replaceAll(name, dict)
				add_link(name, url, 6, thumb, fanart)
		else: 
			match = re.compile('title="([^"]*)" href="([^"]+)">\s*<span class="clip">\s*<img src="(.+?)"').findall(content)[15:-6]
			for name, url, thumb in match:
				name = replaceAll(name, dict)
				add_link(name, url, 6, thumb, fanart)    
		match = re.compile("href='([^']*)' class='.+?'>(\d+)<").findall(content)
		for url, name in match:	
			add_dir('[COLOR yellow]Trang ' + name + '[/COLOR]', url.replace('#038;', ''), 5, logos + 'nguoiviet.png', fanart)
	xbmc.executebuiltin('Container.SetViewMode(500)')
          
def resolveUrl(url):
	content = makeRequest(url)
	if 'www.dnrtv.org.vn' in url:  
		media_url = re.compile("url: '(.+?)mp4'").findall(content)[0] + 'mp4' 
	elif 'truyenhinhcalitoday' in url or 'nguoiviettv' in url:
		videoID = re.compile("http://www.youtube.com/embed/(.+?)\?").findall(content)[0]  
		media_url = 'plugin://plugin.video.youtube/?path=/root/video&action=play_video&videoid=' + videoID       
	item = xbmcgui.ListItem(name, path = media_url)
	xbmcplugin.setResolvedUrl(int(sys.argv[1]), True, item)	  
	return
  
def get_params():
	param = []
	paramstring = sys.argv[2]
	if len(paramstring)>= 2:
		params = sys.argv[2]
		cleanedparams = params.replace('?', '')
		if (params[len(params)-1] == '/'):
			params = params[0:len(params)-2]
		pairsofparams = cleanedparams.split('&')
		param = {}
		for i in range(len(pairsofparams)):
			splitparams = {}
			splitparams = pairsofparams[i].split('=')
			if (len(splitparams)) == 2:
				param[splitparams[0]] = splitparams[1]
	return param

def add_dir(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)
	ok = True
	liz = xbmcgui.ListItem(name, iconImage = "DefaultFolder.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz, isFolder = True)
	return ok

def add_link(name, url, mode, iconimage, fanart):
	u = sys.argv[0] + "?url=" + urllib.quote_plus(url) + "&mode=" + str(mode) + "&name=" + urllib.quote_plus(name) + "&iconimage=" + urllib.quote_plus(iconimage)	
	liz = xbmcgui.ListItem(name, iconImage = "DefaultVideo.png", thumbnailImage = iconimage)
	liz.setInfo( type = "Video", infoLabels = { "Title": name } )
	liz.setProperty('fanart_image', fanart)
	liz.setProperty('IsPlayable', 'true')  
	ok = xbmcplugin.addDirectoryItem(handle = int(sys.argv[1]), url = u, listitem = liz)  
 	  		  
params = get_params()
url = None
name = None
mode = None
iconimage = None

try:
	url = urllib.unquote_plus(params["url"])
except:
	pass
try:
	name = urllib.unquote_plus(params["name"])
except:
	pass
try:
	mode = int(params["mode"])
except:
	pass
try:
	iconimage = urllib.unquote_plus(params["iconimage"])
except:
	pass  

print "Mode: " + str(mode)
print "URL: " + str(url)
print "Name: " + str(name)
print "iconimage: " + str(iconimage)

if mode == None or url == None or len(url)<1:
	main()

elif mode == 1:
	haingoai()

elif mode == 2:
	trongnuoc()

elif mode == 3:
	mediaStations(url)

elif mode == 4:
	NguoiViet()
  
elif mode == 5:
	mediaList(url)
		
elif mode == 6:
	resolveUrl(url)
 
xbmcplugin.endOfDirectory(int(sys.argv[1]))