#!/usr/bin/env python
"""
Script untuk menjalankan Django development server dengan pengaturan khusus
untuk localhost tanpa HTTPS menggunakan Virtual Environment
"""

import os
import sys
import django
import shutil
import subprocess
from pathlib import Path
from django.core.management import execute_from_command_line
from django.conf import settings

def check_and_activate_venv():
    """
    Check apakah venv ada dan activate jika belum aktif
    Returns: True jika berhasil, False jika gagal
    """
    # Skip venv check jika sudah dijalankan dari venv
    if os.environ.get('VENV_ALREADY_ACTIVATED'):
        print("OK: Virtual Environment sudah aktif (skip check)")
        return True
        
    print("Memeriksa Virtual Environment...")
    
    # Get base directory
    base_dir = Path(__file__).resolve().parent
    venv_dir = base_dir / 'venv'
    
    # Check if venv exists
    if not venv_dir.exists():
        print("\n" + "=" * 60)
        print("ERROR: Virtual Environment tidak ditemukan!")
        print("=" * 60)
        print("\nSilakan buat virtual environment terlebih dahulu:")
        print("\n1. Buat venv:")
        print("   python -m venv venv")
        print("\n2. Activate venv:")
        print("   Windows: venv\\Scripts\\activate")
        print("   Linux/Mac: source venv/bin/activate")
        print("\n3. Install dependencies:")
        print("   pip install -r requirements.txt")
        print("\n4. Jalankan script ini lagi")
        print("=" * 60)
        return False
    
    # Check if already in venv
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print("OK: Virtual Environment sudah aktif")
        print(f"   Python: {sys.executable}")
        print(f"   Version: {sys.version.split()[0]}")
        return True
    
    # Not in venv, need to activate
    print("WARNING: Virtual Environment belum aktif")
    print("Mengaktifkan Virtual Environment...")
    
    # Determine activate script path based on OS
    if os.name == 'nt':  # Windows
        activate_script = venv_dir / 'Scripts' / 'python.exe'
    else:  # Linux/Mac
        activate_script = venv_dir / 'bin' / 'python'
    
    if not activate_script.exists():
        print(f"ERROR: Python executable tidak ditemukan di venv!")
        print(f"   Expected: {activate_script}")
        return False
    
    # Re-run this script using venv Python
    print(f"Menjalankan ulang script menggunakan venv Python...")
    print(f"   {activate_script}")
    
    try:
        # Set environment variable to prevent double execution
        env = os.environ.copy()
        env['VENV_ALREADY_ACTIVATED'] = 'True'
        
        # Run this script again but with venv Python
        result = subprocess.run(
            [str(activate_script), __file__] + sys.argv[1:],
            cwd=str(base_dir),
            env=env
        )
        sys.exit(result.returncode)
    except Exception as e:
        print(f"ERROR saat menjalankan venv Python: {e}")
        return False

def clear_all_caches():
    """Hapus semua cache Django dan Python"""
    print("Membersihkan semua cache...")
    
    # Hapus __pycache__ directories
    cache_dirs = [
        '__pycache__',
        'core/__pycache__',
        'pulosarok_website/__pycache__',
        'admin_panel/__pycache__',
        'beneficiaries/__pycache__',
        'business/__pycache__',
        'complaints/__pycache__',
        'documents/__pycache__',
        'layanan/__pycache__',
        'letters/__pycache__',
        'news/__pycache__',
        'organization/__pycache__',
        'posyandu/__pycache__',
        'references/__pycache__',
        'tourism/__pycache__',
        'village_profile/__pycache__',
    ]
    
    for cache_dir in cache_dirs:
        if os.path.exists(cache_dir):
            try:
                shutil.rmtree(cache_dir)
                print(f"Dihapus: {cache_dir}")
            except Exception as e:
                print(f"Gagal hapus {cache_dir}: {e}")
    
    # Hapus .pyc files
    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.pyc'):
                try:
                    os.remove(os.path.join(root, file))
                    print(f"Dihapus: {os.path.join(root, file)}")
                except Exception as e:
                    print(f"Gagal hapus {file}: {e}")
    
    # Hapus cache Django
    try:
        from django.core.cache import cache
        cache.clear()
        print("Django cache cleared")
    except:
        pass
    
    print("Cache cleaning selesai!")

