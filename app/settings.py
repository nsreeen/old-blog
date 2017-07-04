# -*- coding: utf-8 -*-

import os

def parent_dir(path):
    '''Return the parent of a directory.'''
    return os.path.abspath(os.path.join(path, os.pardir))

REPO_NAME = "" #"nasreen123.github.io"  # Used for FREEZER_BASE_URL

DEBUG = True

# Assumes the app is in the same directory
APP_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = parent_dir(APP_DIR)

# Put static files in project root (to deploy to github pages)
FREEZER_DESTINATION = PROJECT_ROOT

FREEZER_BASE_URL = "http://localhost/{0}".format(REPO_NAME)

# If True md files will be removed
FREEZER_REMOVE_EXTRA_FILES = False
  
FLATPAGES_MARKDOWN_EXTENSIONS = ['codehilite']

#FLATPAGES_ROOT = os.path.join(APP_DIR, 'pages')

FLATPAGES_EXTENSION = '.md'
