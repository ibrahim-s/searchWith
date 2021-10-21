# installTasks.py
# Copyright 2021 Ibrahim Hamadeh , released under GPL2.0
# required to preserve data folder, mainly for advanced users. 

import os
import config
import shutil
from logHandler import log

def onInstall():
	# path of data folder in previously installed version.
	src= os.path.join(os.path.abspath(os.path.dirname(__file__)), '..', 'searchWith', 'data')
	# path of data folder in the pending install version.
	dest= os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

	try:
		preserve= config.conf["searchWith"]["preserveDataFolder"]
	except KeyError:
		log.info("No previous version, or version less than 1.8", exc_info= True)
		return
	else:
		# when we ininstall the addon, configuration stays.
		# So we should make sure that a previous version exist.
		if preserve and os.path.isdir(src):
			# The user wants to preserve data folder.
			try:
				shutil.rmtree(dest, ignore_errors=True)
				shutil.copytree(src, dest)
			except :
				log.info("Error trying to preserve data folder", exc_info= True)
