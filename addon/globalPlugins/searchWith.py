# -*- coding: utf-8 -*-
# NVDA Add-on: Search With
# Copyright (C) 2021 ibrahim hamadeh
# This add-on is free software, licensed under the terms of the GNU General Public License (version 2).
# See the file COPYING for more details.

import api
import core, ui
import gui, wx
import os, json
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
#engineNameAndUrl= (
	#('Yahoo', 'https://search.yahoo.com/search/?p='),
	#('Bing', 'https://www.bing.com/search?q='),
	#('DuckDuckGo', 'https://duckduckgo.com/?q='),
	#('Youtube', 'http://www.youtube.com/results?search_query=')
#)

class MenuHelper:
	allItemsDict= None
	defaultMenuItems= ['Yahoo', 'Bing', 'DuckDuckGo', 'Youtube']

	@classmethod
	def getAllItemsDict(cls):
		path= os.path.join(os.path.dirname(__file__), "..", "data", "searchEngines.json")
		with open(path, encoding= "utf-8") as f:
			d= json.load(f)
			cls.allItemsDict= d

	@classmethod
	def getItemsToAdd(cls):
		return [key for key in cls.allItemsDict if key not in cls.getMenuItems()]

	@classmethod
	def getMenuItems(cls):
		return config.conf["searchWith"]["menuItems"]

	@classmethod
	def setMenuItems(cls, _list):
		config.conf["searchWith"]["menuItems"]= _list

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		MenuHelper.getAllItemsDict()
		self.virtualMenuActive= False
		# Menu items, or labels of search engines in virtual menu.
		#self.menuItems= MenuHelper.getMenuItems()
		self.menuItems= []
		self.index= 0

		gui.settingsDialogs.NVDASettingsDialog.categoryClasses.append(SearchWithPanel)

	def terminate(self):
			gui.settingsDialogs.NVDASettingsDialog.categoryClasses.remove(SearchWithPanel)

	def activateMenu(self):
		'''Display virtual menu with its menu items.'''
		#log.info('activating virtual menu ...')
		if self.virtualMenuActive:
			return
		#log.info('binding gestures for virtual menu...')
		for key in ('downArrow', 'upArrow', 'leftArrow', 'rightArrow'):
			self.bindGesture(f'kb:{key}', 'moveOnVirtual')
		self.bindGesture('kb:escape', 'closeVirtual')
		self.bindGesture('kb:enter', 'activateMenuItem')
		self.menuItems= MenuHelper.getMenuItems()
		self.virtualMenuActive= True
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, _("Search With Menu"))
		queueHandler.queueFunction(queueHandler.eventQueue, ui.message, f"{self.menuItems[self.index]}")
			#log.info('Done binding')

	def script_moveOnVirtual(self, gesture):
		'''Script to help us moving on virtual menu, using up and down arrow.'''
		#log.info('under script movingOnVirtual')
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
		#log.info('activating menu item ...')
		text= isSelectedText()
		index= self.index
		# Get the url of the search engine.
		url= MenuHelper.allItemsDict[MenuHelper.getMenuItems()[index]]
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
			#log.info(f'nvdaLang: {lang}')
		elif config.conf["searchWith"]["lang"]== 2:
			# Windows language
			lang= languageHandler.getWindowsLanguage()
			lang= lang.split('_')[0] if '_' in lang else lang
			#log.info(f'winLang: {lang}')
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
	"menuItems": "list(default=list())",
	#"menuItems": "'option(),
	"lang": "integer(default=0)",
	"useLastSpokenAsDefault": "boolean(default=False)",
}
config.conf.spec["searchWith"]= configspec
if not config.conf["searchWith"]["menuItems"]:
	config.conf["searchWith"]["menuItems"]= MenuHelper.defaultMenuItems

