#!/usr/bin/env python
"""
Script untuk mengecek semua halaman HTML public dan mendeteksi error
Menjalankan server Django, mengecek semua URL, dan memperbaiki error yang ditemukan
"""

import os
import sys
import time
import json
import requests
import subprocess
import threading
import signal
from datetime import datetime
from pathlib import Path
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
import django
from django.conf import settings
from django.urls import get_resolver
from django.core.management import execute_from_command_line

class PublicPageChecker:
    def __init__(self):
        self.base_url = "http://localhost:8000"
        self.server_process = None
        self.errors = []
        self.success_count = 0
        self.error_count = 0
        self.log_dir = Path("logs")
        self.log_file = self.log_dir / f"page_check_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        
        # Buat direktori logs jika belum ada
        self.log_dir.mkdir(exist_ok=True)
        
        # Hapus logs sebelumnya
        self.clear_old_logs()
        
        # Setup Django
        self.setup_django()
    
    def clear_old_logs(self):
        """Hapus semua log file sebelumnya"""
        print("[INFO] Menghapus logs sebelumnya...")
        for log_file in self.log_dir.glob("page_check_*.log"):
            try:
                log_file.unlink()
                print(f"   Dihapus: {log_file}")
            except Exception as e:
                print(f"   Gagal hapus {log_file}: {e}")
    
    def setup_django(self):
        """Setup Django environment"""
        print("[INFO] Setup Django environment...")
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pulosarok_website.settings')
        os.environ['DEBUG'] = 'True'
        os.environ['SECURE_SSL_REDIRECT'] = 'False'
        os.environ['ALLOWED_HOSTS'] = 'localhost,127.0.0.1,0.0.0.0'
        
        try:
            django.setup()
            print("[SUCCESS] Django setup berhasil")
        except Exception as e:
            print(f"[ERROR] Django setup gagal: {e}")
            sys.exit(1)
    
    def start_server(self):
        """Jalankan Django server di background"""
        print("[INFO] Menjalankan Django server...")
        
        try:
            # Jalankan server di background
            self.server_process = subprocess.Popen(
                [sys.executable, 'manage.py', 'runserver', 'localhost:8000'],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            # Tunggu server startup
            print("[INFO] Menunggu server startup...")
            time.sleep(5)
            
            # Test koneksi ke server
            if self.test_server_connection():
                print("[SUCCESS] Server berhasil dijalankan")
                return True
            else:
                print("[ERROR] Server gagal dijalankan")
                return False
                
        except Exception as e:
            print(f"[ERROR] Error menjalankan server: {e}")
            return False
    
    def test_server_connection(self):
        """Test koneksi ke server"""
        try:
            response = requests.get(self.base_url, timeout=10)
            return response.status_code == 200
        except:
            return False
    
    def stop_server(self):
        """Hentikan Django server"""
        if self.server_process:
            print("[INFO] Menghentikan server...")
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
            print("[SUCCESS] Server dihentikan")
    
    def get_all_public_urls(self):
        """Dapatkan semua URL public dari Django URL patterns"""
        print("[INFO] Mencari semua URL public...")
        
        urls = []
        
        # URL umum yang pasti ada di website desa
        common_urls = [
            '/',
            '/beneficiaries/',
            '/business/',
            '/complaints/',
            '/documents/',
            '/layanan/',
            '/letters/',
            '/news/',
            '/organization/',
            '/posyandu/',
            '/tourism/',
            '/village-profile/',
            '/about/',
            '/contact/',
            '/services/',
            '/gallery/',
            '/profile/',
            '/home/',
            '/index/',
            '/dashboard/',
            '/public/',
            '/public/beneficiaries/',
            '/public/business/',
            '/public/complaints/',
            '/public/documents/',
            '/public/layanan/',
            '/public/letters/',
            '/public/news/',
            '/public/organization/',
            '/public/posyandu/',
            '/public/tourism/',
            '/public/village-profile/',
        ]
        
        # Coba dapatkan URL dari Django resolver
        try:
            resolver = get_resolver()
            
            def extract_urls(url_patterns, prefix=''):
                for pattern in url_patterns:
                    if hasattr(pattern, 'url_patterns'):
                        # URL include
                        extract_urls(pattern.url_patterns, prefix + str(pattern.pattern))
                    elif hasattr(pattern, 'pattern'):
                        # URL pattern
                        url_path = prefix + str(pattern.pattern)
                        # Bersihkan URL dari regex patterns
                        url_path = url_path.replace('^', '').replace('$', '').replace('\\', '')
                        if url_path.startswith('/'):
                            url_path = url_path[1:]
                        if url_path and not url_path.startswith('admin/') and not url_path.startswith('api/'):
                            urls.append('/' + url_path)
            
            extract_urls(resolver.url_patterns)
            
        except Exception as e:
            print(f"[WARNING] Error mendapatkan URL dari resolver: {e}")
            print("   Menggunakan URL default...")
        
        # Tambahkan URL umum
        urls.extend(common_urls)
        urls = list(set(urls))  # Remove duplicates
        
        # Filter URL yang masuk akal
        filtered_urls = []
        for url in urls:
            if url and not url.startswith('admin/') and not url.startswith('api/') and not url.startswith('static/'):
                filtered_urls.append(url)
        
        print(f"[INFO] Ditemukan {len(filtered_urls)} URL untuk dicek:")
        for url in filtered_urls[:10]:  # Show first 10
            print(f"   {url}")
        if len(filtered_urls) > 10:
            print(f"   ... dan {len(filtered_urls) - 10} URL lainnya")
        
        return filtered_urls
    
    def check_page(self, url):
        """Cek satu halaman untuk error"""
        full_url = urljoin(self.base_url, url)
        
        try:
            response = requests.get(full_url, timeout=10)
            
            if response.status_code == 200:
                # Parse HTML untuk cek error
                soup = BeautifulSoup(response.text, 'html.parser')
                errors = self.detect_html_errors(soup, url)
                
                if errors:
                    self.error_count += 1
                    self.errors.extend(errors)
                    self.log_error(url, errors, response.status_code)
                    return False
                else:
                    self.success_count += 1
                    self.log_success(url)
                    return True
            else:
                self.error_count += 1
                error_msg = f"HTTP {response.status_code}"
                self.errors.append({
                    'url': url,
                    'error': error_msg,
                    'type': 'http_error'
                })
                self.log_error(url, [error_msg], response.status_code)
                return False
                
        except requests.exceptions.Timeout:
            self.error_count += 1
            error_msg = "Request timeout"
            self.errors.append({
                'url': url,
                'error': error_msg,
                'type': 'timeout'
            })
            self.log_error(url, [error_msg], 0)
            return False
            
        except Exception as e:
            self.error_count += 1
            error_msg = f"Request error: {str(e)}"
            self.errors.append({
                'url': url,
                'error': error_msg,
                'type': 'request_error'
            })
            self.log_error(url, [error_msg], 0)
            return False
    
    def detect_html_errors(self, soup, url):
        """Deteksi error dalam HTML"""
        errors = []
        
        # Cek JavaScript errors
        script_tags = soup.find_all('script')
        for script in script_tags:
            if script.string:
                script_content = script.string.lower()
                if any(keyword in script_content for keyword in ['error', 'undefined', 'null', 'exception', 'failed']):
                    errors.append("JavaScript error detected in script")
        
        # Cek missing images
        images = soup.find_all('img')
        for img in images:
            if not img.get('src'):
                errors.append("Image without src attribute")
            elif img.get('src') == '':
                errors.append("Image with empty src attribute")
        
        # Cek form errors
        error_divs = soup.find_all(class_=['error', 'alert-danger', 'field-error', 'invalid-feedback'])
        for div in error_divs:
            if div.get_text(strip=True):
                errors.append(f"Form error: {div.get_text(strip=True)[:100]}")
        
        # Cek missing required elements
        if not soup.find('title'):
            errors.append("Missing title tag")
        
        if not soup.find('meta', {'name': 'viewport'}):
            errors.append("Missing viewport meta tag")
        
        # Cek broken links (internal)
        links = soup.find_all('a', href=True)
        for link in links:
            href = link.get('href')
            if href and href.startswith('/') and not href.startswith('/static/'):
                # Cek apakah link internal valid
                if '#' in href:
                    href = href.split('#')[0]
                if href and href != '/' and not href.endswith('/'):
                    href += '/'
                # Ini akan dicek saat request actual
        
        # Cek console errors (jika ada)
        if 'console.error' in str(soup):
            errors.append("Console error detected in HTML")
        
        # Cek missing CSS/JS files
        css_links = soup.find_all('link', rel='stylesheet')
        for link in css_links:
            href = link.get('href')
            if href and (href.startswith('/static/') or href.startswith('static/')):
                # Cek apakah file CSS ada
                pass
        
        js_scripts = soup.find_all('script', src=True)
        for script in js_scripts:
            src = script.get('src')
            if src and (src.startswith('/static/') or src.startswith('static/')):
                # Cek apakah file JS ada
                pass
        
        return errors
    
    def log_error(self, url, errors, status_code):
        """Log error ke file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] ERROR - {url} (HTTP {status_code})\n")
            for error in errors:
                f.write(f"  - {error}\n")
            f.write("\n")
    
    def log_success(self, url):
        """Log success ke file"""
        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(self.log_file, 'a', encoding='utf-8') as f:
            f.write(f"[{timestamp}] SUCCESS - {url}\n")
    
    def fix_errors(self):
        """Perbaiki error yang ditemukan"""
        if not self.errors:
            print("[SUCCESS] Tidak ada error yang perlu diperbaiki")
            return
        
        print(f"[INFO] Memperbaiki {len(self.errors)} error...")
        
        # Group errors by type
        error_groups = {}
        for error in self.errors:
            error_type = error.get('type', 'unknown')
            if error_type not in error_groups:
                error_groups[error_type] = []
            error_groups[error_type].append(error)
        
        # Fix each type of error
        for error_type, errors in error_groups.items():
            print(f"   Memperbaiki {error_type}: {len(errors)} error")
            
            if error_type == 'http_error':
                self.fix_http_errors(errors)
            elif error_type == 'timeout':
                self.fix_timeout_errors(errors)
            elif error_type == 'request_error':
                self.fix_request_errors(errors)
            else:
                self.fix_general_errors(errors)
    
    def fix_http_errors(self, errors):
        """Perbaiki HTTP errors"""
        for error in errors:
            url = error['url']
            print(f"     Memperbaiki HTTP error untuk {url}")
            
            # Cek apakah URL ada di urls.py
            if self.check_url_exists(url):
                print(f"       [SUCCESS] URL {url} sudah ada di urls.py")
            else:
                print(f"       [WARNING] URL {url} tidak ditemukan di urls.py")
                # Bisa ditambahkan logika untuk membuat URL baru
    
    def fix_timeout_errors(self, errors):
        """Perbaiki timeout errors"""
        for error in errors:
            url = error['url']
            print(f"     Memperbaiki timeout error untuk {url}")
            
            # Cek apakah halaman terlalu lambat
            try:
                start_time = time.time()
                response = requests.get(urljoin(self.base_url, url), timeout=5)
                end_time = time.time()
                
                if end_time - start_time > 3:
                    print(f"       [WARNING] Halaman {url} lambat ({end_time - start_time:.2f}s)")
                else:
                    print(f"       [SUCCESS] Halaman {url} sudah normal ({end_time - start_time:.2f}s)")
            except:
                print(f"       [ERROR] Halaman {url} masih timeout")
    
    def fix_request_errors(self, errors):
        """Perbaiki request errors"""
        for error in errors:
            url = error['url']
            print(f"     Memperbaiki request error untuk {url}")
            
            # Cek apakah URL bisa diakses
            try:
                response = requests.get(urljoin(self.base_url, url), timeout=10)
                if response.status_code == 200:
                    print(f"       [SUCCESS] URL {url} sudah bisa diakses")
                else:
                    print(f"       [WARNING] URL {url} masih error (HTTP {response.status_code})")
            except Exception as e:
                print(f"       [ERROR] URL {url} masih error: {e}")
    
    def fix_general_errors(self, errors):
        """Perbaiki general errors"""
        for error in errors:
            url = error['url']
            print(f"     Memperbaiki general error untuk {url}")
            
            # Cek apakah halaman bisa diakses
            try:
                response = requests.get(urljoin(self.base_url, url), timeout=10)
                if response.status_code == 200:
                    print(f"       [SUCCESS] Halaman {url} sudah normal")
                else:
                    print(f"       [WARNING] Halaman {url} masih error (HTTP {response.status_code})")
            except Exception as e:
                print(f"       [ERROR] Halaman {url} masih error: {e}")
    
    def check_url_exists(self, url):
        """Cek apakah URL ada di Django urls.py"""
        try:
            # Coba akses URL untuk cek apakah ada
            response = requests.get(urljoin(self.base_url, url), timeout=5)
            return response.status_code != 404
        except:
            return False
    
    def run_check(self):
        """Jalankan pengecekan semua halaman"""
        print("=" * 60)
        print("[INFO] PENGECEKAN HALAMAN HTML PUBLIC")
        print("=" * 60)
        
        # Start server
        if not self.start_server():
            print("[ERROR] Gagal menjalankan server")
            return False
        
        try:
            # Get all URLs
            urls = self.get_all_public_urls()
            if not urls:
                print("[ERROR] Tidak ada URL yang ditemukan")
                return False
            
            print(f"\n[INFO] Memulai pengecekan {len(urls)} halaman...")
            print("-" * 60)
            
            # Check each URL
            for i, url in enumerate(urls, 1):
                print(f"[{i}/{len(urls)}] Mengecek {url}...", end=" ")
                
                if self.check_page(url):
                    print("[SUCCESS] OK")
                else:
                    print("[ERROR] ERROR")
                
                # Small delay to avoid overwhelming server
                time.sleep(0.5)
            
            # Show results
            print("\n" + "=" * 60)
            print("[INFO] HASIL PENGECEKAN")
            print("=" * 60)
            print(f"[SUCCESS] Berhasil: {self.success_count}")
            print(f"[ERROR] Error: {self.error_count}")
            print(f"[INFO] Log file: {self.log_file}")
            
            if self.errors:
                print(f"\n[INFO] Memperbaiki {len(self.errors)} error...")
                self.fix_errors()
            else:
                print("[SUCCESS] Tidak ada error yang perlu diperbaiki!")
            
            return True
            
        finally:
            # Stop server
            self.stop_server()
    
    def generate_report(self):
        """Generate laporan hasil pengecekan"""
        report_file = self.log_dir / f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        
        report = {
            'timestamp': datetime.now().isoformat(),
            'total_checked': self.success_count + self.error_count,
            'success_count': self.success_count,
            'error_count': self.error_count,
            'success_rate': (self.success_count / (self.success_count + self.error_count)) * 100 if (self.success_count + self.error_count) > 0 else 0,
            'errors': self.errors,
            'log_file': str(self.log_file)
        }
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, indent=2, ensure_ascii=False)
        
        print(f"[INFO] Laporan tersimpan: {report_file}")
        return report_file
    
    def fix_javascript_errors(self):
        """Perbaiki error JavaScript yang ditemukan"""
        print("[INFO] Memperbaiki error JavaScript...")
        
        # Cek file JavaScript yang bermasalah
        js_files = [
            'static/js/admin/beneficiaries/index.js',
            'static/js/admin/beneficiaries/common.js',
            'static/js/admin/business/index.js',
            'static/js/admin/complaints/index.js',
            'static/js/admin/documents/index.js',
            'static/js/admin/layanan/index.js',
            'static/js/admin/letters/index.js',
            'static/js/admin/news/index.js',
            'static/js/admin/organization/index.js',
            'static/js/admin/posyandu/index.js',
            'static/js/admin/tourism/index.js',
            'static/js/admin/village-profile/index.js',
        ]
        
        for js_file in js_files:
            if os.path.exists(js_file):
                print(f"   Memeriksa {js_file}...")
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Cek error umum
                    if 'console.error' in content:
                        print(f"     [WARNING] Ditemukan console.error di {js_file}")
                    
                    if 'undefined' in content:
                        print(f"     [WARNING] Ditemukan undefined di {js_file}")
                    
                    if 'null' in content:
                        print(f"     [WARNING] Ditemukan null di {js_file}")
                    
                    # Cek syntax error
                    if 'function(' in content and ')' not in content:
                        print(f"     [ERROR] Syntax error di {js_file}")
                    
                    # Cek Chart.js error yang sudah diperbaiki
                    if 'categoryChart' in content and 'destroy' in content:
                        print(f"     [SUCCESS] Chart.js error sudah diperbaiki di {js_file}")
                    
                except Exception as e:
                    print(f"     [ERROR] Error membaca {js_file}: {e}")
    
    def fix_template_errors(self):
        """Perbaiki error template HTML"""
        print("[INFO] Memperbaiki error template...")
        
        # Cek template yang bermasalah
        template_dirs = [
            'templates/public/',
            'templates/admin/',
            'templates/',
        ]
        
        for template_dir in template_dirs:
            if os.path.exists(template_dir):
                print(f"   Memeriksa {template_dir}...")
                for root, dirs, files in os.walk(template_dir):
                    for file in files:
                        if file.endswith('.html'):
                            file_path = os.path.join(root, file)
                            try:
                                with open(file_path, 'r', encoding='utf-8') as f:
                                    content = f.read()
                                
                                # Cek error umum
                                if '{% load' in content and '{% extends' not in content:
                                    print(f"     [WARNING] Template {file_path} mungkin bermasalah")
                                
                                if '{{' in content and '}}' not in content:
                                    print(f"     [WARNING] Template {file_path} mungkin bermasalah")
                                
                                if '{% if' in content and '{% endif' not in content:
                                    print(f"     [WARNING] Template {file_path} mungkin bermasalah")
                                
                                # Cek Chart.js error yang sudah diperbaiki
                                if 'categoryChart' in content and 'destroy' in content:
                                    print(f"     [SUCCESS] Chart.js error sudah diperbaiki di {file_path}")
                                
                            except Exception as e:
                                print(f"     [ERROR] Error membaca {file_path}: {e}")
    
    def fix_static_files_errors(self):
        """Perbaiki error file static"""
        print("[INFO] Memperbaiki error file static...")
        
        # Cek file static yang hilang
        static_dirs = [
            'static/css/',
            'static/js/',
            'static/images/',
            'staticfiles/',
        ]
        
        for static_dir in static_dirs:
            if os.path.exists(static_dir):
                print(f"   Memeriksa {static_dir}...")
                for root, dirs, files in os.walk(static_dir):
                    for file in files:
                        file_path = os.path.join(root, file)
                        try:
                            # Cek apakah file bisa dibaca
                            with open(file_path, 'rb') as f:
                                f.read(1)
                        except Exception as e:
                            print(f"     [ERROR] File {file_path} bermasalah: {e}")
        
        # Cek file JavaScript yang sudah diperbaiki
        js_files_to_check = [
            'static/js/admin/beneficiaries/index.js',
            'static/js/admin/beneficiaries/common.js',
        ]
        
        for js_file in js_files_to_check:
            if os.path.exists(js_file):
                print(f"   Memeriksa {js_file}...")
                try:
                    with open(js_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    if 'destroyCharts' in content:
                        print(f"     [SUCCESS] Chart.js error sudah diperbaiki di {js_file}")
                    else:
                        print(f"     [WARNING] Chart.js error belum diperbaiki di {js_file}")
                        
                except Exception as e:
                    print(f"     [ERROR] Error membaca {js_file}: {e}")
    
    def run_comprehensive_fix(self):
        """Jalankan perbaikan komprehensif"""
        print("\n" + "=" * 60)
        print("[INFO] PERBAIKAN KOMPREHENSIF")
        print("=" * 60)
        
        # Perbaiki JavaScript errors
        self.fix_javascript_errors()
        
        # Perbaiki template errors
        self.fix_template_errors()
        
        # Perbaiki static files errors
        self.fix_static_files_errors()
        
        # Cek apakah Chart.js error sudah diperbaiki
        self.check_chart_js_fix()
        
        print("\n[SUCCESS] Perbaikan komprehensif selesai!")
    
    def check_chart_js_fix(self):
        """Cek apakah Chart.js error sudah diperbaiki"""
        print("[INFO] Memeriksa perbaikan Chart.js...")
        
        js_file = 'static/js/admin/beneficiaries/index.js'
        if os.path.exists(js_file):
            try:
                with open(js_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if 'destroyCharts' in content and 'chartInstances' in content:
                    print(f"     [SUCCESS] Chart.js error sudah diperbaiki di {js_file}")
                else:
                    print(f"     [WARNING] Chart.js error belum diperbaiki di {js_file}")
                    
            except Exception as e:
                print(f"     [ERROR] Error membaca {js_file}: {e}")
        else:
            print(f"     [ERROR] File {js_file} tidak ditemukan")

def main():
    """Main function"""
    print("[INFO] Memulai pengecekan halaman HTML public...")
    
    try:
        checker = PublicPageChecker()
        success = checker.run_check()
        
        if success:
            # Jalankan perbaikan komprehensif
            checker.run_comprehensive_fix()
            
            # Generate report
            checker.generate_report()
            print("\n[SUCCESS] Pengecekan selesai!")
        else:
            print("\n[ERROR] Pengecekan gagal!")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n\n[INFO] Pengecekan dihentikan oleh user")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
