from django import template

from user.models import REGIONS, EMPLOYMENT_TYPE

register = template.Library()

@register.filter(name='region')
def region(value):
    if not isinstance(value, str):
        return value

    r = [item[1] for item in REGIONS if item[0] == value][0]
    return r or value

@register.filter(name='employment_type')
def employment_type(value):
    if not isinstance(value, str):
        return value

    r = [item[1] for item in EMPLOYMENT_TYPE if item[0] == value][0]
    return r or value