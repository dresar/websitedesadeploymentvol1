"""
Hero Image Management Views for Admin Panel - Simplified
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.db.models import Q

from core.models import HeroImage


@login_required
def hero_images_dashboard(request):
    """Dashboard sederhana untuk Hero Images"""
    stats = {
        'total_images': HeroImage.objects.count(),
        'active_images': HeroImage.objects.filter(is_active=True).count(),
        'inactive_images': HeroImage.objects.filter(is_active=False).count(),
    }
    
    recent_images = HeroImage.objects.all()[:5]
    
    context = {
        'stats': stats,
        'recent_images': recent_images,
    }
    return render(request, 'admin_panel/hero_images/dashboard.html', context)


@login_required
def hero_images_list(request):
    """Daftar semua hero images"""
    search = request.GET.get('search', '')
    page_filter = request.GET.get('page', '')
    status_filter = request.GET.get('status', '')
    
    images = HeroImage.objects.all()
    
    if search:
        images = images.filter(Q(name__icontains=search))
    
    if page_filter:
        images = images.filter(page=page_filter)
    
    if status_filter:
        if status_filter == 'active':
            images = images.filter(is_active=True)
        elif status_filter == 'inactive':
            images = images.filter(is_active=False)
    
    # Tidak menggunakan pagination - tampilkan semua
    context = {
        'hero_images': images,
        'search': search,
        'page_filter': page_filter,
        'status_filter': status_filter,
        'page_choices': HeroImage.PAGE_CHOICES,
        # Menu context untuk sidebar
        'active_menu': 'hero_images',
        'active_submenu': 'list',
    }
    return render(request, 'admin_panel/hero_images/list.html', context)


@login_required
def hero_image_create(request):
    """Tambah hero image baru"""
    if request.method == 'POST':
        name = request.POST.get('name')
        page = request.POST.get('page')
        image = request.FILES.get('image')
        is_active = request.POST.get('is_active') == 'on'
        
        # Check if page already has hero image
        if HeroImage.objects.filter(page=page, is_active=True).exists():
            messages.error(request, f'Halaman "{page}" sudah memiliki hero image!')
            return redirect('admin_panel:hero_images:hero_image_create')
        
        # Validate file size (1MB limit)
        if image and image.size > 1024 * 1024:  # 1MB in bytes
            messages.error(request, f'File terlalu besar! Maksimal 1MB. Ukuran file Anda: {image.size / (1024*1024):.2f}MB')
            return redirect('admin_panel:hero_images:hero_image_create')
        
        # Validate file format
        if image:
            allowed_formats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if image.content_type not in allowed_formats:
                messages.error(request, 'Format file tidak didukung! Gunakan JPG, PNG, atau WebP.')
                return redirect('admin_panel:hero_images:hero_image_create')
        
        if name and page and image:
            HeroImage.objects.create(
                name=name,
                page=page,
                image=image,
                is_active=is_active
            )
            messages.success(request, 'Hero image berhasil ditambahkan!')
            return redirect('admin_panel:hero_images:hero_images_list')
        else:
            messages.error(request, 'Semua field harus diisi!')
    
    # Get available pages (pages that don't have hero images yet)
    existing_pages = HeroImage.objects.filter(is_active=True).values_list('page', flat=True)
    all_page_choices = HeroImage.PAGE_CHOICES
    available_pages = [(value, display) for value, display in all_page_choices if value not in existing_pages]
    
    context = {
        'page_choices': HeroImage.PAGE_CHOICES,
        'available_pages': available_pages,
        # Menu context untuk sidebar
        'active_menu': 'hero_images',
        'active_submenu': 'add',
    }
    return render(request, 'admin_panel/hero_images/form.html', context)


@login_required
def hero_image_edit(request, pk):
    """Edit hero image"""
    hero_image = get_object_or_404(HeroImage, pk=pk)
    
    if request.method == 'POST':
        new_page = request.POST.get('page', hero_image.page)
        
        # Check if new page already has hero image (excluding current image)
        if new_page != hero_image.page and HeroImage.objects.filter(page=new_page, is_active=True).exclude(id=hero_image.id).exists():
            messages.error(request, f'Halaman "{new_page}" sudah memiliki hero image!')
            return redirect('admin_panel:hero_images:hero_image_edit', pk=hero_image.id)
        
        hero_image.name = request.POST.get('name', hero_image.name)
        hero_image.page = new_page
        hero_image.is_active = request.POST.get('is_active') == 'on'
        
        if 'image' in request.FILES:
            new_image = request.FILES['image']
            
            # Validate file size (1MB limit)
            if new_image.size > 1024 * 1024:  # 1MB in bytes
                messages.error(request, f'File terlalu besar! Maksimal 1MB. Ukuran file Anda: {new_image.size / (1024*1024):.2f}MB')
                return redirect('admin_panel:hero_images:hero_image_edit', pk=hero_image.id)
            
            # Validate file format
            allowed_formats = ['image/jpeg', 'image/jpg', 'image/png', 'image/webp']
            if new_image.content_type not in allowed_formats:
                messages.error(request, 'Format file tidak didukung! Gunakan JPG, PNG, atau WebP.')
                return redirect('admin_panel:hero_images:hero_image_edit', pk=hero_image.id)
            
            hero_image.image = new_image
        
        hero_image.save()
        messages.success(request, 'Hero image berhasil diupdate!')
        return redirect('admin_panel:hero_images:hero_images_list')
    
    # Get available pages (pages that don't have hero images yet, plus current page)
    existing_pages = HeroImage.objects.filter(is_active=True).exclude(id=hero_image.id).values_list('page', flat=True)
    all_page_choices = HeroImage.PAGE_CHOICES
    available_pages = [(value, display) for value, display in all_page_choices if value not in existing_pages]
    
    context = {
        'image': hero_image,
        'page_choices': all_page_choices,
        'available_pages': available_pages,
    }
    return render(request, 'admin_panel/hero_images/form.html', context)


@login_required
def hero_image_delete(request, pk):
    """Hapus hero image"""
    if request.method == 'POST':
        hero_image = get_object_or_404(HeroImage, pk=pk)
        hero_image.delete()
        return JsonResponse({'success': True, 'message': 'Hero image berhasil dihapus!'})
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'})


@login_required
def check_page_exists(request):
    """API endpoint to check if page already has hero image"""
    page = request.GET.get('page')
    exclude_id = request.GET.get('exclude_id')
    
    if not page:
        return JsonResponse({'exists': False})
    
    queryset = HeroImage.objects.filter(page=page, is_active=True)
    if exclude_id:
        queryset = queryset.exclude(id=exclude_id)
    
    exists = queryset.exists()
    return JsonResponse({'exists': exists})