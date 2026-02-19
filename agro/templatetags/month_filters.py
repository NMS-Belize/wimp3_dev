from django import template
import calendar

register = template.Library()

@register.filter
def month_abbr(value):
    try:
        return calendar.month_abbr[int(value)].upper()
    except:
        return ""