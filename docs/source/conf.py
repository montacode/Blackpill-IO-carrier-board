import os
import sys
# 1. Pfad zur Library hinzufügen
# Da deine Datei in source/examples/dro_hal/zDROHal.py liegt
# und die conf.py meist in source/ liegt:
sys.path.insert(0, os.path.abspath('examples/dro_hal'))
# In der conf.py hinzufügen:
autodoc_mock_imports = ["serial"]
# -- Project information -----------------------------------------------------

project = 'BlackPill'
copyright = '2026, Gerhard Burger'
author = 'Gerhard Burger'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',    # Unterstützt schönere Docstrings
    'sphinx.ext.viewcode',   # Optional: Fügt Links zum Quellcode hinzu
    'sphinx.ext.todo',
    'sphinx.ext.githubpages',
    'sphinx_rtd_theme',
]
numfig = True

# Definiert den Text vor der Nummer
numfig_format = {
    'figure': 'Figure %s: ',  # Hier kannst du 'Figure', 'Abbildung' oder 'Bild' eintragen
    'table': 'Table %s: ',
    'code-block': 'Listing %s: ',
}

templates_path = ['_templates']
language = 'en'



# Dateien und Ordner, die ignoriert werden
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# -- Options for HTML output -------------------------------------------------

# -- Options for HTML output -------------------------------------------------

html_theme = 'sphinx_rtd_theme'

# WICHTIG: Pfad relativ zu deinem _static Ordner!
html_logo = "images/common/nav_logo.png" 

html_theme_options = {
    'logo_only': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    
    # Navigation: Das sorgt für die dauerhafte Einrückung
    'collapse_navigation': False, 
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False
}

# RTD nutzt ein eigenes Sidebar-System. 
# Die html_sidebars von Alabaster werden hier nicht mehr benötigt.

# Pfad für statische Dateien (custom.css)
html_static_path = ['_static', 'images']

# -- Custom Setup Function ---------------------------------------------------

def setup(app):
    # Bindet deine custom.css ein, falls du Farben anpassen willst
    app.add_css_file('standard.css')

# -- Extension configuration -------------------------------------------------

todo_include_todos = True