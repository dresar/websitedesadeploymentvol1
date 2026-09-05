from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, FileResponse, Http404
from django.db.models import Q, Count
from django.core.paginator import Paginator
from django.utils import timezone
from .models import Document, DocumentCategory, DocumentComment, DocumentDownloadLog
from .forms import DocumentForm, DocumentCategoryForm
import os

def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.is_superuser)


# ===================== ADMIN VIEWS =====================

@login_required
@user_passes_test(is_admin)
def documents_dashboard(request):
    """Dashboard Dokumen Admin"""
    # Statistics
    total_documents = Document.objects.count()
    approved_documents = Document.objects.filter(status='published').count()
    submitted_documents = Document.objects.filter(status='review').count()
    completed_documents = Document.objects.filter(status='published', is_public=True).count()
    
    # Recent documents
    recent_documents = Document.objects.select_related('category', 'uploaded_by').order_by('-created_at')[:10]
    
    # Category statistics
    category_stats = {}
    for cat in DocumentCategory.objects.filter(is_active=True):
        count = Document.objects.filter(category=cat).count()
        if count > 0:
            category_stats[cat.name] = count
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'documents_dashboard',
        'total_documents': total_documents,
        'approved_documents': approved_documents,
        'submitted_documents': submitted_documents,
        'completed_documents': completed_documents,
        'recent_documents': recent_documents,
        'category_stats': category_stats,
    }
    
    return render(request, 'admin_panel/documents/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def documents_list(request):
    """List Dokumen Admin dengan Filter & Search"""
    documents = Document.objects.select_related('category', 'uploaded_by').all()
    
    # Search
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(document_number__icontains=search) |
            Q(tags__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Filter by category
    category_id = request.GET.get('category', '')
    if category_id:
        documents = documents.filter(category_id=category_id)
    
    # Filter by status
    status = request.GET.get('status', '')
    if status:
        documents = documents.filter(status=status)
    
    # Filter by year
    year = request.GET.get('year', '')
    if year:
        documents = documents.filter(document_year=year)
    
    # Sorting
    sort_by = request.GET.get('sort', '-created_at')
    documents = documents.order_by(sort_by)
    
    # Pagination
    paginator = Paginator(documents, 20)
    page = request.GET.get('page', 1)
    documents_page = paginator.get_page(page)
    
    # Get filter options
    categories = DocumentCategory.objects.filter(is_active=True)
    years = Document.objects.values_list('document_year', flat=True).distinct().order_by('-document_year')
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'documents_list',
        'documents': documents_page,
        'categories': categories,
        'years': years,
        'search': search,
        'selected_category': category_id,
        'selected_status': status,
        'selected_year': year,
    }
    
    return render(request, 'admin_panel/documents/list.html', context)


@login_required
@user_passes_test(is_admin)
def document_detail(request, pk):
    """Detail Dokumen Admin"""
    document = get_object_or_404(Document.objects.select_related('category', 'uploaded_by'), pk=pk)
    comments = document.comments.all()[:10]
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'document_detail',
        'document': document,
        'comments': comments,
    }
    
    return render(request, 'admin_panel/documents/detail.html', context)


@login_required
@user_passes_test(is_admin)
def document_create(request):
    """Create Dokumen Admin"""
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                document = form.save(commit=False)
                document.uploaded_by = request.user
                document.save()
                
                messages.success(request, f'Dokumen "{document.title}" berhasil ditambahkan!')
                return redirect('admin_panel:document_detail', pk=document.pk)
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DocumentForm()
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'document_create',
        'form': form,
    }
    
    return render(request, 'admin_panel/documents/form.html', context)


@login_required
@user_passes_test(is_admin)
def document_edit(request, pk):
    """Edit Dokumen Admin"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            try:
                document = form.save()
                messages.success(request, f'Dokumen "{document.title}" berhasil diupdate!')
                return redirect('admin_panel:document_detail', pk=document.pk)
                
            except Exception as e:
                messages.error(request, f'Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DocumentForm(instance=document)
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'documents_list',
        'form': form,
        'document': document,
    }
    
    return render(request, 'admin_panel/documents/form.html', context)


@login_required
@user_passes_test(is_admin)
def document_delete(request, pk):
    """Delete Dokumen Admin"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        try:
            title = document.title
            document.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Dokumen "{title}" berhasil dihapus!'})
            
            messages.success(request, f'Dokumen "{title}" berhasil dihapus!')
            return redirect('admin_panel:documents_list')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
            
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:document_detail', pk=pk)
    
    return redirect('admin_panel:document_detail', pk=pk)


@login_required
@user_passes_test(is_admin)
def document_categories_list(request):
    """List Kategori Dokumen"""
    categories = DocumentCategory.objects.all().annotate(
        doc_count=Count('documents')
    )
    
    context = {
        'active_menu': 'documents',
        'active_submenu': 'document_categories',
        'categories': categories,
    }
    
    return render(request, 'admin_panel/documents/categories.html', context)


