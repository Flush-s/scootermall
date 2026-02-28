from django import template

register = template.Library()


@register.filter
def intcomma(value):
    """Форматирует число с разделителями тысяч"""
    try:
        return "{:,}".format(int(value)).replace(",", " ")
    except (ValueError, TypeError):
        return value
