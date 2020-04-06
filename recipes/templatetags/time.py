from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

def pluralise(n):
    return 's' if n!=1 else ''

@register.filter
def timedelta(t):
    bits = []

    hours, remainder = divmod(t.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)

    if hours:
        bits.append('{} hour{}'.format(hours,pluralise(hours)))
    if minutes:
        bits.append('{} minute{}'.format(minutes,pluralise(minutes)))
    if seconds:
        bits.append('{} second{}'.format(seconds,pluralise(seconds)))

    s = ', '.join(bits[:-1])
    if len(s)>1:
        s = '{} and {}'.format(s,bits[-1])
    else:
        s = bits[0] if len(bits)>0 else ''
    return s
