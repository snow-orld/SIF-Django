#!/user/bin/env python
# -*- coding: utf8 -*-
"""
@file    scraper.py
@author  Cecilia M.
@date    2017-09-13
@version $Id: scraper.py 01 2017-09-13 15:09:42 behrisch $

This script parses and caches the event/member/card data of
Japanese version from the wiki page decaf.kouhi.me/lovelive/index.php

The memthods in this module should be called by django cron to keep data updated.

Improvements:
Use Django's cache framework.
"""

import os
import sys
import requests
import codecs
from bs4 import BeautifulSoup
from datetime import datetime, date
import re
import time

from analyzer.modules.constants import *

# Parsing event_page data, generate local parsed events file as a csv with delimeter ';'
class EventScraper():
	
	def __init__(self, rootfolder):
		self.folder = os.path.join(rootfolder, 'cached_events')
		self.html_file = os.path.join(self.folder, EVENT_HTML_FILE)
		self.parsed_file = os.path.join(self.folder, EVENT_PARSED_FILE)
		if not os.path.exists(self.folder):
			os.mkdir(self.folder)
		self.fetch_webpage()

	def fetch_webpage(self):
		do_fetch = False

		r = requests.head(EVENT_URL)
		header = r.headers
		last_modified = datetime.strptime(header['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')

		if not os.path.exists(self.html_file):
			do_fetch = True

		elif datetime.utcfromtimestamp(os.path.getmtime(self.html_file)) < last_modified:
			do_fetch = True

		if do_fetch:
			r = requests.get(EVENT_URL)
			with codecs.open(self.html_file, 'w', encoding='utf-8') as f:
				f.write(r.text)

	def parse(self):
		do_parse = False

		if not os.path.exists(self.parsed_file):
			do_parse = True
		elif os.path.getmtime(self.parsed_file) < os.path.getmtime(self.html_file):
			do_parse = True

		if do_parse:
			htmlf = codecs.open(self.html_file, 'r', encoding='utf-8')
			soup = BeautifulSoup(htmlf, 'html.parser')
			htmlf.close()

			with codecs.open(self.parsed_file, 'w', encoding='utf-8') as f:
				rows = soup.findAll('tr')
				headers = rows[0:2]

				rank_cutoff_leftrows_1 = 0; last_rank_cutoff_1 = 0
				rank_cutoff_leftrows_2 = 0; last_rank_cutoff_2 = 0
				rank_cutoff_leftrows_3 = 0; last_rank_cutoff_3 = 0

				for row in rows[2:]:
					cols = row.findAll('td')

					period = cols[0].text.strip()
					name = cols[1].text.strip()
					eventlink = cols[1].a['href']
					pointsSR = cols[2].text.strip()
					pointsSRLink = cols[2].a['href']

					current_colindex = 3

					if period > "2016/06/05":
						# beginning of Aqour's first round event with two SR rewarded each time
						rankingSR = cols[3].text.strip()
						rankingSRLink = cols[3].a['href']
						current_colindex = 4
					else:
						rankingSR = u'N/A'
						rankingSRLink = u'N/A'

					cols = cols[current_colindex:]

					note = u'N/A'

					try:
						int(cols[-1].text.strip())
					except:
						note = cols[-1].text.strip()
						if note != '-':
							cols = cols[:-1]
						if note == '':
							note = u'N/A'

					# cols are left with only the 1st, 2nd, and 3rd's point and rank cutoff, special case for rank cutoff	
					current_colindex = 0

					point_cutoff_1 = cols[0].text.strip()
					current_colindex += 1
					
					if rank_cutoff_leftrows_1 == 0:
						if 'rowspan' in cols[current_colindex].attrs:
							rank_cutoff_leftrows_1 = int(cols[current_colindex]['rowspan'])
						else:
							rank_cutoff_leftrows_1 = 1
						last_rank_cutoff_1 = cols[current_colindex].text.strip()
						current_colindex += 1
					
					rank_cutoff_1 = last_rank_cutoff_1
					rank_cutoff_leftrows_1 -= 1

					point_cutoff_2 = cols[current_colindex].text.strip()
					current_colindex += 1
					
					if rank_cutoff_leftrows_2 == 0:
						if 'rowspan' in cols[current_colindex].attrs:
							rank_cutoff_leftrows_2 = int(cols[current_colindex]['rowspan'])
						else:
							rank_cutoff_leftrows_2 = 1
						last_rank_cutoff_2 = cols[current_colindex].text.strip()
						current_colindex += 1
					
					rank_cutoff_2 = last_rank_cutoff_2
					rank_cutoff_leftrows_2 -= 1

					# third tier point cut off is not available until 2016/6/5, i.e. when double SR rewards begins
					point_cutoff_3 = cols[current_colindex].text.strip()
					current_colindex += 1
					
					if rank_cutoff_leftrows_3 == 0:
						if 'rowspan' in cols[current_colindex].attrs:
							rank_cutoff_leftrows_3 = int(cols[current_colindex]['rowspan'])
						else:
							rank_cutoff_leftrows_3 = 1
						last_rank_cutoff_3 = cols[current_colindex].text.strip()
						current_colindex += 1
					
					rank_cutoff_3 = last_rank_cutoff_3
					rank_cutoff_leftrows_3 -= 1

					f.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (period, name, eventlink, pointsSR, pointsSRLink, rankingSR, rankingSRLink, point_cutoff_1, rank_cutoff_1, point_cutoff_2, rank_cutoff_2, point_cutoff_3,rank_cutoff_3, note))

