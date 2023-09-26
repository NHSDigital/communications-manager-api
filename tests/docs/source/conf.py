project = 'Test Documentation'
copyright = '2023, NHSD'
author = 'NHSD'

extensions = [
	'myst_parser', 
	'sphinx_markdown_builder',
	'sphinx.ext.autodoc',
	'sphinx.ext.autosummary',
]

templates_path = ['_templates']
exclude_patterns = ['build/*', 'partials/*']

source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}
