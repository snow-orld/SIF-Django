from django.conf import settings

import os
import sys
# IMPORTANT for custom modules(i.e. scripts to be able to import by appname.modules.scriptname)
sys.path.append(settings.BASE_DIR)

import analyzer.modules.scraper as scraper
import analyzer.modules.loader as loader

LOCAL_FOLDER = os.path.join(os.path.dirname(__file__), 'local')
print(LOCAL_FOLDER)
