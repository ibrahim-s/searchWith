# Search With #

*	Author: Ibrahim Hamadeh
*	Download [Stable version 2.5.3][1]
*	NVDA compatibility: 2019.3 and beyond

This addon helps you to search text, via various search engines.  
Let no text selected, and press the gesture of the addon  
A dialog will be displayed, with an edit box to enter a search query  
To search with Google press enter, or tab to search with other engines.  
Or  
select some text and press once, a menu will be displayed with various search engines to choose.  
And while text is selected, you can press the gesture twice to search with Google directly.  
The Default gesture for the addon is: NVDA+ Windows+ S.  
If the keystroke do not work for you, or conflict with other keystroke,  
you can as always add a gesture or change the existent one going to :  
NVDA menu>preferences>inputGestures>Search With category.  

## Usage ##

*	If you want to enter a search query, just press the addon gesture  
*	A dialog will be displayed, with an edit field to enter the search term.  
Want to search with Google? just press enter  
*	Otherwise tab to Other Engines button, and give it a space  
*	A popup menu will show up, with various search engines to choose.  
Yahoo, Bing, DuckDuckGo, and Youtube.  
This is the default menu, and you may modify it from addon's setting panel.  
*	Another way to use the addon, is by selecting some text  
And on Pressing the addon's gesture, or any other you have assigned to it  
a virtual menu will be displayed with various search engines  
Either the default menu, or any other you have tailed to your needs.  
*	Choose one and press enter, the default browser will open displaying search results.  
Or, if you want to search with Google directly  
press the gesture twice, and you are done.  
*	Want to trigger search menu specifically for clipboard or last spoken text?  
You can from input gestures dialog, assigned a gesture for:  
	*	Trigger search menu for clipboard text, and pressed twice searches that text by Google directly.  
	*	Trigger search menu for last spoken text, and pressed twice searches that text by Google directly.  
*	Now if you ask, can I modify Search with menu?  
*	Yes you  can do that from the setting panel,  and adjust the menu to fit to your mood and needs.  
*	You can from there, add to Search with menu, other available search engines  
*	And you can if you like, remove an item from it, move item up, move item down, or return and set it to default state.  
*	If you want these modifications to be permanent, you have to save configuration after wards.  
*	Want to search Google using other language options?  
Go to, Search With category in setting panels  
From the cumbo box there, you can choose search Google either:  
	1.	Using browser settings and language.  
	2.	Using NVDA language.  
	3.	Using windows language.  
*	Now, you have the option to choose the default query in Search with dialog  
from the Options for default query combo box in setting panel, you can choose either  
	*	Leave blank
	*	Use clipboard text
	*	Use last spoken text  
And if clipboard or last spoken text is chosen, text in search box will be displayed selected, so that you can easily override it.  
*	Now let's choose the target language for translate engines, Google Translate and DeepL translator.
*	Still in setting panel, under Translation engines group, there are two combo boxes, one for Google Translate and the other for DeepL Translator. Choose the target language you want for each of them and you are done.
*	Lastly, especially for advanced users  
You can through a check box in setting panel, choose if you want to preserve your data folder upon installing a new version.  
This means that your data will be sustained, but added to it the newly entries in the new version.  
And that's it, hope to search for good and find it, happy searching!  

### Changes for 2.5.3 ###

*	Add DeepL translator to available engines.
*	Add two combo boxes in setting panel, to choose target language for Google translate and DeepL translator.

### Changes for 2.5 ###

*	Return the name of the addon to 'searchWith'(camel case).
*	Add Google Scholar to available engines.

### Changes for 2.4 ###

*	Localization and documentation updates.

### Changes for 2.3 ###

*	Now choosing to preserve data from setting panel, does not means that you will not get the new data entries  
but the new entries in the new version, will be merged and added to your old data file.  
*	Update last tested version to 2023.1 to comply with NVDA version 2023.1.

### Changes for 2.2 ###

*	Add localization and documentation updates.

### Changes for 2.0 ###

*	Disable the addon in secure mode.
*	Update last tested version to 2022.1, to comply with recent addon api version.

### Changes for 1.9 ###

*	Localization and documentation updates.

### Changes for 1.8 ###

*	Add a check box in setting panel, to let advanced users preserve their data folder.  
*	Add two new entries in input gestures:  
	*	trigger search menu for clipboard text, press twice searches Google directly.  
	*	Trigger search menu for last spoken text, press twice searches Google directly.  

### Changes for 1.7 ###

*	Make a combo box in addon's setting, to choose an option for default query in search with dialog.  
*	You can select either Leave blank, Use clipboard text, or Use last spoken text.  

### Changes for 1.6 ###

*	Add tew new sites or search engines:
	*	Google Translate
	*	NVDA Issues On GitHub
*	Use script decorators, instead of traditional script gesture way.

### Changes for 1.5 ###

*	Fixing a serious bug, by escaping special characters in the query string, before including it in the url.

### Changes for 1.4 ###

*	Add localization updates .
*	Remove some doc strings under script functions, not suitable be shown in input gestures.

### Changes for 1.2 ###

*	Add translations for Portuguese (Brazil), Portuguese (Portugal), and Turkish.
*	Add translations for Chinese (Simplified, China)

### Changes for 0.7 ###

*	Add more sites that could be added to menu, such as Stackoverflow, Stackexchange, GoogleBooks and others.  
*	Add the options to use last spoken text as default query, in search with dialog.  

### Changes for 0.4 ###

*	Add a dialog if no text selected, to enter a search query.  
*	Make possible to modify Search with menu from setting panel, to fit to user needs.  

### Changes for 0.3 ###

*	Add setting panel, giving more language options in Google search.  

### Changes for 0.1 ###

*	Initial version  

[1]: https://github.com/ibrahim-s/searchWith/releases/download/2.5.3/searchWith-2.5.3.nvda-addon
