from django import template
import re

register = template.Library()


@register.filter
def replace_chars(value):
    return re.sub(r"[-,()]+", "-", re.sub(r"[ ,()]", "-", value))


@register.filter
def usd(value):
    try:
        value = float(value)
        return f"USD ${value:,.2f}"
    except (ValueError, TypeError):
        return value
