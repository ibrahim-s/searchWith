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
#Insure one instance of Search with dialog is active.
_searchWithDialog= None

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

class MenuHelper:
	# dictionary of search engines, name and url from json file.
	allItemsDict= None
	# Default search with menu, and the user can change it later from addon setting.
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

def searchWithGoogle(text):
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

class GlobalPlugin(globalPluginHandler.GlobalPlugin):

	def __init__(self, *args, **kwargs):
		super(GlobalPlugin, self).__init__(*args, **kwargs)
		MenuHelper.getAllItemsDict()
		self.virtualMenuActive= False
		# Menu items, or labels of search engines in virtual menu.
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

	def openSearchWithDialog(self):
		''' Open Search with dialog if no text is selected.'''
		global _searchWithDialog
		if not _searchWithDialog:
			dialog= SearchWithDialog(gui.mainFrame)
			dialog.Show()
			_searchWithDialog= dialog
		else:
			_searchWithDialog.Raise()

	def script_searchWith(self, gesture):
		text= isSelectedText()
		if not text:
			self.openSearchWithDialog()
			return
		scriptCount= scriptHandler.getLastScriptRepeatCount()
		if scriptCount== 0:
			self.activateMenu()
			return
		searchWithGoogle(text)
		self.clearVirtual()

	# Translators: Category of addon in input gestures.
	script_searchWith.category= _("Search With")
	# Translators: Message displayed in input help more.
	script_searchWith.__doc__= _("Open search with menu if pressed once, search with Google directly twice.")

	__gestures= {
	'kb:nvda+windows+s': 'searchWith',
	}

#default configuration 
configspec={
	"menuItems": "list(default=list())",
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
		# Translators: List of available items to add from.
		staticMenuSizer.Add(wx.StaticText(staticMenuSizer.GetStaticBox(), label= _("Available items to add from")))
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

		# Group of buttons, remove, move up, move down and set default.
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

		# Translators: In search with dialog group
		staticCheckSizer= sHelper.addItem(wx.StaticBoxSizer(wx.VERTICAL, self, _("In search with dialog")))
		# Translators: Label of checkbox to use last spoken ad default query.
		self.lastSpokenDefault= wx.CheckBox(staticCheckSizer.GetStaticBox(), label=_("Use last spoken as default query"))
		staticCheckSizer.Add(self.lastSpokenDefault)

	def onAdd(self, event):
		#log.info('adding item to  search menu...')
		i= self.availableItems.GetSelection()
		numItems = self.availableItems.GetCount()
		if i== -1:
			return
		item= self.availableItems.GetStringSelection()
		self.customMenu.Append(item)
		self.availableItems.Delete(i)
		core.callLater(100, ui.message, "Information: Item added")
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
		''' Moving item up in Search with menu.'''
		i= self.customMenu.GetSelection()
		item= self.customMenu.GetStringSelection()
		numItems= self.customMenu.GetCount()
		if numItems== 0 or i in (0, -1):
			return
		self.customMenu.Insert(item, i-1)
		self.customMenu.Delete(i+1)
		self.customMenu.SetSelection(i-1)
		core.callLater(100, ui.message, _("Information: item moved up"))

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
		core.callLater(100, ui.message, _("Information: item moved down"))

	def onSetDefault(self, event):
		''' Setting search with menu to default.'''
		self.customMenu.Set(MenuHelper.defaultMenuItems)
		self.customMenu.SetSelection(0)
		core.callLater(100, ui.message, _("Information: Menu set to default"))

	def onSave(self):
		config.conf["searchWith"]["menuItems"]= self.customMenu.GetItems()
		config.conf["searchWith"]["lang"]= self.langsComboBox.GetSelection()
		config.conf["searchWith"]["useLastSpokenAsDefault"]= self.lastSpokenDefault.GetValue()

# Graphical user interface for search with dialog
# It should open if no text is selected.
class SearchWithDialog(wx.Dialog):

	def __init__(self, parent):
		# Translators: Title of dialog
		super(SearchWithDialog, self).__init__(parent, title=_("Search With"))

		mainSizer = wx.BoxSizer(wx.VERTICAL)
		sHelper = guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)

		editTextSizer= guiHelper.BoxSizerHelper(self, orientation=wx.VERTICAL)
		# Translators: Label of static text
		editTextSizer.addItem(wx.StaticText(self, wx.ID_ANY, label= _("Search with google")))
		# Translators: Label of text control to enter query.
		self.editControl= editTextSizer.addLabeledControl(_("Enter a search query"), wx.TextCtrl)
		sHelper.addItem(editTextSizer.sizer)

		# Translators: Label of Other engines button
		self.otherEngines= sHelper.addItem(wx.Button(self, wx.ID_ANY, label= _("Other Engines")))
		self.otherEngines.Bind(wx.EVT_BUTTON, self.onOtherEngines)

		sHelper.addDialogDismissButtons(wx.OK | wx.CANCEL)
		self.Bind(wx.EVT_BUTTON, self.onOk, id=wx.ID_OK)
		self.Bind(wx.EVT_BUTTON, self.onCancel, id=wx.ID_CANCEL)

		mainSizer.Add(sHelper.sizer, border=guiHelper.BORDER_FOR_DIALOGS, flag=wx.ALL)
		mainSizer.Fit(self)
		self.editControl.SetFocus()
		self.CentreOnScreen()
		self.Raise()

	def onOtherEngines(self, event):
		text= self.editControl.GetValue()
		if not text:
			return
		btn = event.GetEventObject()
		pos = btn.ClientToScreen( (0,0) )
		menu= OtherEnginesMenu(self, text)
		self.PopupMenu(menu, pos)
		menu.Destroy()
		#log.info('destroying openWith popup menu')

	def onOk(self, event):
		text= self.editControl.GetValue()
		if not text:
			self.editControl.SetFocus()
			return
		searchWithGoogle(text)
		wx.CallLater(4000, self.Destroy)

	def onCancel(self, event):
		self.Destroy()

# Other Engines menu
class OtherEnginesMenu(wx.Menu):
	''' The menu that pops up when pressing Other Engines button in Search with dialog
	items of this menu are the labels of the Search With menu.
	'''
	def __init__(self, parentDialog, text):
		super(OtherEnginesMenu, self).__init__()
		self.text= text
		self.parentDialog= parentDialog

		#Add menu items for search engines in Search With menu
		for label in MenuHelper.getMenuItems():
			item= wx.MenuItem(self, -1, label)
			self.Append(item)
			self.Bind(wx.EVT_MENU, lambda evt , args=label : self.onActivate(evt, args), item)

	def onActivate(self, event, label):
		#log.info(label)
		url= MenuHelper.allItemsDict[label]
		webbrowser.open(url+ self.text)
		import speech
		speech.cancelSpeech()
		wx.CallLater(3000, self.parentDialog.Destroy)
