# -*- coding: utf-8 -*-
import sys, os

extensions = ['sphinx.ext.autodoc', 'sphinx.ext.doctest', 'sphinx.ext.todo']
templates_path = ['_templates']
source_suffix = '.rst'
master_doc = 'index'
project = u'MPEG-1 Audio Python package'
copyright = u'2010, Jari Pennanen'
version = '0.5.4'
release = '0.5.4'
exclude_trees = ['_build']
pygments_style = 'sphinx'

# HTML ---------------------------------------

html_theme = 'default'
html_static_path = ['_static']
htmlhelp_basename = 'MPEG-1AudioPythonpackagedoc'

# LaTeX ---------------------------------------

latex_documents = [
  ('index', 'MPEG-1AudioPythonpackage.tex', u'MPEG-1 Audio Python package Documentation',
   u'Jari Pennanen', 'manual'),
]

# Autodoc ------------------------------------

autoclass_content = "both"
autodoc_member_order = "groupwise"

# Todo ------------------------------------

todo_include_todos = False
