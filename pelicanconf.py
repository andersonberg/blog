#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

PROJECT_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

AUTHOR = 'Anderson Berg'
SITENAME = 'Anderson Berg'
SITEURL = ''
DEFAULT_OG_IMAGE = 'The og:image url'
FAVICON_URL = "The favicon url"

PATH = 'content'

TIMEZONE = 'America/Recife'
LOCALE = ["pt_BR"]
DEFAULT_LANG = 'pt-br'

DEFAULT_DATE_FORMAT = '%d %b, %Y'

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
RELATIVE_URLS = True

STATIC_PATHS = ['images']

DISPLAY_CATEGORIES_ON_MENU = False
DELETE_OUTPUT_DIRECTORY = False
PLUGIN_PATHS = [
    os.path.join(PROJECT_PATH, "pelican-plugins"),
    os.path.join(PROJECT_PATH, "extended_meta"),   
]
PLUGINS = [
    'assets',
    'representative_image',
    'liquid_tags.img',
    'liquid_tags.notebook',
    'pelican_alias',
    # 'extended_meta',
    'i18n_subsites'
]

NOTEBOOK_DIR = 'notebooks'

# EXTRA_HEADER = open('_nb_header.html').read().encode("utf-8").decode('utf-8')

THEME = "/home/anderson/code/yapeme"
# COLOR_SCHEME_CSS = 'monokai.css'

HEADER_COVER = 'images/code-python.jpg'

DISQUS_SITENAME = 'pythonize.org'
GOOGLE_ANALYTICS = 'UA-25538784-1'
TWITTER_USERNAME = 'berg_pe'

JINJA_ENVIRONMENT = {"extensions": ["jinja2.ext.i18n"]}
I18N_GETTEXT_NEWSTYLE = True
I18N_TEMPLATES_LANG = "pt_BR"