#make  SettingsPanel  class
class SearchWithPanel(gui.SettingsPanel):
	# Translators: title of the dialog
	title= _("Search With")

	def makeSettings(self, sizer):
		sHelper = guiHelper.BoxSizerHelper(self, sizer=sizer)

		staticMenuSizer= sHelper.addItem(wx.StaticBoxSizer(wx.VERTICAL, self, "Menu"))
		staticMenuSizer.Add(wx.StaticText(staticMenuSizer.GetStaticBox(), label= _("Available items to add from")))
		# Translators: List of available items to add from.
		#self.availableItems= sHelper.addLabeledControl(_("Available items to add from"),
		#self.availableItems= wx.ListBox(staticMenuSizer.GetStaticBox(), choices= ['apple', 'orange', 'banana', 'cherry'])
		self.availableItems= wx.ListBox(staticMenuSizer.GetStaticBox(), choices= [])
		staticMenuSizer.Add(self.availableItems)
		self.availableItems.Set(MenuHelper.getItemsToAdd())
		self.availableItems.SetSelection(0)

		# Translators: Label of add button.
		addButton= wx.Button(staticMenuSizer.GetStaticBox(), label=_("Add to menu"))
		staticMenuSizer.Add(addButton)
		addButton.Bind(wx.EVT_BUTTON, self.onAdd)

		# Translators: Search with menu items.
		staticMenuSizer.Add(wx.StaticText(staticMenuSizer.GetStaticBox(), label= _("Search with menu")))
		self.customMenu=wx.ListBox(staticMenuSizer.GetStaticBox(), choices= [])
		staticMenuSizer.Add(self.customMenu)
		self.customMenu.Set(MenuHelper.getMenuItems())
		self.customMenu.SetSelection(0)

		buttonGroup = guiHelper.ButtonHelper(wx.VERTICAL)
		# Translators: Label of remove button.
		removeButton= buttonGroup.addButton(self, label= _("Remove"))
		removeButton.Bind(wx.EVT_BUTTON, self.onRemove)
		# Translators: Label of move up button.
		moveUpButton= buttonGroup.addButton(self, label= _("Move item up"))
		moveUpButton.Bind(wx.EVT_BUTTON, self.onMoveUp)
		# Translators: Label of move down button.
		moveDownButton= buttonGroup.addButton(self, label= _("Move item down"))
		moveDownButton.Bind(wx.EVT_BUTTON, self.onMoveDown)
		# Translators: Label of set menu to default button.
		setDefaultButton= buttonGroup.addButton(self, label= _("Set menu to default"))
		setDefaultButton.Bind(wx.EVT_BUTTON, self.onSetDefault)
		sHelper.addItem(buttonGroup)

		# Translators: Languages used in Google search.
		langs= [_("Browser language and setting"), _("NVDA language"), _("Windows language")]
		staticCumboSizer= sHelper.addItem(wx.StaticBoxSizer(wx.VERTICAL, self, "In Google search"))
		staticCumboSizer.Add(wx.StaticText(staticCumboSizer.GetStaticBox(), label= "Use:"))
		self.langsComboBox= wx.Choice(
		staticCumboSizer.GetStaticBox(),
		choices= langs)
		staticCumboSizer.Add(self.langsComboBox)
		self.langsComboBox.SetSelection(config.conf["searchWith"]["lang"])

		# Translators:
		staticCheckSizer= sHelper.addItem(wx.StaticBoxSizer(wx.VERTICAL, self, _("In search with dialog")))
		self.lastSpokenDefault= wx.CheckBox(staticCheckSizer.GetStaticBox(), label=_("Use last spoken as default query"))
		staticCheckSizer.Add(self.lastSpokenDefault)

	def onAdd(self, event):
		log.info('adding item to  search menu...')
		i= self.availableItems.GetSelection()
		numItems = self.availableItems.GetCount()
		if i== -1:
			return
		item= self.availableItems.GetStringSelection()
		self.customMenu.Append(item)
		self.availableItems.Delete(i)
		core.callLater(100, ui.message, "Information: Item added")
		#numItems = self.availableItems.GetCount()
		if numItems== 1:
			return
		newIndex= i if i!= numItems-1 else i-1
		self.availableItems.SetSelection(newIndex)

	def onRemove(self, event):
		''' Removing an item from search with menu.'''
		i= self.customMenu.GetSelection()
		item= self.customMenu.GetStringSelection()
		numItems = self.customMenu.GetCount()
		if i==-1 or not numItems:
			return
		self.customMenu.Delete(i)
		self.availableItems.Append(item)
		core.callLater(100, ui.message, _("Information: item removed"))
		newIndex= i if i!= numItems-1 else i-1
		if newIndex< 0:
			return
		self.customMenu.SetSelection(newIndex)

	def onMoveUp(self, event):
		i= self.customMenu.GetSelection()
		item= self.customMenu.GetStringSelection()
		numItems= self.customMenu.GetCount()
		if numItems== 0 or i in (0, -1):
			return
		self.customMenu.Insert(item, i-1)
		self.customMenu.Delete(i+1)
		self.customMenu.SetSelection(i-1)
		core.callLater(100, ui.message, _("Item moved up"))

	def onMoveDown(self, event):
		''' Moving an item down in search with menu.'''
		i= self.customMenu.GetSelection()
		item= self.customMenu.GetStringSelection()
		numItems= self.customMenu.GetCount()
		if numItems== 1 or i in (numItems-1, -1):
			return
		self.customMenu.Insert(item, i+2)
		self.customMenu.Delete(i)
		self.customMenu.SetSelection(i+1)
		core.callLater(100, ui.message, _("Item moved down"))

	def onSetDefault(self, event):
		''' Setting search with menu to default.'''
		self.customMenu.Set(MenuHelper.defaultMenuItems)
		self.customMenu.SetSelection(0)
		core.callLater(100, ui.message, _("Information: Menu set to default"))

	def onSave(self):
		config.conf["searchWith"]["menuItems"]= self.customMenu.GetItems()
		config.conf["searchWith"]["lang"]= self.langsComboBox.GetSelection()
		config.conf["searchWith"]["useLastSpokenAsDefault"]= self.lastSpokenDefault.GetValue()
