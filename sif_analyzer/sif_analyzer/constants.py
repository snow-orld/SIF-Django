#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file    constants.py
@author  Cecilia M.
@date    2017-08-30
@version $Id: constants.py 02 2017-09-04 11:17: behrisch $

This file contains constants used in the process of parsing and 
analyzing the past events of Japanese version 
based on a local parsed file with info from the wiki page
decaf.kouhi.me/lovelive/index.php?title=List_of_Events
"""

URL = "http://decaf.kouhi.me/lovelive/index.php?title=List_of_Events"
BASEURL = "http://decaf.kouhi.me"
WEBPAGEFILE = "events.html"
PARSEDFILE = "events.txt"

EVENTTYPES = ['Collection Event', 'Score Match', 'Medley Festival', 'Challenge Festival', 'Touring Rally', 'Friendly Match']

GROUPS = [u"u's", u'aqours']
US = ['Honoka', 'Kotori', 'Umi', 'Hanayo', 'Rin', 'Maki', 'Eli', 'Nozomi', 'Nico']
AQOURS = ['Chika', 'You', 'Riko', 'Hanamaru', 'Ruby', 'Yoshiko', 'Dia', 'Kanan', 'Mari']

UNITS = ['Printemps', 'Lily White', 'BiBi', 'CYaRon!', 'AZALEA', 'Guilty Kiss']
GRADES = ['1st Year', '2nd Year', '3rd Year']

CARDATTRIBUTES = ['Smile', 'Pure', 'Cool']
CARDRANKS = ['N', 'R', 'SR', 'SSR', 'UR', 'UR-GIFT']

XMLHEADER = '<?xml version="1.0" encoding="UTF-8"?>'
MEMBERPROFILESUFFIX = "_basicinfo.xml"

