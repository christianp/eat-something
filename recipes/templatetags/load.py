from django import template
from django.utils.html import format_html
from django.contrib.staticfiles.templatetags.staticfiles import static

register = template.Library()

@register.simple_tag()
def css(name):
    return format_html('<link rel="stylesheet" type="text/css" href="{}"/>',static('css/'+name+'.css'))

@register.simple_tag()
def js(name):
    return format_html('<script language="javascript" src="{}"></script>',static('js/'+name+'.js'))
