#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = 'Νέος Μπαμπάς'
SITENAME = 'Έγινα μπαμπάς! Και τώρα τι;'
SITEURL = ''

PATH = 'content'

TIMEZONE = 'Europe/Athens'

DEFAULT_LANG = 'el'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None

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

# hargikas -- manual change
# Setting up the locale
LOCALE = ('el',     # On Windows
           'el_GR'  # On Unix/Linux
)


# several typographical improvements will be incorporated into the generated HTML
TYPOGRIFY = True

# Static Content
STATIC_PATHS = ['images', 'extra']

EXTRA_PATH_METADATA = {
    'extra/favicon.ico': {'path': 'favicon.ico'},
}