class MemberScraper():

	def __init__(self, rootfolder):
		self.folder = os.path.join(rootfolder, 'cached_member')

	def fetch_webpage(self, name=None):
		if name == None:
			return

		do_fetch = False

		url = BASE_URL + MEMBER_URLS[name]
		fullname = FULLNAME[name]
		member_folder = os.path.join(self.folder, fullname)
		filename = os.path.join(member_folder, fullname + '.html')

		if not os.path.exists(member_folder):
			os.makedirs(member_folder, exist_ok=True)

		if not os.path.exists(filename):
			do_fetch = True
		else:
			r = requests.head(url)
			header = r.headers
			last_modified = datetime.strptime(header['Last-Modified'], '%a, %d %b %Y %H:%M:%S %Z')

			if datetime.utcfromtimestamp(os.path.getmtime(filename)) < last_modified:
				do_fetch = True

		if do_fetch:
			print('\nRetriving %s\'s file ...' % fullname)	# Future work: animating with progress

			r = requests.get(url)
			with codecs.open(filename, 'w', encoding='utf-8') as f:
				f.write(r.text)
		else:
			print('\n%s\'s file is up-to-date.' % fullname)

	def li2xml(self, li):
		tag = li.b.string.split(':')[0].replace(' ', '_')
		context = li.text.split(':')[1].strip()
		return '%s<%s>%s</%s>\n' % ('	', tag, context, tag)

	def parse(self, name=None):
		if name == None:
			return

		fullname = FULLNAME[name]
		member_folder = os.path.join(self.folder, fullname)
		html_file = os.path.join(member_folder, fullname + '.html')
		basic_file = os.path.join(member_folder, fullname + MEMBER_PROFILE_SUFFIX)
		parsed_file = os.path.join(member_folder, fullname + '.txt')

		if not os.path.exists(html_file):
			self.fetch_webpage(name)

		htmlf = codecs.open(html_file, 'r', encoding='utf-8')
		soup = BeautifulSoup(htmlf, 'html.parser')
		htmlf.close()

		# member basic info file, only created once
		if not os.path.exists(basic_file) or os.stat(basic_file).st_size == 0:
			print('Parsing %s\'s character profile to %s ...' % (fullname, fullname + MEMBER_PROFILE_SUFFIX))

			with codecs.open(basic_file, 'w', encoding='utf-8') as f:
				f.write(XML_HEADER + '\n')
				f.write('<characterprofile>\n')
				for li in soup.table.findAll('li'):
					f.write(self.li2xml(li))
				f.write('%s<%s>%s</%s>\n' % ('	', 'description', soup.table.find('p').getText().strip(), 'description'))
				f.write('</characterprofile>\n')

		# card file
		if not os.path.exists(parsed_file) or os.stat(parsed_file).st_size < 128 or os.path.getmtime(parsed_file) < os.path.getmtime(html_file):
			print('Parsing %s\'s cards profile to %s ...' % (fullname, fullname + '.txt'))

			# parse cards - find all tags between #Cards and #Side_Stories
			tags = []
			for tag in soup.find('span', id='Cards').find_parent().next_siblings:
				# next_siblings can be a bs4.element.Tag or a bs4.element.NavigableString (i.e. with only one child string)
				if tag.string == '\n':
					continue
				if tag.find('span', id='Side_Stories'):
					break
				tags.append(tag)

			with codecs.open(parsed_file, 'w', encoding='utf-8') as f:
				# write csv header
				f.write('cardid;rank;attribute;normalimagelink;idolizedimagelink;smile;pure;cool;skill;effect;leaderskill;leadereffect;version;realeasedate')

				rank = ''	# current rank for current cards, since rank appears before all cards under it
				isprevdate = True	# each release date coming after one card if any, a flag to show whether the last row is a release date

				for tag in tags:
					if tag.name == 'h3':
						rank = tag.string[:-1]
						if rank == 'Rare':
							rank = 'R'
						if rank == 'Super Rare':
							rank = 'SR'
						if rank == 'Super Super Rare':
							rank = 'SSR'
						if rank == 'Ultra Rare':
							rank = 'UR'
					elif tag.name == 'table':
						rows = tag.findAll('tr')
						header = rows[0].th.span
						attribute = COLOR_TO_ATTRIBUTES[header['style'].split(';')[0].split(':')[1].strip()]
						cardid = header.string.split('[')[1].split(']')[0].split(' ')[-1]
						version = 'N/A'
						version_match = re.search('\((.*)\)', header.string)
						if version_match:
							version = version_match.group(1)
						# print(version.encode('cp932', 'ignore').decode('cp932'))
						
						# row[1] - two images (3 row/each), Max level: 60(4 col)
						images = rows[1].findAll('td')[:2]
						normalimagelink = 'N/A'
						if rows[1].td.text.find('This card comes pre') > -1:
							version = 'pretransformed'
						else:
							# normalimagelink = fetchimagelink(BASE_URL+images[0].a['href'])
							normalimagelink = BASE_URL+images[0].a['href']
						idolizedimagelink = BASE_URL+images[1].a['href']

						# row[2] - hp, smile, pure, cool
						smile, pure, cool = [int(td.span.string) for td in rows[2].findAll('td')[1:]]

						# row[3] - skills, two sets in <p> tags under the only <td>, in between there is <p><br /></p> each
						skillsets = rows[3].findAll('p')[0::2]
						try:
							skill = skillsets[0].contents[2].string.split(':')[1].strip()
						except:
							skill = skillsets[0].contents[2].text.split(':')[1].strip()
						effect = skillsets[0].contents[4].strip()
						leaderskill = skillsets[1].contents[2].string.split(':')[1].strip()
						leadereffect = skillsets[1].contents[4].strip()
					
						if not isprevdate:
							f.write('N/A')	# last card's release date is not specified, give it a N/A

						f.write('\n%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;' % (cardid, rank, attribute, normalimagelink, idolizedimagelink, smile, pure, cool, skill, effect, leaderskill, leadereffect, version))

						isprevdate = False

					elif tag.name == 'p':
						isprevdate = True
						if not tag.i:
							# print(tag, tag.previous_element, tag.next_element)
							continue
						if tag.i.string:
							# print(tag.i.string)
							releasetext = tag.i.string
						else:
							# print(tag.i.text)
							releasetext = tag.i.text
						
						if releasetext.find('Added on') > -1:
							match = re.search(r'Added on (\w+ \d+, \d+)\.', releasetext)
							timestamp = time.mktime(time.strptime(match.group(1), '%B %d, %Y'))
							releasedate = date.fromtimestamp(timestamp)
						elif releasetext.find('Initially awarded as a prize during') > -1:
							# releasedate = 'Event Reward'
							releasedate = releasetext[7:]
						elif releasetext.find('Bundled with') > -1:
							# releasedate = 'Bundled Bonus'
							releasedate = releasetext[7:]
						elif releasetext.find('Exchanged') > -1:
							releasedate = releasetext[7:]
						elif releasetext.find('Added to Seal Shop on') > -1:
							match = re.search(r'Added to Seal Shop on (\w+ \d+, \d+)\W+', releasetext)
							timestamp = time.mktime(time.strptime(match.group(1), '%B %d, %Y'))
							releasedate = date.fromtimestamp(timestamp)
						elif releasetext.find('Awarded') > -1:
							releasedate = releasetext[7:]
						else:
							raise RuntimeError('Member parsing error: Cannot handle release date text "%s"' % releasetext)
						
						# print(releasedate)
						f.write('%s' % releasedate)