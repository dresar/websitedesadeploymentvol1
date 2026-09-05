from django import template
import os
from decimal import Decimal

register = template.Library()

@register.filter
def basename(value):
    """
    Extract the basename (filename) from a file path
    """
    if not value:
        return ''
    return os.path.basename(str(value))

@register.filter
def rupiah(value):
    """
    Format number as Indonesian Rupiah currency
    """
    if not value:
        return 'Rp 0'
    
    try:
        # Convert to Decimal for proper formatting
        if isinstance(value, (int, float, str)):
            decimal_value = Decimal(str(value))
        else:
            decimal_value = value
            
        # Format with thousand separators
        formatted = f"{decimal_value:,.0f}".replace(',', '.')
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return 'Rp 0'

@register.filter
def rupiah_short(value):
    """
    Format number as Indonesian Rupiah currency with short notation (K, M, B)
    """
    if not value:
        return 'Rp 0'
    
    try:
        # Convert to Decimal for proper formatting
        if isinstance(value, (int, float, str)):
            decimal_value = Decimal(str(value))
        else:
            decimal_value = value
        
        # Convert to float for easier calculation
        num_value = float(decimal_value)
        
        if num_value >= 1_000_000_000:
            return f"Rp {num_value/1_000_000_000:.1f}B"
        elif num_value >= 1_000_000:
            return f"Rp {num_value/1_000_000:.1f}M"
        elif num_value >= 1_000:
            return f"Rp {num_value/1_000:.1f}K"
        else:
            return f"Rp {num_value:,.0f}".replace(',', '.')
    except (ValueError, TypeError):
        return 'Rp 0'

@register.filter
def format_harga(value):
    """
    Format harga dengan filter yang lebih fleksibel
    """
    if not value:
        return 'Gratis'
    
    try:
        # Convert to Decimal for proper formatting
        if isinstance(value, (int, float, str)):
            decimal_value = Decimal(str(value))
        else:
            decimal_value = value
            
        # Format with thousand separators
        formatted = f"{decimal_value:,.0f}".replace(',', '.')
        return f"Rp {formatted}"
    except (ValueError, TypeError):
        return 'Gratis'

@register.filter
def harga_range(min_harga, max_harga):
    """
    Format range harga dari min ke max
    """
    if not min_harga and not max_harga:
        return 'Gratis'
    
    if min_harga and max_harga:
        if min_harga == max_harga:
            return format_harga(min_harga)
        else:
            return f"{format_harga(min_harga)} - {format_harga(max_harga)}"
    elif min_harga:
        return f"Dari {format_harga(min_harga)}"
    elif max_harga:
        return f"Hingga {format_harga(max_harga)}"
    else:
        return 'Gratis'