#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'RyanKing'
SITENAME = "RyanKing's Blog"
#SITEURL = 'http://ryanking8215.github.io'
SITEURL = ''

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
SLUGIFY_SOURCE = 'basename'
FILENAME_METADATA = '(?P<date>\d{4}-\d{2}-\d{2}).*'
OUTPUT_RETENTION = ['.git','.gitignore']

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),
         ('Jinja2', 'http://jinja.pocoo.org/'),
         ('You can modify those links in your config file', '#'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

#THEME = 'pelican-themes/pelican-bootstrap3'
THEME = 'pelican-themes/simple-bootstrap'
#THEME = 'pelican-themes/plumage'
