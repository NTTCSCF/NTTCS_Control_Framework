from django import template
from datetime import datetime

register = template.Library()


@register.filter(name='resta')
def resta(a, b):
    a = datetime.fromisoformat(b.isoformat().split("T")[0]+"T"+str(a))
    b = b.replace(tzinfo=None)
    return a-b
