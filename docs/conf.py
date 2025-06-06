
project = 'Cool Docs Blog'
author = 'pfd'
release = '0.1'
extensions = ['myst_parser']
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}
html_theme = 'alabaster'
html_extra_path = ['_generated_feeds']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store', '.venv']