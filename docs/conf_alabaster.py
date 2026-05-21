# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

import os
import sys

# -- Project information -----------------------------------------------------

project = 'BlackPill'
copyright = '2026, Gerhard Burger'
author = 'Gerhard Burger'
release = '1.0.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
]

templates_path = ['_templates']
language = 'en'

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

html_theme = 'alabaster'

# Combined Theme Options to prevent overwriting
html_theme_options = {
    # Pfad ausgehend vom source-Ordner
    'logo': 'common/nav_logo.png', 
    
    'logo_name': False,          # WICHTIG: Schaltet den Text-Titel aus
    'description': '',           # WICHTIG: Schaltet den Text-Untertitel aus
    
    'fixed_sidebar': True,
    'sidebar_width': '300px',
    'logo_text_align': 'left',
}

# Sidebar elements order: 
# 1. Project Title & Description (via about.html) 
# 2. Navigation 
# 3. Searchbox
html_sidebars = {
    '**': [
        'about.html',           # Das Logo und die Beschreibung
        'navigation.html',      # Das Menü (Introduction, etc.)
        'searchbox.html',       # Die Suche
    ]
}

# Path for static files (where custom.css lives)
html_static_path = ['_static', 'images']

# -- Custom Setup Function ---------------------------------------------------

def setup(app):
    # Connects custom CSS for the clean "Molex-Style" look
    # Note: Ensure custom.css exists in source/_static/
    app.add_css_file('custom.css')

# -- Extension configuration -------------------------------------------------

todo_include_todos = True