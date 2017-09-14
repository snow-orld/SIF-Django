#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file    loader.py
@author  Cecilia M.
@date    2017-09-13
@version $Id: loader.py 01 2017-09-13 19:25:09 behrisch $

This script loads the parsed event and member data from local parsed file
to django.

The memthods in this module should be called by django cron to keep data updated.

Make Sure:
Already loaded data into db do not need to be added. Performacne concern.
"""

from django.conf import settings
from analyzer.modules.constants import *

class Loader():
	"""Load new data into database if newly updated. Manage the analyzer app's data lifetime."""
	def __init__(self):
		self.load()

	def load(self):
		# Check if local files have been updated
		event_folder = os.path.join()

