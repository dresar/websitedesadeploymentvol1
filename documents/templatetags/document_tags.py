from django import template

register = template.Library()


@register.filter(name='split')
def split(value, arg):
    """
    Split string by separator
    Usage: {{ value|split:"," }}
    """
    if value:
        return [item.strip() for item in value.split(arg)]
    return []


@register.filter(name='file_icon')
def file_icon(extension):
    """
    Return appropriate icon class for file extension
    """
    icons = {
        'pdf': 'fa-file-pdf text-danger',
        'doc': 'fa-file-word text-primary',
        'docx': 'fa-file-word text-primary',
        'xls': 'fa-file-excel text-success',
        'xlsx': 'fa-file-excel text-success',
        'zip': 'fa-file-archive text-warning',
        'rar': 'fa-file-archive text-warning',
    }
    return icons.get(extension.lower(), 'fa-file text-secondary')


@register.filter(name='file_badge')
def file_badge(extension):
    """
    Return Bootstrap badge class for file extension
    """
    badges = {
        'pdf': 'bg-danger',
        'doc': 'bg-primary',
        'docx': 'bg-primary',
        'xls': 'bg-success',
        'xlsx': 'bg-success',
        'zip': 'bg-warning',
        'rar': 'bg-warning',
    }
    return badges.get(extension.lower(), 'bg-secondary')

