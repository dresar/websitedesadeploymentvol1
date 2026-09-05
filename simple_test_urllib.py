#!/usr/bin/env python
"""
Simple Error Pages Test untuk Production Mode
"""

import urllib.request
import urllib.error
import time
import ssl

def test_error_pages():
    """
    Test custom error pages dengan urllib
    """
    base_url = "http://127.0.0.1:8000"
    
    print("🧪 Testing Custom Error Pages...")
    print("=" * 50)
    
    # Disable SSL warnings
    ssl._create_default_https_context = ssl._create_unverified_context
    
    # Test 404
    print("Testing 404 Error Page...")
    try:
        req = urllib.request.Request(f"{base_url}/nonexistent-page/")
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            print(f"✅ 404 Error Page: Status {response.status}")
            if "Halaman Tidak Ditemukan" in content:
                print("✅ Custom 404 template detected!")
            else:
                print("❌ Custom 404 template not found")
                print("Content preview:", content[:200] + "...")
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"✅ 404 Error Page: Status {e.code}")
            content = e.read().decode('utf-8')
            if "Halaman Tidak Ditemukan" in content:
                print("✅ Custom 404 template detected!")
            else:
                print("❌ Custom 404 template not found")
                print("Content preview:", content[:200] + "...")
        else:
            print(f"❌ 404 Error Page: Unexpected status {e.code}")
    except Exception as e:
        print(f"❌ 404 Error Page: ERROR - {e}")
    
    print()
    
    # Test 403
    print("Testing 403 Error Page...")
    try:
        req = urllib.request.Request(f"{base_url}/admin-panel/")
        with urllib.request.urlopen(req, timeout=10) as response:
            content = response.read().decode('utf-8')
            print(f"✅ 403 Error Page: Status {response.status}")
            if "Akses Ditolak" in content:
                print("✅ Custom 403 template detected!")
            else:
                print("❌ Custom 403 template not found")
    except urllib.error.HTTPError as e:
        if e.code == 403:
            print(f"✅ 403 Error Page: Status {e.code}")
            content = e.read().decode('utf-8')
            if "Akses Ditolak" in content:
                print("✅ Custom 403 template detected!")
            else:
                print("❌ Custom 403 template not found")
        else:
            print(f"❌ 403 Error Page: Unexpected status {e.code}")
    except Exception as e:
        print(f"❌ 403 Error Page: ERROR - {e}")
    
    print()
    print("=" * 50)
    print("🎯 Error Pages Test Complete!")
    print()
    print("📝 Manual Testing:")
    print("1. Open browser and go to: http://127.0.0.1:8000/nonexistent-page/")
    print("2. You should see custom 404 page with 'Halaman Tidak Ditemukan'")
    print("3. Try: http://127.0.0.1:8000/admin-panel/ (should show 403)")
    print("4. Check browser developer tools for security headers")

if __name__ == '__main__':
    # Wait for server to start
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    test_error_pages()
