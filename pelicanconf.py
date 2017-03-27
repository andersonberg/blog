#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Anderson Berg'
SITENAME = 'Pythonize'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'America/Recife'

DEFAULT_LANG = 'pt'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

# Blogroll
LINKS = (('Pelican', 'http://getpelican.com/'),
         ('Python.org', 'http://python.org/'),)

# Social widget
SOCIAL = (('You can add links in your config file', '#'),
          ('Another social link', '#'),)

DEFAULT_PAGINATION = 10

# Uncomment following line if you want document-relative URLs when developing
# RELATIVE_URLS = True


STATIC_PATHS = ['images']
PLUGIN_PATH = ['/home/andersonberg/Projetos/pelican-plugins']
PLUGINS = ["representative_image"]


DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = False

PLUGIN_PATHS = ['/home/andersonberg/Projetos/pelican-plugins']
PLUGINS = [
    'assets',
    'global_license',
    'i18n_subsites',
    'liquid_tags.img',
    'summary',
]

THEME = "/home/andersonberg/Projetos/pelican-themes/clean-blog"
COLOR_SCHEME_CSS = 'monokai.css'


DISQUS_SITENAME = 'pythonize.org'
GOOGLE_ANALYTICS = 'UA-25538784-1'
TWITTER_USERNAME = 'berg_pe'
