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

import urllib, urllib2, re, os, sys, shutil
import xbmc, xbmcplugin, xbmcgui, xbmcaddon

mysettings = xbmcaddon.Addon(id = 'plugin.program.addonCreator')
profile = mysettings.getAddonInfo('profile')
home = mysettings.getAddonInfo('path')
fanart = xbmc.translatePath(os.path.join(home, 'fanart.jpg'))
icon = xbmc.translatePath(os.path.join(home, 'icon.png'))
logos = xbmc.translatePath(os.path.join(home, 'resources', 'logos\\'))

name_of_plugin_folder = mysettings.getSetting('name_of_plugin_folder')
my_first_addon = xbmc.translatePath('special://home/addons/plugin.video.' + name_of_plugin_folder)
name_of_addon = mysettings.getSetting('name_of_addon')
addon_version_number = mysettings.getSetting('addon_version_number')
provider_name = mysettings.getSetting('provider_name')
addon_icon = mysettings.getSetting('addon_icon')
addon_fanart = mysettings.getSetting('addon_fanart')
sum_mary = mysettings.getSetting('sum_mary')
desc = mysettings.getSetting('desc')
m3u_file = mysettings.getSetting('m3u_file')
xml_file = mysettings.getSetting('xml_file')
m3u_regex = '#.+,(.+?)\n(.+?)\n'
xml_regex = '<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>'

def open_file(file):
	try:
		f = open(file, 'r')
		content = f.read()
		f.close()
		return content	
	except:
		pass 
		
def home():
	add_dir('[COLOR yellow]Create XBMC/Kodi add-on [COLOR cyan]from m3u/xml playlist[COLOR white][B] - NO REGEX[/B][/COLOR]', 'AddonCreator', 1, logos + 'xml.png', fanart)