@login_required
@user_passes_test(is_admin)
def document_category_create(request):
    """Create Kategori"""
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST)
        if form.is_valid():
            try:
                category = form.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f'Kategori "{category.name}" berhasil ditambahkan!'})
                
                messages.success(request, f'Kategori "{category.name}" berhasil ditambahkan!')
                return redirect('admin_panel:document_categories_list')
                
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
                
                messages.error(request, f'Error: {str(e)}')
        else:
            # Handle validation errors
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                errors = {field: [str(e) for e in errors] for field, errors in form.errors.items()}
                return JsonResponse({'success': False, 'message': 'Data tidak valid', 'errors': errors})
            
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    
    return redirect('admin_panel:document_categories_list')


@login_required
@user_passes_test(is_admin)
def document_category_edit(request, pk):
    """Edit Kategori"""
    category = get_object_or_404(DocumentCategory, pk=pk)
    
    if request.method == 'POST':
        form = DocumentCategoryForm(request.POST, instance=category)
        if form.is_valid():
            try:
                category = form.save()
                
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': True, 'message': f'Kategori "{category.name}" berhasil diupdate!'})
                
                messages.success(request, f'Kategori "{category.name}" berhasil diupdate!')
                return redirect('admin_panel:document_categories_list')
                
            except Exception as e:
                if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                    return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
                
                messages.error(request, f'Error: {str(e)}')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'{field}: {error}')
    else:
        form = DocumentCategoryForm(instance=category)
    
    context = {
        'form': form,
        'category': category,
    }
    
    return render(request, 'admin_panel/documents/category_form.html', context)


@login_required
@user_passes_test(is_admin)
def document_category_delete(request, pk):
    """Delete Kategori"""
    category = get_object_or_404(DocumentCategory, pk=pk)
    
    if request.method == 'POST':
        try:
            name = category.name
            category.delete()
            
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': f'Kategori "{name}" berhasil dihapus!'})
            
            messages.success(request, f'Kategori "{name}" berhasil dihapus!')
            
        except Exception as e:
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
            
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('admin_panel:document_categories_list')


@login_required
@user_passes_test(is_admin)
def document_comment_add(request, pk):
    """Add Comment to Document (Admin)"""
    document = get_object_or_404(Document, pk=pk)
    
    if request.method == 'POST':
        try:
            name = request.POST.get('name')
            email = request.POST.get('email')
            comment = request.POST.get('comment')
            
            DocumentComment.objects.create(
                document=document,
                name=name,
                email=email,
                comment=comment,
                is_approved=True  # Auto approve admin comments
            )
            
            messages.success(request, 'Komentar berhasil ditambahkan!')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return redirect('admin_panel:document_detail', pk=pk)


@login_required
@user_passes_test(is_admin)
def document_preview(request, pk):
    """Preview Document"""
    document = get_object_or_404(Document, pk=pk)
    
    context = {
        'document': document,
    }
    
    return render(request, 'admin_panel/documents/preview.html', context)


@login_required
@user_passes_test(is_admin)
def api_documents_stats(request):
    """API untuk statistik dokumen"""
    stats = {
        'total': Document.objects.count(),
        'published': Document.objects.filter(status='published').count(),
        'draft': Document.objects.filter(status='draft').count(),
        'review': Document.objects.filter(status='review').count(),
    }
    
    return JsonResponse({'success': True, 'stats': stats})


# ===================== PUBLIC VIEWS =====================

def public_documents_list(request):
    """List Dokumen Public"""
    documents = Document.objects.filter(
        status='published',
        is_public=True
    ).select_related('category')
    
    # Search
    search = request.GET.get('search', '')
    if search:
        documents = documents.filter(
            Q(title__icontains=search) |
            Q(document_number__icontains=search) |
            Q(tags__icontains=search) |
            Q(summary__icontains=search)
        )
    
    # Filter by category type
    category_type = request.GET.get('type', '')
    if category_type:
        documents = documents.filter(category__category_type=category_type)
    
    # Filter by year
    year = request.GET.get('year', '')
    if year:
        documents = documents.filter(document_year=year)
    
    # Sorting
    documents = documents.order_by('-document_year', '-created_at')
    
    # Pagination
    paginator = Paginator(documents, 12)
    page = request.GET.get('page', 1)
    documents_page = paginator.get_page(page)
    
    # Get filter options
    years = Document.objects.filter(status='published', is_public=True).values_list('document_year', flat=True).distinct().order_by('-document_year')
    categories = DocumentCategory.objects.filter(is_active=True)
    
    context = {
        'documents': documents_page,
        'years': years,
        'categories': categories,
        'search': search,
        'selected_type': category_type,
        'selected_year': year,
    }
    
    return render(request, 'public/documents/list.html', context)