def clear_chrome_cache():
    """Instruksi untuk menghapus cache Chrome"""
    print("\nINSTRUKSI MENGHAPUS CACHE CHROME:")
    print("=" * 50)
    print("1. Buka Chrome")
    print("2. Tekan Ctrl + Shift + Delete")
    print("3. Pilih 'All time' untuk Time range")
    print("4. Centang semua opsi:")
    print("   - Browsing history")
    print("   - Cookies and other site data")
    print("   - Cached images and files")
    print("5. Klik 'Clear data'")
    print("6. Atau gunakan mode incognito: Ctrl + Shift + N")
    print("=" * 50)

def show_file_monitoring_info():
    """Tampilkan informasi monitoring file"""
    print("\nMONITORING FILE DEVELOPMENT:")
    print("=" * 50)
    print("Django akan memonitor perubahan pada file berikut:")
    print("\nBackend Files:")
    print("   - models.py - Perubahan model database")
    print("   - views.py - Perubahan logic aplikasi") 
    print("   - forms.py - Perubahan form validation")
    print("   - urls.py - Perubahan routing URL")
    print("   - admin.py - Perubahan admin interface")
    print("   - serializers.py - Perubahan API serializers")
    
    print("\nFrontend Files:")
    print("   - *.html - Template changes")
    print("   - *.css - Stylesheet changes")
    print("   - *.js - JavaScript changes")
    print("   - static/ - Static files")
    
    print("\nConfiguration Files:")
    print("   - settings.py - Django settings")
    print("   - requirements.txt - Dependencies")
    print("   - manage.py - Management commands")
    
    print("\nAuto-reload akan terjadi ketika:")
    print("   [OK] File Python (*.py) diubah dan disimpan")
    print("   [OK] Template HTML diubah dan disimpan")
    print("   [OK] Static files diubah dan disimpan")
    print("   [OK] Settings diubah dan disimpan")
    
    print("\nCatatan:")
    print("   - Pastikan file disimpan dengan benar")
    print("   - Tunggu beberapa detik untuk reload")
    print("   - Jika tidak reload, restart server manual")
    print("=" * 50)

