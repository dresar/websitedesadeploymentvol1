from django import template
from django.utils.safestring import mark_safe
from django.utils.html import strip_tags
import re

register = template.Library()

@register.filter
def summonote_content(content, is_summonote=False):
    """
    Filter untuk menangani konten Summonote dengan styling khusus
    """
    if not content:
        return ""
    
    if is_summonote:
        # Untuk Summonote, tambahkan wrapper dengan styling khusus
        summonote_wrapper = f'''
        <div class="summonote-content-wrapper" style="
            border-left: 4px solid #F97316;
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.05), rgba(251, 146, 60, 0.05));
            padding: 1.5rem;
            border-radius: 0 8px 8px 0;
            margin: 1rem 0;
        ">
            <div class="summonote-header" style="
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
            ">
                <i class="fas fa-sticky-note" style="color: #F97316; font-size: 1.5rem; margin-right: 0.75rem;"></i>
                <h2 style="color: #1f2937; font-size: 1.25rem; font-weight: 600; margin: 0;">Summonote</h2>
            </div>
            <div class="summonote-body">
                {content}
            </div>
        </div>
        '''
        return mark_safe(summonote_wrapper)
    else:
        # Untuk konten biasa, return as-is
        return mark_safe(content)

@register.filter
def summonote_excerpt(content, is_summonote=False):
    """
    Filter untuk membuat excerpt dari konten Summonote
    """
    if not content:
        return ""
    
    # Strip HTML tags untuk excerpt
    clean_content = strip_tags(content)
    word_count = 15  # Default word count
    
    if is_summonote:
        # Untuk Summonote, tambahkan prefix
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        
        summonote_excerpt = f'''
        <div class="summonote-excerpt" style="
            border-left: 3px solid #F97316;
            background: rgba(249, 115, 22, 0.05);
            padding: 0.75rem 1rem;
            border-radius: 0 4px 4px 0;
            margin: 0.5rem 0;
        ">
            <span style="color: #F97316; font-weight: 600; font-size: 0.875rem;">
                <i class="fas fa-sticky-note" style="margin-right: 0.25rem;"></i>Summonote:
            </span>
            <span style="color: #374151; margin-left: 0.5rem;">{excerpt}</span>
        </div>
        '''
        return mark_safe(summonote_excerpt)
    else:
        # Untuk konten biasa, return excerpt biasa
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        return excerpt

@register.filter
def summonote_excerpt_20(content, is_summonote=False):
    """
    Filter untuk membuat excerpt dari konten Summonote dengan 20 kata
    """
    if not content:
        return ""
    
    # Strip HTML tags untuk excerpt
    clean_content = strip_tags(content)
    word_count = 20
    
    if is_summonote:
        # Untuk Summonote, tambahkan prefix
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        
        summonote_excerpt = f'''
        <div class="summonote-excerpt" style="
            border-left: 3px solid #F97316;
            background: rgba(249, 115, 22, 0.05);
            padding: 0.75rem 1rem;
            border-radius: 0 4px 4px 0;
            margin: 0.5rem 0;
        ">
            <span style="color: #F97316; font-weight: 600; font-size: 0.875rem;">
                <i class="fas fa-sticky-note" style="margin-right: 0.25rem;"></i>Summonote:
            </span>
            <span style="color: #374151; margin-left: 0.5rem;">{excerpt}</span>
        </div>
        '''
        return mark_safe(summonote_excerpt)
    else:
        # Untuk konten biasa, return excerpt biasa
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        return excerpt

@register.filter
def summonote_badge(is_summonote=False):
    """
    Filter untuk menampilkan badge Summonote
    """
    if is_summonote:
        badge = '''
        <span class="summonote-badge" style="
            display: inline-flex;
            align-items: center;
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            background: linear-gradient(135deg, #F97316, #FB923C);
            color: white;
            margin-left: 0.5rem;
        ">
            <i class="fas fa-sticky-note" style="margin-right: 0.25rem;"></i>Summonote
        </span>
        '''
        return mark_safe(badge)
    return ""

@register.filter
def summonote_card_class(is_summonote=False):
    """
    Filter untuk menambahkan class CSS untuk card Summonote
    """
    if is_summonote:
        return "summonote-card"
    return ""

