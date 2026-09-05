"""
Custom template filters for beneficiaries app
Includes currency formatting and other utility filters
"""
from django import template
from django.utils.safestring import mark_safe
import locale

register = template.Library()


@register.filter
def rupiah(value):
    """
    Format number as Indonesian Rupiah currency with dot separator
    Usage: {{ amount|rupiah }}
    Output: Rp 1.000.000
    """
    if value is None or value == '':
        return 'Rp 0'
    
    try:
        # Convert to float first
        float_value = float(value)
        
        # Try using Indonesian locale
        try:
            locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
            formatted = locale.currency(float_value, grouping=True, symbol=False)
            return f"Rp {formatted}"
        except locale.Error:
            # Fallback: Manual formatting for Indonesian Rupiah
            # Use comma then replace with dot
            formatted = f"{float_value:,.0f}".replace(',', '.')
            return f"Rp {formatted}"
    except (ValueError, TypeError):
        return 'Rp 0'


@register.filter
def rupiah_short(value):
    """
    Format number as Indonesian Rupiah with short notation (K, M, B)
    Usage: {{ amount|rupiah_short }}
    Output: Rp 1.5M, Rp 500K
    """
    if value is None or value == '':
        return 'Rp 0'
    
    try:
        float_value = float(value)
        
        if float_value >= 1_000_000_000:
            return f"Rp {float_value/1_000_000_000:.1f}B"
        elif float_value >= 1_000_000:
            return f"Rp {float_value/1_000_000:.1f}M"
        elif float_value >= 1_000:
            return f"Rp {float_value/1_000:.1f}K"
        else:
            return f"Rp {float_value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return 'Rp 0'


@register.filter
def format_number(value):
    """
    Format number with Indonesian thousand separator (dot)
    Usage: {{ number|format_number }}
    Output: 1.000.000
    """
    if value is None or value == '':
        return '0'
    
    try:
        float_value = float(value)
        return f"{float_value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return '0'


@register.filter
def percentage(value, decimals=1):
    """
    Format number as percentage
    Usage: {{ value|percentage }} or {{ value|percentage:2 }}
    Output: 85.5%
    """
    if value is None or value == '':
        return '0%'
    
    try:
        float_value = float(value)
        return f"{float_value:.{decimals}f}%"
    except (ValueError, TypeError):
        return '0%'


@register.filter
def economic_status_badge(value):
    """
    Generate badge HTML for economic status
    Usage: {{ beneficiary.economic_status|economic_status_badge }}
    """
    badge_classes = {
        'sangat_miskin': 'badge-danger',
        'miskin': 'badge-warning',
        'rentan_miskin': 'badge-info',
        'tidak_miskin': 'badge-success',
    }
    
    labels = {
        'sangat_miskin': 'Sangat Miskin',
        'miskin': 'Miskin',
        'rentan_miskin': 'Rentan Miskin',
        'tidak_miskin': 'Tidak Miskin',
    }
    
    badge_class = badge_classes.get(value, 'badge-secondary')
    label = labels.get(value, value)
    
    return mark_safe(f'<span class="badge {badge_class}">{label}</span>')


@register.filter
def status_badge(value):
    """
    Generate badge HTML for beneficiary status
    Usage: {{ beneficiary.status|status_badge }}
    """
    badge_classes = {
        'aktif': 'badge-success',
        'tidak_aktif': 'badge-danger',
        'lulus': 'badge-info',
        'meninggal': 'badge-dark',
        'pindah': 'badge-warning',
    }
    
    labels = {
        'aktif': 'Aktif',
        'tidak_aktif': 'Tidak Aktif',
        'lulus': 'Lulus',
        'meninggal': 'Meninggal',
        'pindah': 'Pindah',
    }
    
    badge_class = badge_classes.get(value, 'badge-secondary')
    label = labels.get(value, value)
    
    return mark_safe(f'<span class="badge {badge_class}">{label}</span>')


@register.filter
def aid_type_badge(value):
    """
    Generate badge HTML for aid type
    Usage: {{ aid.aid_type|aid_type_badge }}
    """
    badge_classes = {
        'uang': 'badge-success',
        'sembako': 'badge-warning',
        'kesehatan': 'badge-danger',
        'pendidikan': 'badge-info',
        'perumahan': 'badge-primary',
        'usaha': 'badge-dark',
        'lainnya': 'badge-secondary',
    }
    
    labels = {
        'uang': 'Bantuan Uang',
        'sembako': 'Sembako',
        'kesehatan': 'Kesehatan',
        'pendidikan': 'Pendidikan',
        'perumahan': 'Perumahan',
        'usaha': 'Bantuan Usaha',
        'lainnya': 'Lainnya',
    }
    
    badge_class = badge_classes.get(value, 'badge-secondary')
    label = labels.get(value, value)
    
    return mark_safe(f'<span class="badge {badge_class}">{label}</span>')

