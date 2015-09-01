"""
tracks context processors

tracks depends on a number of assets to function.  These include:

    extjs 4.2
    wireit + yui
    jquery
    jqplot
    jqplot.science

Most of these assets are available via CDN, and these are set as the
default.  Others, such as jqplot.science, are hosted in a git repository
whose path will need to be configured in settings.py.

To add tracks to your site, you will need to extend the django setting
*TEMPLATE_CONTEXT_PROCESSORS* with tracks.context_processors.assets.
For example::

    from django.conf import global_settings
    TEMPLATE_CONTEXT_PROCESSORS = global_settings.TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += ('tracks.context_processors.assets',)

Settings
========

All settings will be run through the django template processor in the
context of '{% load "staticfiles" %}', so you can use '{% static ... %}'
in your definitions.  The default value for variable *TRACKS_ZZZ* is
given in *tracks.context_processors.DEFAULT_ZZZ* for each variable *ZZZ*.

*TRACKS_EXTJS*

    This is a the html required to include ext-all.js and the associated
    ext-all.css.  The default is tracks.context_processors.EXTJS_CDN.

*TRACKS_JQUERY*

    this is the link to jquery.  The default is to use jquery from
    django admin.
"""
from django.conf import settings

DEFAULT_EXTJS = """
<link href="http://cdn.sencha.com/ext/gpl/4.2.0/resources/css/ext-all.css" rel="stylesheet" />
<script src="http://cdn.sencha.com/ext/gpl/4.2.0/ext-all.js"></script>
"""

DEFAULT_JQUERY = """
{% static admin/js/jquery.min.js %}
"""

def _defaults(**kw):
    return { k: getattr(settings,k,v) for k,v in kw.items() }

def assets(request):
    return _defaults(
        TRACKS_EXTJS=DEFAULT_EXTJS,
        TRACKS_JQUERY=DEFAULT_JQUERY,
        )

