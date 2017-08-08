#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals
import os

AUTHOR = 'Anderson Berg'
SITENAME = 'Pythonize'
SITESUBTITLE = u'Python, Django e desenvolvimento Web'
SITEURL = os.environ.get('SITEURL', 'http://localhost:8000')
SITEDESCRIPTION = u'Artigos sobre desenvolvimento Web, Python e Django.'

PATH = 'content'

TIMEZONE = 'America/Recife'

DEFAULT_LANG = u'pt_BR.utf8'

DEFAULT_DATE_FORMAT = '%d %b, %Y'
I18N_TEMPLATES_LANG = u'EN'
LOCALE = ['pt_BR.utf8']

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
WEBASSETS = True

PLUGIN_PATHS = ['/home/anderson/Projetos/pelican-plugins', './plugins']
PLUGINS = [
    'assets',
    'extended_meta',
    'representative_image',
    'i18n_subsites',
    'liquid_tags.img',
    'liquid_tags.notebook',
    'pelican_alias',
    'ipynb.liquid'
]

NOTEBOOK_DIR = 'notebooks'
JINJA_EXTENSIONS = ['jinja2.ext.i18n',]
I18N_GETTEXT_NEWSTYLE = True
I18N_UNTRANSLATED_PAGES = 'keep'
I18N_SUBSITES = {}

EXTRA_HEADER = open('_nb_header.html').read().encode("utf-8").decode('utf-8')

THEME = "/home/anderson/Projetos/pelican-themes/yapeme"
COLOR_SCHEME_CSS = 'monokai.css'

HEADER_COVER = 'images/code-python.jpg'
TAG_URL = "tag/{slug}.html"

DISQUS_SITENAME = 'pythonize.org'
GOOGLE_ANALYTICS = 'UA-25538784-1'
TWITTER_USERNAME = 'berg_pe'