@register.filter
def summonote_meta_description(content, is_summonote=False):
    """
    Filter untuk meta description yang mendukung Summonote
    """
    if not content:
        return ""
    
    # Strip HTML tags untuk meta description
    clean_content = strip_tags(content)
    word_count = 20
    
    if is_summonote:
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        return f"[Summonote] {excerpt}"
    else:
        words = clean_content.split()[:word_count]
        excerpt = " ".join(words)
        if len(clean_content.split()) > word_count:
            excerpt += "..."
        return excerpt

@register.filter
def summonote_title(title, is_summonote=False):
    """
    Filter untuk menambahkan prefix Summonote pada judul
    """
    if is_summonote:
        return f"📌 {title}"
    return title

@register.filter
def summonote_icon(is_summonote=False):
    """
    Filter untuk menampilkan icon Summonote
    """
    if is_summonote:
        return mark_safe('<i class="fas fa-sticky-note" style="color: #F97316;"></i>')
    return ""

@register.filter
def summonote_priority(is_summonote=False):
    """
    Filter untuk menentukan prioritas Summonote
    """
    if is_summonote:
        return "high"
    return "normal"

@register.filter
def summonote_color(is_summonote=False):
    """
    Filter untuk mendapatkan warna Summonote
    """
    if is_summonote:
        return "#F97316"
    return "#3B82F6"

@register.filter
def summonote_border_style(is_summonote=False):
    """
    Filter untuk mendapatkan border style Summonote
    """
    if is_summonote:
        return "border-left: 4px solid #F97316;"
    return ""

@register.filter
def summonote_background_style(is_summonote=False):
    """
    Filter untuk mendapatkan background style Summonote
    """
    if is_summonote:
        return "background: linear-gradient(135deg, rgba(249, 115, 22, 0.05), rgba(251, 146, 60, 0.05));"
    return ""

@register.filter
def summonote_excerpt_form(excerpt, is_summonote=False):
    """
    Filter untuk menampilkan excerpt dengan styling Summonote di form
    """
    if not excerpt:
        return ""
    
    if is_summonote:
        # Untuk Summonote, tambahkan styling khusus
        summonote_excerpt = f'''
        <div class="summonote-excerpt-form" style="
            border-left: 3px solid #F97316;
            background: rgba(249, 115, 22, 0.05);
            padding: 0.75rem 1rem;
            border-radius: 0 4px 4px 0;
            margin: 0.5rem 0;
            font-style: italic;
        ">
            <span style="color: #F97316; font-weight: 600; font-size: 0.875rem;">
                <i class="fas fa-sticky-note" style="margin-right: 0.25rem;"></i>
            </span>
            <span style="color: #374151; margin-left: 0.5rem;">{excerpt}</span>
        </div>
        '''
        return mark_safe(summonote_excerpt)
    else:
        # Untuk excerpt biasa, return as-is
        return excerpt

@register.filter
def summonote_excerpt_preview(excerpt, is_summonote=False):
    """
    Filter untuk preview excerpt dengan styling Summonote
    """
    if not excerpt:
        return ""
    
    if is_summonote:
        # Untuk Summonote, tambahkan styling khusus untuk preview
        summonote_preview = f'''
        <div class="summonote-excerpt-preview" style="
            border-left: 3px solid #F97316;
            background: linear-gradient(135deg, rgba(249, 115, 22, 0.1), rgba(251, 146, 60, 0.1));
            padding: 1rem 1.25rem;
            border-radius: 0 6px 6px 0;
            margin: 1rem 0;
            box-shadow: 0 2px 4px rgba(249, 115, 22, 0.1);
        ">
            <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                <i class="fas fa-sticky-note" style="color: #F97316; font-size: 1.125rem; margin-right: 0.5rem;"></i>
            </div>
            <p style="color: #374151; margin: 0; line-height: 1.6; font-style: italic;">{excerpt}</p>
        </div>
        '''
        return mark_safe(summonote_preview)
    else:
        # Untuk excerpt biasa, return dengan styling biasa
        return f'<p style="color: #6b7280; font-style: italic; margin: 1rem 0;">{excerpt}</p>'
