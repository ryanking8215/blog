#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'RyanKing'
SITENAME = "RyanKing"
#SITEURL = 'http://ryanking8215.github.io'
#SITEURL = ''

PATH = 'content'

#TIMEZONE = 'Europe/Paris'
TIMEZONE = 'Asia/Shanghai'

DEFAULT_LANG = 'zh'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# my setup
#DELETE_OUTPUT_DIRECTORY = False
DEFAULT_DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
SLUGIFY_SOURCE = 'title'
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2}).*'
OUTPUT_RETENTION = ['.git','.gitignore']

# Blogroll
LINKS = (('V2EX', 'http://www.v2ex.com/member/ryanking8215'),)

# Social widget
SOCIAL = (('github', 'https://github.com/ryanking8215'),)

DEFAULT_PAGINATION = 10

MAIN_MENU = True
MENUITEMS = (('ARCHIVES', '/archives.html'), ('Categories', '/categories.html'), ('TAG', '/tags.html'), )
SITETITLE = SITENAME
SITESUBTITLE = "嵌入式/python开发工程师"

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

THEME = 'theme/Flex'
