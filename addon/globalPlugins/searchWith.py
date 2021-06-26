# -*- coding: utf-8 -*-
# NVDA Add-on: Search With
# Copyright (C) 2021 ibrahim hamadeh
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file COPYING for more details.

import api
import ui
import gui, wx
from gui import guiHelper
import config
import queueHandler
import languageHandler
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
		# Menu items, or labels of search engines in virtual menu.
		self.menuItems= [name for name, url in engineNameAndUrl]
		self.index= 0

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SearchWithPanel)

	def terminate(self):
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SearchWithPanel)

	def activateMenu(self):
		'''Display virtual menu with its menu items.'''
		#log.info('activating virtual menu ...')
		if self.virtualMenuActive:
			return
		log.info('binding gestures for virtual menu...')
		for key in ('downArrow', 'upArrow', 'leftArrow', 'rightArrow'):
			self.bindGesture(f'kb:{key}', 'moveOnVirtual')
		self.bindGesture('kb:escape', 'closeVirtual')
		self.bindGesture('kb:enter', 'activateMenuItem')
		self.virtualMenuActive= True
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Search With Menu"))
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
			self.index= self.index+1 if self.index!=num-1 else 0
		elif key== 'upArrow':
			self.index= self.index-1 if self.index!=0 else num-1
		ui.message(f"{self.menuItems[self.index]}")

	def script_closeVirtual(self, gesture):
		''' Script to close the virtual menu.'''
		self.clearVirtual()
		# After destroying virtual menu, the focus object does not announce itself
		# So we have to do that explicitly.
		api.getFocusObject().reportFocus()

	def clearVirtual(self):
		''' Helper function to clear the virtual menu.'''
		self.clearGestureBindings()
		self.bindGestures(self.__gestures)
		self.virtualMenuActive= False
		self.index= 0

	def script_activateMenuItem(self, gesture):
		''' Activating a menu item with enter key.'''
		log.info('activating menu item ...')
		text= isSelectedText()
		index= self.index
		# Get the url of the search engine.
		url= engineNameAndUrl[index][1]
		webbrowser.open(url+ text)
		self.clearVirtual()

	def script_searchWith(self, gesture):
		text= isSelectedText()
		if not text:
			# Translators: Message displayed if no text selected.
			ui.message(_("No text selected"))
			return
		scriptCount= scriptHandler.getLastScriptRepeatCount()
		if scriptCount== 0:
			self.activateMenu()
			return
		googleUrl= 'https://google.com/search?q='
		if config.conf["searchWith"]["lang"]== 0:
			lang= ""
		elif config.conf["searchWith"]["lang"]== 1:
			# NVDA language
			lang= languageHandler.getLanguage()
			lang= lang.split('_')[0] if '_' in lang else lang
			log.info(f'nvdaLang: {lang}')
		elif config.conf["searchWith"]["lang"]== 2:
			# Windows language
			lang= languageHandler.getWindowsLanguage()
			lang= lang.split('_')[0] if '_' in lang else lang
			log.info(f'winLang: {lang}')
		langParam= f"&lr=lang_{lang}&hr={lang}" if lang else ""
		webbrowser.open(googleUrl+ text+ langParam)
		self.clearVirtual()

	# Translators: Category of addon in input gestures.
	script_searchWith.category= _("Search With")
	# Translators: Message displayed in input help more.
	script_searchWith.__doc__= _("Open search with menu if pressed once, search with Google directly twice.")

	__gestures= {
	'kb:nvda+e': 'searchWith',
	}

#default configuration 
configspec={
	"lang": "integer(default=0)",
}
config.conf.spec["searchWith"]= configspec

#make  SettingsPanel  class
class SearchWithPanel(gui.SettingsPanel):
	# Translators: title of the dialog
	title= _("Search With")

	def makeSettings(self, sizer):
		settingsSizerHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		# Translators: Languages used in Google search.
		langs= [_("Browser language and setting"), _("NVDA language"), _("Windows language")]
		self.langsComboBox= settingsSizerHelper.addLabeledControl(
		# Translators: label of cumbo box to choose language for Google search.
		_("Choose language used in Google search"), 
		wx.Choice, choices= langs)
		self.langsComboBox.SetSelection(config.conf["searchWith"]["lang"])

	def onSave(self):
		config.conf["searchWith"]["lang"]= self.langsComboBox.GetSelection()
