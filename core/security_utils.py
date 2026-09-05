"""
Security utilities for password validation and security checks
"""
import re
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_password_strength(password, settings):
    """
    Validate password strength based on security settings
    """
    errors = []
    
    # Check minimum length
    if len(password) < settings.min_password_length:
        errors.append(_(f'Password must be at least {settings.min_password_length} characters long.'))
    
    # Check uppercase requirement
    if settings.require_uppercase and not re.search(r'[A-Z]', password):
        errors.append(_('Password must contain at least one uppercase letter.'))
    
    # Check lowercase requirement
    if settings.require_lowercase and not re.search(r'[a-z]', password):
        errors.append(_('Password must contain at least one lowercase letter.'))
    
    # Check numbers requirement
    if settings.require_numbers and not re.search(r'\d', password):
        errors.append(_('Password must contain at least one number.'))
    
    # Check symbols requirement
    if settings.require_symbols and not re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        errors.append(_('Password must contain at least one symbol.'))
    
    return errors


def get_password_strength_score(password, settings):
    """
    Calculate password strength score (0-100)
    """
    score = 0
    
    # Length score (max 30 points)
    length_score = min(30, len(password) * 2)
    score += length_score
    
    # Character variety score (max 40 points)
    variety_score = 0
    if re.search(r'[a-z]', password):
        variety_score += 10
    if re.search(r'[A-Z]', password):
        variety_score += 10
    if re.search(r'\d', password):
        variety_score += 10
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        variety_score += 10
    score += variety_score
    
    # Complexity score (max 30 points)
    complexity_score = 0
    if len(set(password)) > len(password) * 0.5:  # No repeated characters
        complexity_score += 15
    if not re.search(r'(.)\1{2,}', password):  # No 3+ consecutive same characters
        complexity_score += 15
    score += complexity_score
    
    return min(100, score)


def get_security_recommendations(settings):
    """
    Get security recommendations based on current settings
    """
    recommendations = []
    
    if not settings.enable_ssl_redirect:
        recommendations.append("Enable SSL redirect for better security")
    
    if not settings.enable_hsts:
        recommendations.append("Enable HSTS to prevent protocol downgrade attacks")
    
    if not settings.enable_2fa:
        recommendations.append("Enable Two-Factor Authentication for enhanced security")
    
    if not settings.enable_captcha:
        recommendations.append("Enable CAPTCHA to prevent automated attacks")
    
    if settings.min_password_length < 12:
        recommendations.append("Increase minimum password length to 12 characters")
    
    if not settings.require_symbols:
        recommendations.append("Require symbols in passwords for better security")
    
    if settings.password_expiry > 90:
        recommendations.append("Consider reducing password expiry to 90 days or less")
    
    if settings.security_level == 'low':
        recommendations.append("Consider upgrading to medium or high security level")
    
    return recommendations


def check_login_attempts(user, request):
    """
    Check if user has exceeded maximum login attempts
    """
    # TODO: Implement login attempt tracking
    # This would require a model to track failed login attempts
    return True


def get_security_score(settings):
    """
    Calculate overall security score based on settings
    """
    score = 0
    
    # SSL Settings (25 points)
    if settings.enable_ssl_redirect:
        score += 15
    if settings.enable_hsts:
        score += 10
    
    # Authentication Settings (35 points)
    if settings.enable_2fa:
        score += 20
    if settings.enable_captcha:
        score += 10
    if settings.max_login_attempts <= 5:
        score += 5
    
    # Password Policy (40 points)
    if settings.min_password_length >= 8:
        score += 10
    if settings.require_uppercase and settings.require_lowercase:
        score += 10
    if settings.require_numbers:
        score += 10
    if settings.require_symbols:
        score += 10
    
    return min(100, score)