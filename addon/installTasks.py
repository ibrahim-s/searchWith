# installTasks.py
# Copyright 2021 Ibrahim Hamadeh , cary-rowen, released under GPL2.0
# required to preserve data mainly for advanced users. 

import os
import config
import json
from logHandler import log


def onInstall():
	# path of data in previously installed version.
	src= os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'searchWith', 'data', 'otherEngines.json')
	# path of data in the pending install version.
	dest= os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data', 'otherEngines.json')

	try:
		preserve= config.conf["searchWith"]["preserveDataFolder"]
	except KeyError:
		log.info("No previous version, or version less than 1.8", exc_info= True)
		return
	else:
		# when we ininstall the addon, configuration stays.
		# So we should make sure that a previous version exist.
		if preserve and os.path.exists(src):
			# The user wants to preserve data
			try:
				with open(src, 'r', encoding='utf-8') as s, open(dest, 'r', encoding='utf-8') as d:
					src_Data = json.load(s)
					dest_Data = json.load(d)
				#if the two dictionaries are similar we return early
				if src_Data == dest_Data:
					return
				# Merge dictionaries, but keep user data, while updating newly added entries
				merge_Data={**dest_Data, **src_Data}
				# Just save the merged dictionary
				with open(dest, 'w', encoding='utf-8') as f:
					json.dump(merge_Data, f, indent=4, sort_keys=False, ensure_ascii=False)
			except:
				log.error("Error trying to preserve data", exc_info= True)
