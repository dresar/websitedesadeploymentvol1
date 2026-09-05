#!/usr/bin/env python
"""
Production Server Runner untuk Website Desa Pulosarok
Mode: Production dengan HTTP (tanpa auto HTTPS redirect)
"""

import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_production_environment():
    """
    Setup environment untuk production mode
    """
    # Set environment variables untuk production
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
    os.environ.setdefault('DEBUG', 'False')
    os.environ.setdefault('ENVIRONMENT', 'production')
    
    # Setup Django
    django.setup()
    
    print("🚀 Production Environment Setup Complete!")
    print("🔒 Security Mode: HIGH")
    print("🌐 HTTP Mode: ENABLED (no auto HTTPS redirect)")
    print("📊 Error Pages: CUSTOM")
    print("🛡️ Security Headers: ENABLED")
    print("📝 Logging: ENABLED")
    print("=" * 50)

def run_production_server():
    """
    Run Django server dalam production mode
    """
    setup_production_environment()
    
    # Run server dengan production settings
    execute_from_command_line(['manage.py', 'runserver', '0.0.0.0:8000'])

def run_with_gunicorn():
    """
    Run dengan Gunicorn (untuk production deployment)
    """
    setup_production_environment()
    
    # Install gunicorn jika belum ada
    try:
        import gunicorn
    except ImportError:
        print("Installing Gunicorn...")
        os.system("pip install gunicorn")
    
    # Run dengan Gunicorn
    os.system("gunicorn --bind 0.0.0.0:8000 --workers 4 --timeout 120 pulosarok_website.wsgi:application")

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'gunicorn':
        run_with_gunicorn()
    else:
        run_production_server()
