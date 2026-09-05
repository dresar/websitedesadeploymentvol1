from django import template
import json

register = template.Library()

@register.filter
def json_to_list(value):
    """Convert JSON string to Python list"""
    if not value or value == '[]':
        return []
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return []

@register.filter
def json_to_dict(value):
    """Convert JSON string to Python dictionary"""
    if not value or value == '{}':
        return {}
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return {}
