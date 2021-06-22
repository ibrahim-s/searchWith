# -*- coding: utf-8 -*-
# NVDA Add-on: Search With
# Copyright (C) 2021 ibrahim hamadeh
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file copying for more details.

import api
import ui
import queueHandler
import globalPluginHandler
import textInfos
import scriptHandler
import webbrowser
from logHandler import log
import addonHandler
addonHandler.initTranslation()

def isSelectedText():
	"""this function  specifies if a certain text is selected or not
	and if it is, returns text selected.
	"""
	obj=api.getFocusObject()
	treeInterceptor=obj.treeInterceptor
	if hasattr(treeInterceptor,'TextInfo') and not treeInterceptor.passThrough:
		obj=treeInterceptor
	try:
		info=obj.makeTextInfo(textInfos.POSITION_SELECTION)
	except (RuntimeError, NotImplementedError):
		info=None
	if not info or info.isCollapsed:
		return False
	else:
		return info.text

# Search engines name and url
engineNameAndUrl= (
	('Yahoo', 'https://search.yahoo.com/search/?p='),
	('Bing', 'https://www.bing.com/search?q='),
	('DuckDuckGo', 'https://duckduckgo.com/?q='),
	('Youtube', 'http://www.youtube.com/results?search_query=')
)

class GlobalPlugin(globalPluginHandler.GlobalPlugin):
	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		self.virtualMenuActive= False
		#self.menuItems= ['Yahoo', 'Bing', 'DuckDuckGo', 'Youtube']
		# Menu items, or labels of search engines in virtual menu.
		self.menuItems= [key for key, value in engineNameAndUrl]
		self.index= 0

	def activateMenu(self):
		'''Activate virtual menu with its menu items.'''
		log.info('activating virtual menu ...')
		if self.virtualMenuActive:
			return
		log.info('binding gestures for virtual menu...')
		for key in ('downArrow', 'upArrow', 'leftArrow', 'rightArrow'):
			self.bindGesture(f'kb:{key}', 'moveOnVirtual')
			#self.bindGesture('kb:downArrow', 'movingOnVirtual')
			#self.bindGesture('kb:upArrow', 'movingOnVirtual')
			self.bindGesture('kb:escape', 'closeVirtual')
		self.bindGesture('kb:enter', 'activateMenuItem')
		self.virtualMenuActive= True
		#ui.message("Search With Menu {}".format(self.menuItems[self.index]))
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Search With Menu"))#
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, f"{self.menuItems[self.index]}")
			#log.info('Done binding')

	def script_moveOnVirtual(self, gesture):
		'''Script to help us moving on virtual menu, using up and down arrow.'''
		log.info('under script movingOnVirtual')
		key= gesture.mainKeyName
		if key in ('leftArrow', 'rightArrow'):
			return
		num= len(self.menuItems)
		if key== 'downArrow':
			self.index= self.index+1 if self.index!=3 else 0
		elif key== 'upArrow':
			self.index= self.index-1 if self.index!=0 else num-1
		ui.message(f"{self.menuItems[self.index]}")

	def script_closeVirtual(self, gesture):
		self.clearVirtual()
		# After destroying virtual menu, the focus object does not announce itself
		api.getFocusObject().reportFocus()

	def clearVirtual(self):
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		self.virtualMenuActive= False
		self.index= 0

	def script_activateMenuItem(self, gesture):
		''' Activating a menu item with enter key.'''
		log.info('activating menu item ...')
		text= isSelectedText()
		index= self.index
		"""if index== 0:
			baseUrl= 'https://search.yahoo.com/search/?p='
			webbrowser.open(baseUrl+ text)
		elif index== 1:
			baseUrl= 'https://www.bing.com/search?q='
			webbrowser.open(baseUrl+ text)
		elif index== 2:
			baseUrl= 'https://duckduckgo.com/?q='
			webbrowser.open(baseUrl+ text)
		elif index== 3:
			baseUrl= 'http://www.youtube.com/results?search_query='
			webbrowser.open(baseUrl+ text)
		"""
		# Get the url of the search engine.
		url= engineNameAndUrl[index][1]
		webbrowser.open(url+ text)
		self.clearVirtual()

	def script_searchWitMenu(self, gesture):
		text= isSelectedText()
		if not text:
			# Translators: Message displayed if no text selected.
			ui.message(_("No text selected"))
			return
		#url= 'https://google.com/search?q=%s'%text
		scriptCount= scriptHandler.getLastScriptRepeatCount()
		if scriptCount== 0:
			self.activateMenu()
		else:
			googleUrl= 'https://google.com/search?q='
			webbrowser.open(googleUrl+ text)
			self.clearVirtual()

	__gestures= {
	'kb:nvda+e': 'searchWitMenu',
	}