def setup_development_environment():
    """Setup environment variables untuk development"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
    
    # Force development settings - DISABLE ALL SSL/HTTPS
    os.environ['DEBUG'] = 'True'
    os.environ['SECURE_SSL_REDIRECT'] = 'False'
    os.environ['SECURE_HSTS_SECONDS'] = '0'
    os.environ['SECURE_HSTS_INCLUDE_SUBDOMAINS'] = 'False'
    os.environ['SECURE_HSTS_PRELOAD'] = 'False'
    os.environ['CSRF_COOKIE_SECURE'] = 'False'
    os.environ['SESSION_COOKIE_SECURE'] = 'False'
    os.environ['SECURE_PROXY_SSL_HEADER'] = ''
    os.environ['SECURE_REFERRER_POLICY'] = ''
    os.environ['SECURE_CROSS_ORIGIN_OPENER_POLICY'] = ''
    os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,0.0.0.0'
    
    # Disable production security features
    os.environ['SECURE_BROWSER_XSS_FILTER'] = 'False'
    os.environ['SECURE_CONTENT_TYPE_NOSNIFF'] = 'False'
    os.environ['X_FRAME_OPTIONS'] = 'SAMEORIGIN'
    
    # Disable CORS restrictions for development
    os.environ['CORS_ALLOW_ALL_ORIGINS'] = 'True'
    os.environ['CORS_ALLOW_CREDENTIALS'] = 'True'
    
    # Set development database - PostgreSQL
    os.environ['DATABASE_ENGINE'] = 'django.db.backends.postgresql'
    os.environ['DATABASE_NAME'] = 'postgres'
    os.environ['DATABASE_USER'] = 'postgres'
    os.environ['DATABASE_PASSWORD'] = 'root'
    os.environ['DATABASE_HOST'] = 'localhost'
    os.environ['DATABASE_PORT'] = '5432'
    
    # Disable cache for development
    os.environ['CACHE_BACKEND'] = 'django.core.cache.backends.dummy.DummyCache'
    
    # Set log level to INFO for development
    os.environ['LOG_LEVEL'] = 'INFO'
    
    # Optimasi untuk performa development
    os.environ['DEBUG_TOOLBAR'] = 'False'
    os.environ['COMPRESS_ENABLED'] = 'False'
    os.environ['STATICFILES_STORAGE'] = 'django.contrib.staticfiles.storage.StaticFilesStorage'
    
    # Disable unnecessary middleware untuk development
    os.environ['DISABLE_MIDDLEWARE'] = 'True'
    
    # Enable file monitoring untuk auto-reload
    os.environ['DJANGO_AUTO_RELOAD'] = 'True'
    os.environ['WATCHDOG_ENABLED'] = 'True'

def run_development_server():
    """Jalankan Django development server"""
    print("\n" + "=" * 60)
    print("WEBSITE DESA PULOSAROK - DEVELOPMENT SERVER")
    print("=" * 60 + "\n")
    
    # Skip venv check jika sudah dijalankan dari venv
    if not os.environ.get('VENV_ALREADY_ACTIVATED'):
        # Check dan activate venv
        if not check_and_activate_venv():
            sys.exit(1)
    else:
        print("OK: Virtual Environment sudah aktif (skip check)")
        print(f"   Python: {sys.executable}")
        print(f"   Version: {sys.version.split()[0]}")
    
    print("\n" + "-" * 60)
    
    # Hapus cache hanya jika belum dijalankan sebelumnya
    if not os.environ.get('CACHE_ALREADY_CLEARED'):
        # Hapus semua cache terlebih dahulu
        clear_all_caches()
        os.environ['CACHE_ALREADY_CLEARED'] = 'True'
    else:
        print("OK: Cache sudah dibersihkan sebelumnya (skip)")
    
    # Tampilkan instruksi Chrome
    clear_chrome_cache()
    
    # Tampilkan informasi monitoring file hanya sekali
    if not os.environ.get('MONITORING_INFO_SHOWN'):
        show_file_monitoring_info()
        os.environ['MONITORING_INFO_SHOWN'] = 'True'
    else:
        print("OK: Monitoring info sudah ditampilkan (skip)")
    
    print("\n" + "=" * 60)
    print("Memulai Django Development Server...")
    print("=" * 60)
    print("\nServer akan berjalan di: http://localhost:8000")
    print("Mode: Development (HTTPS disabled)")
    print("Auto-reload: ENABLED - Server akan restart otomatis saat ada perubahan")
    print("Threading: DISABLED - Untuk stabilitas development")
    print("Cache: DISABLED - Untuk development yang lebih responsif")
    print("Python: " + sys.executable)
    print("Django: " + django.get_version())
    print("\nServer akan otomatis restart ketika ada perubahan!")
    print("Tekan Ctrl+C untuk menghentikan server")
    print("=" * 60 + "\n")
    
    # Setup environment
    setup_development_environment()
    
    # Setup Django
    django.setup()
    
    # Run server dengan optimasi
    try:
        print("Starting Django development server...")
        print("Monitoring files for changes...")
        print("Auto-reload enabled - Server will restart on file changes")
        print("\n" + "=" * 60)
        
        # Enable auto-reload untuk development, gunakan threading untuk performa
        execute_from_command_line(['manage.py', 'runserver', 'localhost:8000', '--nothreading'])
    except KeyboardInterrupt:
        print("\n\nServer dihentikan oleh user")
        print("Terima kasih telah menggunakan development server!")
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}")
        print("Tips troubleshooting:")
        print("   - Pastikan virtual environment aktif")
        print("   - Periksa apakah port 8000 sudah digunakan")
        print("   - Jalankan 'python manage.py check' untuk cek konfigurasi")
        sys.exit(1)

if __name__ == '__main__':
    run_development_server()
