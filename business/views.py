from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.http import require_http_methods
from django.middleware.csrf import get_token
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.generic import ListView
import json
from datetime import datetime, timedelta

from .models import (
    Business, BusinessCategory, BusinessProduct, 
    BusinessFinance, UKM, Koperasi, BUMG, Aset, LayananJasa, BusinessPageHeader,
    JenisKoperasi
)
from .forms import LayananJasaForm, UKMForm, KoperasiForm, BUMGForm, BusinessForm
# Import Penduduk from references app
try:
    from references.models import Penduduk
except ImportError:
    try:
        from letters.models import Penduduk
    except ImportError:
        Penduduk = None

# Helper functions
def is_admin(user):
    return user.is_staff or user.is_superuser

def get_business_statistics():
    """Get business statistics for dashboard"""
    stats = {
        'total_businesses': Business.objects.filter(status='approved').count(),
        'total_umkm': UKM.objects.filter(status='aktif').count(),
        'total_koperasi': Koperasi.objects.filter(status='aktif').count(),
        'total_bumg': BUMG.objects.filter(status='aktif').count(),
        'total_layanan': LayananJasa.objects.filter(status='aktif').count(),
        'pending_approvals': Business.objects.filter(status='pending').count(),
    }
    return stats

# Public Views
def business_list(request):
    """Halaman daftar bisnis publik"""
    businesses = Business.objects.filter(status='approved').select_related('category').order_by('-created_at')
    categories = BusinessCategory.objects.all()
    
    # Filter berdasarkan kategori
    category_id = request.GET.get('category')
    if category_id:
        businesses = businesses.filter(category_id=category_id)
    
    # Filter berdasarkan jenis bisnis
    business_type = request.GET.get('type')
    if business_type:
        businesses = businesses.filter(business_type=business_type)
    
    # Fungsi pencarian
    search = request.GET.get('search')
    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(businesses, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistik untuk dashboard
    stats = {
        'total_businesses': businesses.count(),
        'business_types': Business.objects.filter(status='approved').values('business_type').annotate(count=Count('id')),
        'categories': categories.annotate(business_count=Count('businesses', filter=Q(businesses__status='approved')))
    }
    
    # Get page header for business list
    try:
        from .models import BusinessPageHeader
        page_header = BusinessPageHeader.objects.filter(
            page_type='business_list',
            is_active=True
        ).first()
    except:
        page_header = None
    
    context = {
        'business_list': page_obj,
        'businesses': page_obj,  # Keep both for compatibility
        'categories': categories,
        'stats': stats,
        'page_header': page_header,
        'search_query': search,
        'is_paginated': page_obj.has_other_pages(),
    }

    return render(request, 'public/business/business_list.html', context)

def business_detail(request, business_id):
    """Public business detail page"""
    business = get_object_or_404(Business, id=business_id, status='approved')
    products = BusinessProduct.objects.filter(business=business)
    
    # Get page header for business detail
    try:
        from .models import BusinessPageHeader
        page_header = BusinessPageHeader.objects.filter(
            page_type='business_detail',
            is_active=True
        ).first()
    except:
        page_header = None
    
    context = {
        'business': business,
        'products': products,
        'page_header': page_header,
    }
    return render(request, 'public/business/business_detail.html', context)

def business_register(request):
    """Formulir pendaftaran bisnis publik"""
    if request.method == 'POST':
        # Handle form submission
        pass
    
    context = {
        'page_title': 'Daftar Bisnis Baru',
    }
    return render(request, 'public/business/business_register.html', context)

def umkm_list_public(request):
    """Halaman daftar UMKM publik"""
    umkm_list = UKM.objects.filter(status='aktif').order_by('-created_at')
    
    # Filter dan pencarian
    search = request.GET.get('search')
    if search:
        umkm_list = umkm_list.filter(
            Q(nama_usaha__icontains=search) |
            Q(pemilik__icontains=search) |
            Q(jenis_usaha__icontains=search) |
            Q(produk_utama__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(umkm_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'umkm_list': page_obj,
        'search_query': search,
        'page_title': 'Daftar UMKM',
    }
    return render(request, 'public/business/umkm_list.html', context)

def umkm_detail_public(request, umkm_id):
    """Public UMKM detail page"""
    umkm = get_object_or_404(UKM, id=umkm_id, status='aktif')
    
    context = {
        'umkm': umkm,
        'page_title': f'Detail {umkm.nama_usaha}',
    }
    return render(request, 'public/business/umkm_detail.html', context)

def koperasi_list_public(request):
    """Halaman daftar Koperasi publik"""
    koperasi_list = Koperasi.objects.filter(status='aktif').order_by('-created_at')
    
    # Filter dan pencarian
    search = request.GET.get('search')
    if search:
        koperasi_list = koperasi_list.filter(
            Q(nama__icontains=search) |
            Q(ketua__icontains=search) |
            Q(alamat__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(koperasi_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'koperasi_list': page_obj,
        'search_query': search,
        'page_title': 'Daftar Koperasi',
    }
    return render(request, 'public/business/koperasi_list.html', context)

def koperasi_detail_public(request, koperasi_id):
    """Detail koperasi publik"""
    koperasi = get_object_or_404(Koperasi, id=koperasi_id, status='aktif')
    
    context = {
        'koperasi': koperasi,
    }
    return render(request, 'public/business/koperasi_detail.html', context)

def bumg_list_public(request):
    """Halaman daftar BUMG publik"""
    bumg_list = BUMG.objects.filter(status='aktif').order_by('-created_at')
    
    # Filter dan pencarian
    search = request.GET.get('search')
    if search:
        bumg_list = bumg_list.filter(
            Q(nama__icontains=search) |
            Q(direktur__icontains=search) |
            Q(bidang_usaha__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(bumg_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'bumg_list': page_obj,
        'search_query': search,
        'page_title': 'Daftar BUMG',
    }
    return render(request, 'public/business/bumg_list.html', context)

def bumg_detail_public(request, bumg_id):
    """Public BUMG detail page"""
    bumg = get_object_or_404(BUMG, id=bumg_id, status='aktif')
    
    context = {
        'bumg': bumg,
        'page_title': f'Detail {bumg.nama}',
    }
    return render(request, 'public/business/bumg_detail.html', context)

def toko_warung_list(request):
    """Halaman daftar Toko dan Warung"""
    toko_warung = Business.objects.filter(
        status='approved', 
        business_type__in=['warung', 'umkm']
    ).select_related('category').order_by('-created_at')
    categories = BusinessCategory.objects.filter(is_active=True)
    
    # Filter dan pencarian
    category_id = request.GET.get('category')
    if category_id:
        toko_warung = toko_warung.filter(category_id=category_id)
    
    business_type = request.GET.get('type')
    if business_type and business_type in ['warung', 'umkm']:
        toko_warung = toko_warung.filter(business_type=business_type)
    
    search = request.GET.get('search')
    if search:
        toko_warung = toko_warung.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(address__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(toko_warung, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'businesses': page_obj,
        'toko_list': page_obj,  # Add toko_list for template compatibility
        'categories': categories,
        'current_category': category_id,
        'current_type': business_type,
        'search_query': search,
        'page_title': 'Daftar Toko & Warung',
        'business_type': 'toko_warung',
        'sub_types': [('warung', 'Warung'), ('umkm', 'UMKM')],
    }
    return render(request, 'public/business/toko_warung_list.html', context)

def layanan_jasa_list(request):
    """Halaman daftar Layanan Jasa"""
    layanan_list = LayananJasa.objects.all()

    # Filter dan pencarian
    search = request.GET.get('search')
    if search:
        layanan_list = layanan_list.filter(
            Q(nama__icontains=search) |
            Q(penyedia__icontains=search) |
            Q(kategori__icontains=search) |
            Q(deskripsi__icontains=search)
        ).distinct()
    
    # Pagination
    paginator = Paginator(layanan_list, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'layanan_list': page_obj,
        'search_query': search,
        'page_title': 'Daftar Layanan Jasa',
    }
    return render(request, 'public/business/layanan_jasa_list.html', context)

def layanan_jasa_detail_public(request, layanan_id):
    """Public Layanan Jasa detail page"""
    layanan = get_object_or_404(LayananJasa, id=layanan_id, status='aktif')
    
    context = {
        'layanan': layanan,
        'page_title': f'Detail {layanan.nama}',
    }
    return render(request, 'public/business/layanan_jasa_detail.html', context)

# API Views
@ensure_csrf_cookie
def get_csrf_token(request):
    """Get CSRF token for AJAX requests"""
    return JsonResponse({'csrfToken': get_token(request)})

@csrf_exempt
@require_http_methods(["POST"])
def api_business_register(request):
    """API untuk registrasi bisnis"""
    try:
        data = json.loads(request.body)
        # Handle business registration logic here
        return JsonResponse({'success': True, 'message': 'Bisnis berhasil didaftarkan'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def api_business_list(request):
    """API untuk mendapatkan daftar bisnis"""
    business_type = request.GET.get('type', 'all')
    search = request.GET.get('search', '')
    
    if business_type == 'toko_warung':
        businesses = Business.objects.filter(
            status='approved',
            business_type__in=['warung', 'umkm']
        )
    else:
        businesses = Business.objects.filter(status='approved')
    
    if search:
        businesses = businesses.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search)
        )
    
    business_list = []
    for business in businesses[:20]:  # Limit to 20 results
        business_list.append({
            'id': business.id,
            'name': business.name,
            'business_type': business.business_type,
            'description': business.description,
            'address': getattr(business, 'address', ''),
            'phone': getattr(business, 'phone', ''),
            'email': getattr(business, 'email', ''),
            'website': getattr(business, 'website', ''),
        })
    
    return JsonResponse({
        'success': True,
        'businesses': business_list
    })

def api_business_detail(request, business_id):
    """API untuk detail bisnis"""
    try:
        business = Business.objects.get(id=business_id, status='approved')
        return JsonResponse({
            'success': True,
            'business': {
                'id': business.id,
                'name': business.name,
                'business_type': business.business_type,
                'description': business.description,
                'address': business.address,
                'phone': business.phone,
                'email': business.email,
                'website': business.website,
            }
        })
    except Business.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Bisnis tidak ditemukan'})

def api_business_categories(request):
    """API untuk mendapatkan kategori bisnis"""
    categories = BusinessCategory.objects.filter(is_active=True)
    category_list = []
    for category in categories:
        category_list.append({
            'id': category.id,
            'name': category.name,
            'description': category.description,
        })
    
    return JsonResponse({
        'success': True,
        'categories': category_list
    })

def api_business_statistics(request):
    """API untuk statistik bisnis"""
    stats = get_business_statistics()
    return JsonResponse({
        'success': True,
        'statistics': stats
    })

def api_penduduk_search(request):
    """API untuk pencarian penduduk - Enhanced version"""
    try:
        query = request.GET.get('q', '')
        limit = int(request.GET.get('limit', 10))
        
        # Return empty results if query too short
        if len(query) < 2:
            return JsonResponse({
                'success': True,
                'results': [],
                'message': 'Minimal 2 karakter untuk pencarian'
            })
        
        if Penduduk:
            # Search by name or NIK
            penduduk_list = Penduduk.objects.filter(
                Q(name__icontains=query) | Q(nik__icontains=query)
            ).select_related('dusun', 'lorong')[:limit]
            
            results = []
            for penduduk in penduduk_list:
                # Get all available fields with correct field names
                result_item = {
                    'id': penduduk.id,
                    'nama': penduduk.name,  # Model field: name
                    'nik': penduduk.nik,  # Model field: nik
                    'tempat_lahir': getattr(penduduk, 'birth_place', ''),  # Model field: birth_place
                    'tanggal_lahir': str(penduduk.birth_date) if hasattr(penduduk, 'birth_date') and penduduk.birth_date else '',  # Model field: birth_date
                    'jenis_kelamin': penduduk.get_gender_display() if hasattr(penduduk, 'gender') else '',  # Model field: gender
                    'alamat': penduduk.address if hasattr(penduduk, 'address') else '',  # Model field: address
                    'telepon': penduduk.phone_number or penduduk.mobile_number or '' if hasattr(penduduk, 'phone_number') else '',  # Model fields: phone_number, mobile_number
                    'email': penduduk.email if hasattr(penduduk, 'email') else '',  # Model field: email
                }
                
                # Add dusun info if available
                if hasattr(penduduk, 'dusun') and penduduk.dusun:
                    result_item['dusun'] = penduduk.dusun.name if hasattr(penduduk.dusun, 'name') else (penduduk.dusun.nama if hasattr(penduduk.dusun, 'nama') else '')
                    result_item['dusun_id'] = penduduk.dusun.id
                
                # Add lorong info if available
                if hasattr(penduduk, 'lorong') and penduduk.lorong:
                    result_item['lorong'] = penduduk.lorong.nama_lorong
                    result_item['lorong_id'] = penduduk.lorong.id
                
                results.append(result_item)
            
            return JsonResponse({
                'success': True,
                'results': results,
                'count': len(results),
                'message': f'Ditemukan {len(results)} penduduk'
            })
        else:
            return JsonResponse({
                'success': False,
                'results': [],
                'message': 'Model Penduduk tidak tersedia'
            })
    
    except Exception as e:
        return JsonResponse({
            'success': False,
            'results': [],
            'message': f'Error: {str(e)}'
        }, status=500)

def api_business_search(request):
    """API untuk pencarian bisnis"""
    query = request.GET.get('q', '')
    if len(query) < 2:
        return JsonResponse({'success': True, 'data': []})
    
    businesses = Business.objects.filter(
        Q(name__icontains=query) |
        Q(description__icontains=query)
    )[:10]
    
    results = []
    for business in businesses:
        results.append({
            'id': business.id,
            'name': business.name,
            'business_type': business.business_type,
            'address': getattr(business, 'address', ''),
        })
    
        return JsonResponse({'success': True, 'data': results})

# Admin Views
@login_required
@user_passes_test(is_admin)
def admin_business_dashboard(request):
    """Dashboard admin untuk bisnis"""
    stats = get_business_statistics()
    
    # Recent businesses
    recent_businesses = Business.objects.filter(status='pending').order_by('-created_at')[:5]
    
    context = {
        'stats': stats,
        'recent_businesses': recent_businesses,
    }
    return render(request, 'admin_panel/business/dashboard.html', context)

# Admin Panel Views
@login_required
@user_passes_test(is_admin)
def admin_ukm_list(request):
    """Admin UMKM list view"""
    search = request.GET.get('search', '')
    umkm_list = UKM.objects.all().order_by('-created_at')
    
    if search:
        umkm_list = umkm_list.filter(
            Q(nama_usaha__icontains=search) |
            Q(pemilik__icontains=search) |
            Q(jenis_usaha__icontains=search)
        )
    
    paginator = Paginator(umkm_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/umkm_list.html', {
        'page_obj': page_obj,
        'search': search
    })

@login_required
@user_passes_test(is_admin)
def umkm_create(request):
    """Create UMKM view"""
    if request.method == 'POST':
        # Debug: Log form data
        import logging
        logger = logging.getLogger(__name__)
        logger.info('=== UMKM Create Debug ===')
        logger.info(f'POST data keys: {list(request.POST.keys())}')
        logger.info(f'FILES data keys: {list(request.FILES.keys())}')
        
        # Debug: Check specific files
        if 'foto_usaha' in request.FILES:
            foto_file = request.FILES['foto_usaha']
            logger.info(f'Foto usaha file: {foto_file.name}, size: {foto_file.size}, type: {foto_file.content_type}')
        else:
            logger.info('No foto_usaha file in request')
            
        if 'logo_usaha' in request.FILES:
            logo_file = request.FILES['logo_usaha']
            logger.info(f'Logo usaha file: {logo_file.name}, size: {logo_file.size}, type: {logo_file.content_type}')
        else:
            logger.info('No logo_usaha file in request')
        
        form = UKMForm(request.POST, request.FILES)
        
        if form.is_valid():
            try:
                logger.info('Form is valid, saving...')
                ukm_instance = form.save()
                logger.info(f'UMKM created successfully: {ukm_instance.id}')
                
                # Debug: Check if files were saved
                if ukm_instance.foto_usaha:
                    logger.info(f'Foto usaha saved: {ukm_instance.foto_usaha.url}')
                if ukm_instance.logo_usaha:
                    logger.info(f'Logo usaha saved: {ukm_instance.logo_usaha.url}')
                
                messages.success(request, 'UMKM berhasil ditambahkan!')
                return redirect('admin_panel:umkm_list')
            except Exception as e:
                logger.error(f'Error creating UMKM: {str(e)}')
                logger.error(f'Error type: {type(e).__name__}')
                import traceback
                logger.error(f'Traceback: {traceback.format_exc()}')
                messages.error(request, f'Error: {str(e)}')
        else:
            logger.error('Form is not valid')
            logger.error(f'Form errors: {form.errors}')
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = UKMForm()
    
    return render(request, 'admin_panel/business/umkm_form.html', {
        'form': form,
        'umkm': None,
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def umkm_detail(request, umkm_id):
    """UMKM detail view"""
    ukm = get_object_or_404(UKM, id=umkm_id)
    return render(request, 'admin_panel/business/umkm_detail.html', {
        'umkm': ukm
    })

@login_required
@user_passes_test(is_admin)
def umkm_edit(request, umkm_id):
    """Edit UMKM view"""
    ukm = get_object_or_404(UKM, id=umkm_id)
    
    if request.method == 'POST':
        # Debug: Log form data
        import logging
        logger = logging.getLogger(__name__)
        logger.info(f'=== UMKM Edit Debug - ID: {umkm_id} ===')
        logger.info(f'POST data keys: {list(request.POST.keys())}')
        logger.info(f'FILES data keys: {list(request.FILES.keys())}')
        
        # Debug: Check specific files
        if 'foto_usaha' in request.FILES:
            foto_file = request.FILES['foto_usaha']
            logger.info(f'Foto usaha file: {foto_file.name}, size: {foto_file.size}, type: {foto_file.content_type}')
        else:
            logger.info('No foto_usaha file in request')
            
        if 'logo_usaha' in request.FILES:
            logo_file = request.FILES['logo_usaha']
            logger.info(f'Logo usaha file: {logo_file.name}, size: {logo_file.size}, type: {logo_file.content_type}')
        else:
            logger.info('No logo_usaha file in request')
        
        form = UKMForm(request.POST, request.FILES, instance=ukm)
        
        if form.is_valid():
            try:
                logger.info('Form is valid, saving...')
                ukm_instance = form.save()
                logger.info(f'UMKM saved successfully: {ukm_instance.id}')
                
                # Debug: Check if files were saved
                if ukm_instance.foto_usaha:
                    logger.info(f'Foto usaha saved: {ukm_instance.foto_usaha.url}')
                if ukm_instance.logo_usaha:
                    logger.info(f'Logo usaha saved: {ukm_instance.logo_usaha.url}')
                
                messages.success(request, 'UMKM berhasil diperbarui!')
                return redirect('admin_panel:umkm_list')
            except Exception as e:
                logger.error(f'Error saving UMKM {umkm_id}: {str(e)}')
                logger.error(f'Error type: {type(e).__name__}')
                import traceback
                logger.error(f'Traceback: {traceback.format_exc()}')
                messages.error(request, f'Error: {str(e)}')
        else:
            logger.error('Form is not valid')
            logger.error(f'Form errors: {form.errors}')
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = UKMForm(instance=ukm)
    
    return render(request, 'admin_panel/business/umkm_form.html', {
        'form': form,
        'umkm': ukm,  # Keep umkm for template compatibility
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def umkm_delete(request, umkm_id):
    """Delete UMKM view"""
    ukm = get_object_or_404(UKM, id=umkm_id)
    if request.method == 'POST':
        ukm.delete()
        messages.success(request, 'UMKM berhasil dihapus!')
        return redirect('admin_panel:umkm_list')
    return render(request, 'admin_panel/business/umkm_delete_confirm.html', {
        'umkm': ukm
    })

# Koperasi Views
@login_required
@user_passes_test(is_admin)
def koperasi_list(request):
    """Admin Koperasi list view"""
    search = request.GET.get('search', '')
    koperasi_list = Koperasi.objects.all().order_by('-created_at')
    
    if search:
        koperasi_list = koperasi_list.filter(
            Q(nama__icontains=search) |
            Q(ketua__icontains=search) |
            Q(sekretaris__icontains=search)
        )
    
    paginator = Paginator(koperasi_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/koperasi_admin.html', {
        'page_obj': page_obj,
        'search': search
    })

@login_required
@user_passes_test(is_admin)
def koperasi_create(request):
    """Create Koperasi view"""
    if request.method == 'POST':
        form = KoperasiForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Koperasi berhasil ditambahkan!')
                return redirect('admin_panel:koperasi_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = KoperasiForm()
    
    return render(request, 'admin_panel/business/koperasi_form.html', {
        'form': form,
        'koperasi': None,
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def koperasi_detail(request, koperasi_id):
    """Koperasi detail view"""
    koperasi = get_object_or_404(Koperasi, id=koperasi_id)
    return render(request, 'admin_panel/business/koperasi_detail.html', {
        'koperasi': koperasi
    })

@login_required
@user_passes_test(is_admin)
def koperasi_edit(request, koperasi_id):
    """Edit Koperasi view"""
    koperasi = get_object_or_404(Koperasi, id=koperasi_id)
    
    if request.method == 'POST':
        form = KoperasiForm(request.POST, request.FILES, instance=koperasi)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Koperasi berhasil diperbarui!')
                return redirect('admin_panel:koperasi_detail', koperasi_id=koperasi.id)
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = KoperasiForm(instance=koperasi)
    
    return render(request, 'admin_panel/business/koperasi_form.html', {
        'form': form,
        'koperasi': koperasi,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def koperasi_delete(request, koperasi_id):
    """Delete Koperasi view"""
    koperasi = get_object_or_404(Koperasi, id=koperasi_id)
    if request.method == 'POST':
        koperasi.delete()
        messages.success(request, 'Koperasi berhasil dihapus!')
        return redirect('admin_panel:koperasi_list')
    return render(request, 'admin_panel/business/koperasi_delete_confirm.html', {
        'koperasi': koperasi
    })

# BUMG Views
@login_required
@user_passes_test(is_admin)
def bumg_list(request):
    """Admin BUMG list view"""
    search = request.GET.get('search', '')
    bumg_list = BUMG.objects.all().order_by('-created_at')
    
    if search:
        bumg_list = bumg_list.filter(
            Q(nama__icontains=search) |
            Q(direktur__icontains=search) |
            Q(bidang_usaha__icontains=search)
        )
    
    paginator = Paginator(bumg_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/bumg_admin.html', {
        'page_obj': page_obj,
        'search': search
    })

@login_required
@user_passes_test(is_admin)
def bumg_create(request):
    """Create BUMG view"""
    if request.method == 'POST':
        form = BUMGForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'BUMG berhasil ditambahkan!')
                return redirect('admin_panel:bumg_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = BUMGForm()
    
    return render(request, 'admin_panel/business/bumg_form.html', {
        'form': form,
        'bumg': None,
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def bumg_detail(request, bumg_id):
    """BUMG detail view"""
    bumg = get_object_or_404(BUMG, id=bumg_id)
    return render(request, 'admin_panel/business/bumg_detail.html', {
        'bumg': bumg
    })

@login_required
@user_passes_test(is_admin)
def bumg_edit(request, bumg_id):
    """Edit BUMG view"""
    bumg = get_object_or_404(BUMG, id=bumg_id)
    
    if request.method == 'POST':
        form = BUMGForm(request.POST, request.FILES, instance=bumg)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'BUMG berhasil diperbarui!')
                return redirect('admin_panel:bumg_detail', bumg_id=bumg.id)
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = BUMGForm(instance=bumg)
    
    return render(request, 'admin_panel/business/bumg_form.html', {
        'form': form,
        'bumg': bumg,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def bumg_delete(request, bumg_id):
    """Delete BUMG view"""
    bumg = get_object_or_404(BUMG, id=bumg_id)
    if request.method == 'POST':
        bumg.delete()
        messages.success(request, 'BUMG berhasil dihapus!')
        return redirect('admin_panel:bumg_list')
    return render(request, 'admin_panel/business/bumg_delete_confirm.html', {
        'bumg': bumg
    })

# Layanan Jasa Views
@login_required
@user_passes_test(is_admin)
def admin_layanan_jasa_list(request):
    """Admin Layanan Jasa list view"""
    search = request.GET.get('search', '')
    layanan_list = LayananJasa.objects.all().order_by('-created_at')
    
    if search:
        layanan_list = layanan_list.filter(
            Q(nama__icontains=search) |
            Q(penyedia__icontains=search) |
            Q(kategori__icontains=search)
        )
    
    paginator = Paginator(layanan_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/layanan_jasa.html', {
        'page_obj': page_obj,
        'search': search
    })

@login_required
@user_passes_test(is_admin)
def layanan_jasa_create(request):
    """Create Layanan Jasa view"""
    if request.method == 'POST':
        form = LayananJasaForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Layanan Jasa berhasil ditambahkan!')
                return redirect('admin_panel:layanan_jasa_list')
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = LayananJasaForm()
    
    return render(request, 'admin_panel/business/layanan_jasa_form.html', {
        'form': form,
        'layanan': None,
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def layanan_jasa_detail(request, layanan_id):
    """Layanan Jasa detail view"""
    layanan = get_object_or_404(LayananJasa, id=layanan_id)
    return render(request, 'admin_panel/business/layanan_jasa_detail.html', {
        'layanan': layanan
    })

@login_required
@user_passes_test(is_admin)
def layanan_jasa_edit(request, layanan_id):
    """Edit Layanan Jasa view"""
    layanan = get_object_or_404(LayananJasa, id=layanan_id)
    
    if request.method == 'POST':
        form = LayananJasaForm(request.POST, request.FILES, instance=layanan)
        if form.is_valid():
            try:
                form.save()
                messages.success(request, 'Layanan Jasa berhasil diperbarui!')
                return redirect('admin_panel:layanan_jasa_detail', layanan_id=layanan.id)
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Form tidak valid. Silakan periksa kembali input Anda.')
    else:
        form = LayananJasaForm(instance=layanan)
    
    return render(request, 'admin_panel/business/layanan_jasa_form.html', {
        'form': form,
        'layanan': layanan,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def layanan_jasa_delete(request, layanan_id):
    """Delete Layanan Jasa view"""
    layanan = get_object_or_404(LayananJasa, id=layanan_id)
    if request.method == 'POST':
        layanan.delete()
        messages.success(request, 'Layanan Jasa berhasil dihapus!')
        return redirect('admin_panel:layanan_jasa_list')
    return render(request, 'admin_panel/business/layanan_jasa_delete_confirm.html', {
        'layanan': layanan
    })

# Business Categories Views
@login_required
@user_passes_test(is_admin)
def business_categories_list(request):
    """Business Categories list view"""
    categories = BusinessCategory.objects.all().order_by('name')
    return render(request, 'admin_panel/business/categories.html', {
        'categories': categories
    })

@login_required
@user_passes_test(is_admin)
def business_category_create(request):
    """Create Business Category view"""
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        
        try:
            BusinessCategory.objects.create(
                name=name,
                description=description,
                is_active=is_active
            )
            messages.success(request, 'Kategori berhasil ditambahkan!')
            return redirect('admin_panel:business_categories_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin_panel/business/category_form.html', {
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def business_category_detail(request, category_id):
    """Business Category detail view"""
    category = get_object_or_404(BusinessCategory, id=category_id)
    return render(request, 'admin_panel/business/category_detail.html', {
        'category': category
    })

@login_required
@user_passes_test(is_admin)
def business_category_edit(request, category_id):
    """Edit Business Category view"""
    category = get_object_or_404(BusinessCategory, id=category_id)
    
    if request.method == 'POST':
        category.name = request.POST.get('name')
        category.description = request.POST.get('description')
        category.is_active = request.POST.get('is_active') == 'on'
        
        try:
            category.save()
            messages.success(request, 'Kategori berhasil diperbarui!')
            return redirect('admin_panel:business_category_detail', category_id=category.id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin_panel/business/category_form.html', {
        'category': category,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def business_category_delete(request, category_id):
    """Delete Business Category view"""
    category = get_object_or_404(BusinessCategory, id=category_id)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Kategori berhasil dihapus!')
        return redirect('admin_panel:business_categories_list')
    return render(request, 'admin_panel/business/category_delete_confirm.html', {
        'category': category
    })

# Business Dashboard
@login_required
@user_passes_test(is_admin)
def business_dashboard(request):
    """Business dashboard view"""
    stats = get_business_statistics()
    
    # Get recent data
    recent_ukm = UKM.objects.filter(status='aktif').order_by('-created_at')[:5]
    
    # Monthly statistics
    now = timezone.now()
    monthly_registrations = UKM.objects.filter(created_at__month=now.month, created_at__year=now.year).count()
    monthly_approvals = UKM.objects.filter(status='aktif', updated_at__month=now.month, updated_at__year=now.year).count()
    
    return render(request, 'admin_panel/business/dashboard.html', {
        'total_umkm': stats['total_umkm'],
        'total_koperasi': stats['total_koperasi'],
        'total_bumg': stats['total_bumg'],
        'total_layanan': stats['total_layanan'],
        'active_ukm': stats['total_umkm'],
        'active_koperasi': stats['total_koperasi'],
        'active_bumg': stats['total_bumg'],
        'active_layanan': stats['total_layanan'],
        'total_businesses': stats['total_businesses'],
        'approved_businesses': stats['total_businesses'],
        'pending_businesses': stats['pending_approvals'],
        'total_employees': 0,  # Calculate from all businesses
        'recent_ukm': recent_ukm,
        'monthly_registrations': monthly_registrations,
        'monthly_approvals': monthly_approvals,
        'recent_registrations': UKM.objects.filter(created_at__gte=now - timedelta(days=7)).count(),
        'total_categories': BusinessCategory.objects.count()
    })

# Public Business Registration Views
def business_register(request):
    """Public business registration form"""
    from .forms import BusinessRegistrationForm
    
    if request.method == 'POST':
        form = BusinessRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                registration = form.save(commit=False)
                registration.status = 'pending'
                registration.save()
                
                # Handle multiple images if any
                images = request.FILES.getlist('images')
                for image in images:
                    from .models import BusinessRegistrationImage
                    BusinessRegistrationImage.objects.create(
                        registration=registration,
                        image=image,
                        is_primary=False
                    )
                
                messages.success(request, 'Pendaftaran bisnis berhasil dikirim! Tim kami akan menghubungi Anda dalam 1-2 hari kerja.')
                return redirect('business:business_register_success', registration_id=registration.id)
            except Exception as e:
                messages.error(request, f'Terjadi kesalahan saat menyimpan data: {str(e)}')
        else:
            # Display form errors
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{form.fields[field].label}: {error}')
    else:
        form = BusinessRegistrationForm()
    
    return render(request, 'public/business/business_register.html', {
        'form': form
    })

def business_register_success(request, registration_id):
    """Success page after business registration"""
    from .models import BusinessRegistration
    registration = get_object_or_404(BusinessRegistration, id=registration_id)
    
    return render(request, 'public/business/business_register_success.html', {
        'registration': registration
    })

# Removed business_detail_public - using specific views for each business type

def business_list_public(request):
    """Public business list view - shows all approved businesses"""
    search_query = request.GET.get('search', '')
    business_type = request.GET.get('type', '')
    category_id = request.GET.get('category', '')
    
    # Get all approved businesses from all models
    businesses = []
    
    # Get UMKM
    umkm_list = UKM.objects.filter(status='aktif')
    for umkm in umkm_list:
        businesses.append({
            'id': umkm.id,
            'name': umkm.nama_usaha,
            'description': umkm.keterangan,
            'phone': umkm.telepon,
            'email': umkm.email,
            'address': umkm.alamat_usaha,
            'business_type': 'UMKM',
            'business_type_display': 'UMKM',
            'category': None,
            'image': umkm.foto_usaha,
            'logo': umkm.logo_usaha,
            'status': 'approved',
            'created_at': umkm.created_at,
            'updated_at': umkm.updated_at,
            'url_name': 'umkm_detail'
        })
    
    # Get Koperasi
    koperasi_list = Koperasi.objects.filter(status='aktif')
    for koperasi in koperasi_list:
        businesses.append({
            'id': koperasi.id,
            'name': koperasi.nama,
            'description': koperasi.keterangan,
            'phone': koperasi.telepon,
            'email': koperasi.email,
            'address': koperasi.alamat,
            'business_type': 'Koperasi',
            'business_type_display': 'Koperasi',
            'category': None,
            'image': koperasi.foto_koperasi,
            'logo': koperasi.logo_koperasi,
            'status': 'approved',
            'created_at': koperasi.created_at,
            'updated_at': koperasi.updated_at,
            'url_name': 'koperasi_detail'
        })
    
    # Get BUMG
    bumg_list = BUMG.objects.filter(status='aktif')
    for bumg in bumg_list:
        businesses.append({
            'id': bumg.id,
            'name': bumg.nama,
            'description': bumg.bidang_usaha,
            'phone': bumg.telepon,
            'email': bumg.email,
            'address': bumg.alamat,
            'business_type': 'BUMG',
            'business_type_display': 'BUMG',
            'category': None,
            'image': bumg.foto_bumg,
            'logo': bumg.logo_bumg,
            'status': 'approved',
            'created_at': bumg.created_at,
            'updated_at': bumg.updated_at,
            'url_name': 'bumg_detail'
        })
    
    # Get Layanan Jasa
    layanan_list = LayananJasa.objects.filter(status='aktif')
    for layanan in layanan_list:
        businesses.append({
            'id': layanan.id,
            'name': layanan.nama,
            'description': layanan.deskripsi,
            'phone': layanan.telepon,
            'email': layanan.email,
            'address': layanan.alamat,
            'business_type': 'Layanan Jasa',
            'business_type_display': 'Layanan Jasa',
            'category': None,
            'image': layanan.foto_layanan,
            'logo': layanan.logo_layanan,
            'status': 'approved',
            'created_at': layanan.created_at,
            'updated_at': layanan.updated_at,
            'url_name': 'layanan_jasa_detail'
        })
    
    # Apply filters
    if search_query:
        businesses = [b for b in businesses if search_query.lower() in b['name'].lower() or 
                     (b['description'] and search_query.lower() in b['description'].lower())]
    
    if business_type:
        businesses = [b for b in businesses if b['business_type'].lower() == business_type.lower()]
    
    if category_id:
        businesses = [b for b in businesses if b['category'] and str(b['category'].id) == category_id]
    
    # Sort by created_at
    businesses.sort(key=lambda x: x['created_at'], reverse=True)
    
    # Pagination
    paginator = Paginator(businesses, 12)
    page_number = request.GET.get('page')
    business_list = paginator.get_page(page_number)
    
    # Get categories for filter
    categories = BusinessCategory.objects.all()
    
    return render(request, 'public/business/business_list.html', {
        'business_list': business_list,
        'search_query': search_query,
        'business_type': business_type,
        'category_id': category_id,
        'categories': categories,
        'is_paginated': paginator.num_pages > 1
    })
