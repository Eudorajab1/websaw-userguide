from datetime import datetime

extensions = []
templates_path = ["_templates"]
source_suffix = ".rst"
master_doc = "index"

project = u"WebSaw"
year = datetime.now().year
copyright = u"%d WebSaw" % year

exclude_patterns = ["_build"]

html_theme = "alabaster"
html_static_path = ['_static']


html_sidebars = {
    "**": [
        "about.html",
        "navigation.html",
        "relations.html",
        "searchbox.html",
        "donate.html",
    ]
}
html_theme_options = {
    "logo": "websaw-logos_transparent.png",
    "description": "A light, fully fucntional, ultra fast, flexible and feauture rich web framework",
    "github_user": "Eudorajab1",
    "fixed_sidebar": True,
    "show_powered_by": False,
    "tidelift_url": "https://tidelift.com/subscription/pkg/pypi-alabaster?utm_source=pypi-alabaster&utm_medium=referral&utm_campaign=docs",  # noqa
}
