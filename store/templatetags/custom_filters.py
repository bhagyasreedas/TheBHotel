
from django import template

register = template.Library()

@register.filter
def add_range(value):
    return range(value)