def create_addon():
	if (len(m3u_file) > 0) or (len(xml_file) > 0) and ((len(name_of_plugin_folder) > 0) and (len(name_of_addon) > 0) and (len(addon_version_number) > 0) and (len(provider_name) > 0) and (len(addon_icon) > 0) and (len(addon_fanart) > 0) and (len(sum_mary) > 0) and (len(desc) > 0)):
		try:		
			# Delete add-on folder if exist and create new empty folder for add-on.
			try:
				shutil.rmtree(my_first_addon)
			except:
				pass				
			os.mkdir(my_first_addon)
			
			# Create default.py
			f = open(my_first_addon + '/default.py', 'w')
			
			f.write('# -*- coding: utf-8 -*-\n\n')
			
			f.write('import xbmc, xbmcgui, xbmcplugin, sys, re\n\n')
			
			f.write('plugin_handle = int(sys.argv[1])\n')
			f.write('xbmcplugin.setContent(plugin_handle, "video")\n')
			f.write('icon = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/icon.png")\n')
			f.write('fanart = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/fanart.jpg")\n')
			f.write('m3u_playlist = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/playlist.m3u")\n')		
			f.write('xml_playlist = xbmc.translatePath("special://home/addons/plugin.video.' + name_of_plugin_folder + '/playlist.xml")\n')
			f.write('xml_regex = "<title>(.*?)</title>\s*<link>(.*?)</link>\s*<thumbnail>(.*?)</thumbnail>"\n')	
			f.write('m3u_regex = "#.+,(.+?)\\n(.+?)\\n"\n\n')
			
			f.write('def open_file(file):\n' + '    try:\n' + '        f = open(file, "r")\n' + '        content = f.read()\n' + '        f.close()\n' + '        return content\n' + '    except:\n' + '        pass\n\n') 			

			f.write('def add_item(url, infolabels, img = "", fanart = ""):\n' + '    listitem = xbmcgui.ListItem(infolabels["title"], iconImage = img, thumbnailImage = img)\n' + '    listitem.setInfo("video", infolabels)\n' + '    listitem.setProperty("fanart_image", fanart)\n' + '    listitem.setProperty("IsPlayable", "false")\n' + '    xbmcplugin.addDirectoryItem(plugin_handle, url, listitem)\n' + '    return\n\n')			

			f.write('try:\n')			
			f.write('    link = open_file(m3u_playlist)\n')        			
			f.write('    match = re.compile(m3u_regex).findall(link)\n')			
			f.write('    for title, url in match:\n')
			f.write('        try:\n')        
			f.write('            url = url.replace(\'"\', \' \').replace(\'&amp;\', \'&\').strip()\n')
			f.write('            title = re.sub(\'\s+\', \' \', title).replace(\'"\', \' \').strip()\n')
			f.write('            add_item(url, {"title": title}, icon, fanart)\n')
			f.write('        except:\n')
			f.write('            pass\n')
			f.write('except:\n')
			f.write('    pass\n\n')
			
			f.write('try:\n')			
			f.write('    link = open_file(xml_playlist)\n')        			
			f.write('    match = re.compile(xml_regex).findall(link)\n')			
			f.write('    for title, url, thumb in match:\n')
			f.write('        try:\n')        
			f.write('            url = url.replace(\'"\', \' \').replace(\'&amp;\', \'&\').strip()\n')
			f.write('            title = re.sub(\'\s+\', \' \', title).replace(\'"\', \' \').strip()\n')
			f.write('            if (len(thumb) > 0):\n')
			f.write('                add_item(url, {"title": title}, thumb, thumb)\n')	
			f.write('            else:\n')
			f.write('                add_item(url, {"title": title}, icon, fanart)\n')			
			f.write('        except:\n')
			f.write('            pass\n')
			f.write('except:\n')
			f.write('    pass\n\n')			
					
			f.write('xbmcplugin.endOfDirectory(plugin_handle)\n' + 'sys.exit(0)')				
			f.close()
			
			# Create addon.xml
			f = open(my_first_addon + '/addon.xml', 'w')			
			f.write('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>\n')
			f.write('<addon id="plugin.video.' + name_of_plugin_folder + '" name="' + name_of_addon.replace('\[', '[').replace('\]', ']') + '" version="' + addon_version_number + '" provider-name="' + provider_name.replace('\[', '[').replace('\]', ']') + '">\n')			
			#f.write('    <requires>\n' + '        <import addon="xbmc.python" version="2.1.0" optional="true" />\n' + '    </requires>\n')
			f.write('    <requires>\n' + '    </requires>\n') # Requires nothing
			f.write('    <extension point="xbmc.python.pluginsource"\n' + '               library="default.py">\n' + '        <provides>video</provides>\n' + '    </extension>\n')
			f.write('    <extension point="xbmc.addon.metadata">\n' + '        <platform>all</platform>\n' + '        <summary>' + sum_mary.replace('\[', '[').replace('\]', ']') + '</summary>\n' + '        <description>' + desc.replace('\[', '[').replace('\]', ']') + '</description>\n' + '    </extension>\n')
			f.write('</addon>')			
			f.close()

			# Copy icon, fanart, playlist(s) to plugin folder, then rename them.
			shutil.copy(addon_icon, my_first_addon)
			shutil.copy(addon_fanart, my_first_addon)
			shutil.copy(m3u_file, my_first_addon)
			shutil.copy(xml_file, my_first_addon)			
			os.rename(xbmc.translatePath(os.path.join(my_first_addon, addon_icon.split('/')[-1].split('\\')[-1])), xbmc.translatePath(os.path.join(my_first_addon, 'icon.png')))					
			os.rename(xbmc.translatePath(os.path.join(my_first_addon, addon_fanart.split('/')[-1].split('\\')[-1])), xbmc.translatePath(os.path.join(my_first_addon, 'fanart.jpg')))		
			os.rename(xbmc.translatePath(os.path.join(my_first_addon, m3u_file.split('/')[-1].split('\\')[-1])), xbmc.translatePath(os.path.join(my_first_addon, 'playlist.m3u')))		
			os.rename(xbmc.translatePath(os.path.join(my_first_addon, xml_file.split('/')[-1].split('\\')[-1])), xbmc.translatePath(os.path.join(my_first_addon, 'playlist.xml')))					

			# Conclusion.
			xbmcgui.Dialog().ok('Add-on Creator', '[COLOR red][B]Please manually reboot XBMC/Kodi.[/B][/COLOR]', '[B]Then look for your add-on in VIDEOS >> add-ons.[/B]', 'Done. Enjoy!')			
		except:	
			xbmcgui.Dialog().ok('Add-on Creator', '[COLOR red][B]Oops! Something has gone terribly wrong.[/B][/COLOR]', '[B]Double check ALL settings.[/B]', 'Then try again.')
	else:	
		mysettings.openSettings()
	
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
	home()

elif mode == 1:
	create_addon()
	sys.exit(0)

xbmcplugin.endOfDirectory(int(sys.argv[1]))