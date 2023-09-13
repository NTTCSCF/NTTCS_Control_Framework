from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='resta')
def resta(a, b):
    a = datetime(b.year, b.month, b.day, a.hour, a.minute).astimezone()
    b = b.astimezone()
    return a-b
