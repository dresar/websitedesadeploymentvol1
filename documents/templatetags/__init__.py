from django import template

register = template.Library()

@register.filter
def split_tags(value, delimiter=','):
    """Split a string by delimiter and return a list"""
    if not value:
        return []
    return [tag.strip() for tag in str(value).split(delimiter) if tag.strip()]

@register.filter
def file_extension(value):
    """Get file extension from filename"""
    if not value:
        return 'default'
    return str(value).split('.')[-1].lower() if '.' in str(value) else 'default'