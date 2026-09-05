from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Sum
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import datetime, timedelta

from .models import (
    Business, BusinessCategory, BusinessOwner, BusinessProduct, 
    BusinessFinance, UKM, Koperasi, BUMG, Aset, LayananJasa, BusinessPageHeader,
    JenisKoperasi, BusinessRegistration, BusinessRegistrationImage
)
from .forms import UKMForm, KoperasiForm, BUMGForm, LayananJasaForm, BusinessForm

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
        'active_menu': 'business',
        'active_submenu': 'business_dashboard',
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

# UMKM Admin Views
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
        'active_menu': 'business',
        'active_submenu': 'umkm',
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
        logger.info('=== UMKM Create Debug (admin_views) ===')
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
                ukm = form.save()
                logger.info(f'UMKM created successfully: {ukm.id}')
                
                # Debug: Check if files were saved
                if ukm.foto_usaha:
                    logger.info(f'Foto usaha saved: {ukm.foto_usaha.url}')
                if ukm.logo_usaha:
                    logger.info(f'Logo usaha saved: {ukm.logo_usaha.url}')
                
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
        'active_menu': 'business',
        'active_submenu': 'umkm_add',
        'form': form,
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
        logger.info(f'=== UMKM Edit Debug (admin_views) - ID: {umkm_id} ===')
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
                return redirect('admin_panel:umkm_detail', umkm_id=ukm.id)
            except Exception as e:
                logger.error(f'Error saving UMKM {umkm_id}: {str(e)}')
                logger.error(f'Error type: {type(e).__name__}')
                import traceback
                logger.error(f'Traceback: {traceback.format_exc()}')
                messages.error(request, f'Error: {str(e)}')
        else:
            logger.error('Form is not valid')
            logger.error(f'Form errors: {form.errors}')
            messages.error(request, 'Form tidak valid. Silakan periksa kembali.')
    else:
        form = UKMForm(instance=ukm)
    
    return render(request, 'admin_panel/business/umkm_form.html', {
        'form': form,
        'umkm': ukm,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def umkm_delete(request, umkm_id):
    """Delete UMKM view - AJAX only"""
    if request.method == 'POST':
        try:
            ukm = get_object_or_404(UKM, id=umkm_id)
            nama_usaha = ukm.nama_usaha
            ukm.delete()
            return JsonResponse({
                'success': True,
                'message': f'UMKM "{nama_usaha}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus UMKM: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Koperasi Admin Views
@login_required
@user_passes_test(is_admin)
def koperasi_list(request):
    """Admin Koperasi list view"""
    search = request.GET.get('search', '')
    koperasi_list = Koperasi.objects.all().order_by('-created_at')
    
    if search:
        koperasi_list = koperasi_list.filter(
            Q(nama_koperasi__icontains=search) |
            Q(ketua__icontains=search) |
            Q(sekretaris__icontains=search)
        )
    
    paginator = Paginator(koperasi_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/koperasi_admin.html', {
        'active_menu': 'business',
        'active_submenu': 'koperasi',
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
        'active_menu': 'business',
        'active_submenu': 'koperasi_add',
        'form': form,
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
    """Delete Koperasi view - AJAX only"""
    if request.method == 'POST':
        try:
            koperasi = get_object_or_404(Koperasi, id=koperasi_id)
            nama = koperasi.nama
            koperasi.delete()
            return JsonResponse({
                'success': True,
                'message': f'Koperasi "{nama}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus Koperasi: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# BUMG Admin Views
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
        'active_menu': 'business',
        'active_submenu': 'bumg',
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
        'active_menu': 'business',
        'active_submenu': 'bumg_add',
        'form': form,
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
    """Delete BUMG view - AJAX only"""
    if request.method == 'POST':
        try:
            bumg = get_object_or_404(BUMG, id=bumg_id)
            nama = bumg.nama
            bumg.delete()
            return JsonResponse({
                'success': True,
                'message': f'BUMG "{nama}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus BUMG: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Layanan Jasa Admin Views
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
        'active_menu': 'business',
        'active_submenu': 'layanan_jasa',
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
        'active_menu': 'business',
        'active_submenu': 'layanan_jasa_add',
        'form': form,
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
    """Delete Layanan Jasa view - AJAX only"""
    if request.method == 'POST':
        try:
            layanan = get_object_or_404(LayananJasa, id=layanan_id)
            nama = layanan.nama
            layanan.delete()
            return JsonResponse({
                'success': True,
                'message': f'Layanan Jasa "{nama}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus Layanan Jasa: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Business Categories Admin Views
@login_required
@user_passes_test(is_admin)
def business_categories_list(request):
    """Business Categories list view"""
    categories = BusinessCategory.objects.all().order_by('name')
    return render(request, 'admin_panel/business/categories.html', {
        'active_menu': 'business',
        'active_submenu': 'categories',
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
        
        if name:
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
        else:
            messages.error(request, 'Nama kategori harus diisi!')
    
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
        name = request.POST.get('name')
        description = request.POST.get('description')
        is_active = request.POST.get('is_active') == 'on'
        
        if name:
            try:
                category.name = name
                category.description = description
                category.is_active = is_active
                category.save()
                messages.success(request, 'Kategori berhasil diperbarui!')
                return redirect('admin_panel:business_category_detail', category_id=category.id)
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            messages.error(request, 'Nama kategori harus diisi!')
    
    return render(request, 'admin_panel/business/category_form.html', {
        'category': category,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def business_category_delete(request, category_id):
    """Delete Business Category view - AJAX only"""
    if request.method == 'POST':
        try:
            category = get_object_or_404(BusinessCategory, id=category_id)
            name = category.name
            category.delete()
            return JsonResponse({
                'success': True,
                'message': f'Kategori "{name}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus kategori: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Business Admin Views
@login_required
@user_passes_test(is_admin)
def business_list_admin(request):
    """Admin Business list view"""
    search = request.GET.get('search', '')
    business_list = Business.objects.all().order_by('-created_at')
    
    if search:
        business_list = business_list.filter(
            Q(name__icontains=search) |
            Q(description__icontains=search) |
            Q(address__icontains=search)
        )
    
    paginator = Paginator(business_list, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'admin_panel/business/business_list.html', {
        'page_obj': page_obj,
        'search': search
    })

@login_required
@user_passes_test(is_admin)
def business_create(request):
    """Create Business view"""
    if request.method == 'POST':
        # Handle form submission
        name = request.POST.get('name')
        business_type = request.POST.get('business_type')
        description = request.POST.get('description')
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        website = request.POST.get('website')
        category_id = request.POST.get('category')
        status = request.POST.get('status', 'pending')
        
        try:
            business = Business.objects.create(
                name=name,
                business_type=business_type,
                description=description,
                address=address,
                phone=phone,
                email=email,
                website=website,
                category_id=category_id,
                status=status
            )
            messages.success(request, 'Bisnis berhasil ditambahkan!')
            return redirect('admin_panel:business_list')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    categories = BusinessCategory.objects.filter(is_active=True)
    return render(request, 'admin_panel/business/business_form.html', {
        'categories': categories,
        'is_edit': False
    })

@login_required
@user_passes_test(is_admin)
def business_detail_admin(request, business_id):
    """Business detail view"""
    business = get_object_or_404(Business, id=business_id)
    return render(request, 'admin_panel/business/business_detail.html', {
        'business': business
    })

@login_required
@user_passes_test(is_admin)
def business_edit(request, business_id):
    """Edit Business view"""
    business = get_object_or_404(Business, id=business_id)
    
    if request.method == 'POST':
        # Handle form submission
        business.name = request.POST.get('name')
        business.business_type = request.POST.get('business_type')
        business.description = request.POST.get('description')
        business.address = request.POST.get('address')
        business.phone = request.POST.get('phone')
        business.email = request.POST.get('email')
        business.website = request.POST.get('website')
        business.category_id = request.POST.get('category')
        business.status = request.POST.get('status')
        
        try:
            business.save()
            messages.success(request, 'Bisnis berhasil diperbarui!')
            return redirect('admin_panel:business_detail', business_id=business.id)
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    categories = BusinessCategory.objects.filter(is_active=True)
    return render(request, 'admin_panel/business/business_form.html', {
        'business': business,
        'categories': categories,
        'is_edit': True
    })

@login_required
@user_passes_test(is_admin)
def business_delete(request, business_id):
    """Delete Business view - AJAX only"""
    if request.method == 'POST':
        try:
            business = get_object_or_404(Business, id=business_id)
            name = business.name
            business.delete()
            return JsonResponse({
                'success': True,
                'message': f'Bisnis "{name}" berhasil dihapus!'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Gagal menghapus bisnis: {str(e)}'
            }, status=400)
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Business Registration Admin Views
@login_required
@user_passes_test(is_admin)
def business_registration_list(request):
    """Admin Business Registration list view"""
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    type_filter = request.GET.get('type', '')
    
    registrations = BusinessRegistration.objects.all().order_by('-created_at')
    
    if search:
        registrations = registrations.filter(
            Q(business_name__icontains=search) |
            Q(owner_name__icontains=search) |
            Q(owner_nik__icontains=search) |
            Q(owner_email__icontains=search)
        )
    
    if status_filter:
        registrations = registrations.filter(status=status_filter)
    
    if type_filter:
        registrations = registrations.filter(registration_type=type_filter)
    
    paginator = Paginator(registrations, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total': BusinessRegistration.objects.count(),
        'pending': BusinessRegistration.objects.filter(status='pending').count(),
        'approved': BusinessRegistration.objects.filter(status='approved').count(),
        'rejected': BusinessRegistration.objects.filter(status='rejected').count(),
        'under_review': BusinessRegistration.objects.filter(status='under_review').count(),
    }
    
    return render(request, 'admin_panel/business/registration_list.html', {
        'active_menu': 'business',
        'active_submenu': 'business_registrations',
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'type_filter': type_filter,
        'stats': stats
    })

@login_required
@user_passes_test(is_admin)
def business_registration_detail(request, registration_id):
    """Business Registration detail view"""
    registration = get_object_or_404(BusinessRegistration, id=registration_id)
    images = registration.images.all()
    
    return render(request, 'admin_panel/business/registration_detail.html', {
        'active_menu': 'business',
        'active_submenu': 'business_registrations',
        'registration': registration,
        'images': images
    })

@login_required
@user_passes_test(is_admin)
def business_registration_approve(request, registration_id):
    """Approve business registration"""
    if request.method in ['POST', 'GET']:
        try:
            registration = get_object_or_404(BusinessRegistration, id=registration_id)
            admin_notes = request.POST.get('admin_notes', '')
            
            # Update registration status
            registration.status = 'approved'
            registration.approved_by = request.user
            registration.approved_at = timezone.now()
            registration.admin_notes = admin_notes
            registration.save()
            
            # Create corresponding business record based on type
            if registration.registration_type == 'umkm':
                # Create UKM record
                ukm = UKM.objects.create(
                    nama_usaha=registration.business_name,
                    pemilik=registration.owner_name,
                    alamat_usaha=registration.business_address,
                    alamat_pemilik=registration.owner_address,
                    telepon=registration.owner_phone,
                    email=registration.owner_email,
                    jenis_usaha=registration.jenis_usaha or 'Usaha Kecil',
                    skala_usaha=registration.skala_usaha or 'mikro',
                    foto_usaha=registration.business_photo,
                    logo_usaha=registration.business_logo,
                    status='aktif',
                    keterangan=f"Disetujui dari pendaftaran online - {registration.created_at.strftime('%d %B %Y')}"
                )
                
            elif registration.registration_type == 'koperasi':
                # Create Koperasi record
                koperasi = Koperasi.objects.create(
                    nama=registration.business_name,
                    ketua=registration.ketua or registration.owner_name,
                    sekretaris=registration.sekretaris or '',
                    bendahara=registration.bendahara or '',
                    alamat=registration.business_address,
                    telepon=registration.owner_phone,
                    email=registration.owner_email,
                    jumlah_anggota=registration.jumlah_anggota or 0,
                    modal_dasar=registration.modal_dasar or 0,
                    foto_koperasi=registration.business_photo,
                    logo_koperasi=registration.business_logo,
                    status='aktif',
                    keterangan=f"Disetujui dari pendaftaran online - {registration.created_at.strftime('%d %B %Y')}"
                )
                
            elif registration.registration_type == 'bumg':
                # Create BUMG record
                bumg = BUMG.objects.create(
                    nama=registration.business_name,
                    direktur=registration.direktur or registration.owner_name,
                    komisaris=registration.komisaris or '',
                    alamat=registration.business_address,
                    telepon=registration.owner_phone,
                    email=registration.owner_email,
                    jumlah_karyawan=registration.jumlah_karyawan or 0,
                    bidang_usaha=registration.bidang_usaha or registration.business_description,
                    foto_bumg=registration.business_photo,
                    logo_bumg=registration.business_logo,
                    status='aktif',
                    keterangan=f"Disetujui dari pendaftaran online - {registration.created_at.strftime('%d %B %Y')}"
                )
                
            elif registration.registration_type == 'layanan_jasa':
                # Create LayananJasa record
                layanan = LayananJasa.objects.create(
                    nama=registration.business_name,
                    penyedia=registration.penyedia or registration.owner_name,
                    alamat=registration.business_address,
                    telepon=registration.owner_phone,
                    email=registration.owner_email,
                    kategori=registration.kategori_layanan or 'Layanan Umum',
                    deskripsi=registration.business_description,
                    tarif_layanan=registration.tarif_layanan or 0,
                    foto_layanan=registration.business_photo,
                    logo_layanan=registration.business_logo,
                    status='aktif',
                    keterangan=f"Disetujui dari pendaftaran online - {registration.created_at.strftime('%d %B %Y')}"
                )
            
            messages.success(request, f'Pendaftaran {registration.business_name} berhasil disetujui!')
            return redirect('admin_panel:business_registration_detail', registration_id=registration.id)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:business_registration_detail', registration_id=registration_id)
    
    return redirect('admin_panel:business_registration_list')

@login_required
@user_passes_test(is_admin)
def business_registration_reject(request, registration_id):
    """Reject business registration"""
    if request.method in ['POST', 'GET']:
        try:
            registration = get_object_or_404(BusinessRegistration, id=registration_id)
            admin_notes = request.POST.get('admin_notes', '')
            
            registration.status = 'rejected'
            registration.admin_notes = admin_notes
            registration.save()
            
            messages.success(request, f'Pendaftaran {registration.business_name} telah ditolak.')
            return redirect('admin_panel:business_registration_detail', registration_id=registration.id)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:business_registration_detail', registration_id=registration_id)
    
    return redirect('admin_panel:business_registration_list')

@login_required
@user_passes_test(is_admin)
def business_registration_under_review(request, registration_id):
    """Mark business registration as under review"""
    if request.method in ['POST', 'GET']:
        try:
            registration = get_object_or_404(BusinessRegistration, id=registration_id)
            admin_notes = request.POST.get('admin_notes', '')
            
            registration.status = 'under_review'
            registration.admin_notes = admin_notes
            registration.save()
            
            messages.success(request, f'Pendaftaran {registration.business_name} sedang ditinjau.')
            return redirect('admin_panel:business_registration_detail', registration_id=registration.id)
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:business_registration_detail', registration_id=registration_id)
    
    return redirect('admin_panel:business_registration_list')