def public_document_detail(request, slug):
    """Detail Dokumen Public"""
    document = get_object_or_404(
        Document.objects.select_related('category', 'uploaded_by'),
        slug=slug,
        status='published',
        is_public=True
    )
    
    # Increment view count
    document.view_count += 1
    document.save(update_fields=['view_count'])
    
    # Get related documents
    related_documents = Document.objects.filter(
        category=document.category,
        status='published',
        is_public=True
    ).exclude(pk=document.pk)[:5]
    
    context = {
        'document': document,
        'related_documents': related_documents,
    }
    
    return render(request, 'public/documents/detail.html', context)


def public_document_download(request, slug):
    """Download Dokumen Public"""
    document = get_object_or_404(
        Document,
        slug=slug,
        status='published',
        is_public=True
    )
    
    # Check if file exists and is valid
    if not document.file or not document.file.name:
        raise Http404("File tidak ditemukan atau tidak tersedia")
    
    # Check if file exists on disk
    try:
        if not os.path.exists(document.file.path):
            raise Http404("File tidak ditemukan di server")
    except ValueError:
        # This happens when the file field is empty or invalid
        raise Http404("File tidak valid atau tidak tersedia")
    
    # Increment download count
    document.download_count += 1
    document.save(update_fields=['download_count'])
    
    # Log download
    try:
        ip_address = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR', ''))
        if ',' in ip_address:
            ip_address = ip_address.split(',')[0].strip()
        
        DocumentDownloadLog.objects.create(
            document=document,
            ip_address=ip_address,
            user_agent=request.META.get('HTTP_USER_AGENT', '')
        )
    except:
        pass
    
    # Serve file
    try:
        response = FileResponse(open(document.file.path, 'rb'))
        response['Content-Disposition'] = f'attachment; filename="{os.path.basename(document.file.name)}"'
        return response
    except (OSError, IOError) as e:
        raise Http404(f"File tidak dapat dibuka: {str(e)}")


def public_transparansi_anggaran(request):
    """Halaman Transparansi Anggaran (APBDES, Realisasi, Dana Desa)"""
    documents = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['apbdes', 'realisasi_anggaran', 'dana_desa']
    ).select_related('category').order_by('-document_year', '-created_at')
    
    # Filter by year
    year = request.GET.get('year', '')
    if year:
        documents = documents.filter(document_year=year)
    
    # Get years
    years = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['apbdes', 'realisasi_anggaran', 'dana_desa']
    ).values_list('document_year', flat=True).distinct().order_by('-document_year')
    
    context = {
        'documents': documents,
        'years': years,
        'selected_year': year,
    }
    
    return render(request, 'public/documents/transparansi_anggaran.html', context)


def public_produk_hukum(request):
    """Halaman Produk Hukum Desa (Perdes, Perkades, SK)"""
    documents = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['perdes', 'perkades', 'sk_kades']
    ).select_related('category').order_by('-document_year', '-created_at')
    
    # Filter by type
    doc_type = request.GET.get('type', '')
    if doc_type:
        documents = documents.filter(category__category_type=doc_type)
    
    # Filter by year
    year = request.GET.get('year', '')
    if year:
        documents = documents.filter(document_year=year)
    
    # Get years
    years = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['perdes', 'perkades', 'sk_kades']
    ).values_list('document_year', flat=True).distinct().order_by('-document_year')
    
    context = {
        'documents': documents,
        'years': years,
        'selected_type': doc_type,
        'selected_year': year,
    }
    
    return render(request, 'public/documents/produk_hukum.html', context)


def public_profil_desa(request):
    """Halaman Profil & Data Desa"""
    documents = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['profil_desa', 'data_kependudukan', 'peta_desa']
    ).select_related('category').order_by('-document_year', '-created_at')
    
    context = {
        'documents': documents,
    }
    
    return render(request, 'public/documents/profil_desa.html', context)


def public_laporan(request):
    """Halaman Laporan Desa (LPPD, Musdes)"""
    documents = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['lppd', 'musdes', 'laporan_lainnya']
    ).select_related('category').order_by('-document_year', '-created_at')
    
    # Filter by year
    year = request.GET.get('year', '')
    if year:
        documents = documents.filter(document_year=year)
    
    # Get years
    years = Document.objects.filter(
        status='published',
        is_public=True,
        category__category_type__in=['lppd', 'musdes', 'laporan_lainnya']
    ).values_list('document_year', flat=True).distinct().order_by('-document_year')
    
    context = {
        'documents': documents,
        'years': years,
        'selected_year': year,
    }
    
    return render(request, 'public/documents/laporan.html', context)

