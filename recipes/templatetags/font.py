from django import template
from django.conf import settings
import random

register = template.Library()

@register.simple_tag
def random_font():
    font = random.choice(settings.SCRIPT_FONTS)
    return 'font-{}'.format(font)

@register.simple_tag
def choice(value):
    return random.choice(value)
