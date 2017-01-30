__author__ = 'maykel'
from django import template
import os

register = template.Library()


@register.filter(name='get_last')
def get_last(value):
    fname = os.path.basename(value.url)
    return fname
