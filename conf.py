import os
import sys
import sphinx_rtd_theme

project = 'PAUL'
author = 'PAUL DEV TEAM'
release = '1.0.0'

extenstions = [
  'sphinx.ext.autodoc'
  'sphinx.ext.viewcode'
  'sphinx_rtd_theme'
  ]
templates_path = ['_templates']
exclude_patterns = []
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

html_theme_options = {
  'collaspe_naviagion' : False,
  'display_version' : True,
  'logo_only' : True
}
autodoc_member_order = 'bysource'

sys.path.insert{0, os.path.abspath{'../'}}
