# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Virtool Dev"
copyright = "2024, Ian Boyes, Reece Hoffmann"
author = "Ian Boyes, Reece Hoffmann"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.intersphinx",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "piccolo_theme"
# html_static_path = ['_static']


# -- Options for intersphinx extension ---------------------------------------

intersphinx_mapping = {
    "virtool": (
        "https://dev.virtool.ca/projects/virtool/en/latest/",
        None,
    ),
    "core": ("https://dev.virtool.ca/projects/virtool-core/en/latest/", None),
    "workflow": (
        "https://dev.virtool.ca/projects/virtool-workflow/en/latest/",
        None,
    ),
}
# https://www.sphinx-doc.org/en/master/usage/extensions/intersphinx.html#confval-intersphinx_disabled_reftypes
# intersphinx_disabled_reftypes = ["*"]
