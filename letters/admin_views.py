"""
Admin Views untuk Sistem Surat Desa Pulosarok
Views khusus admin panel dengan CRUD lengkap untuk semua model
"""

from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q, Count, Avg, Sum
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from django.urls import reverse
from django.template.loader import render_to_string
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.core.cache import cache
import json
from datetime import datetime, timedelta
import logging

from .models import (
    LetterType, Letter, LetterAttachment, LetterTracking, 
    LetterTemplate, LetterRecipient, LetterSettings
)

# Import advanced views
try:
    from .advanced_views import (
        letter_request_list, letter_request_detail, letter_request_create, letter_request_edit,
        outgoing_letters_list, template_editor, document_upload,
        api_upload_document, api_generate_letter_from_template
    )
except ImportError:
    # Fallback functions if advanced_views not available
    def letter_request_list(request):
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    def letter_request_detail(request, request_id):
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    def letter_request_create(request):
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_create')
    
    def letter_request_edit(request, request_id):
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    def outgoing_letters_list(request):
        messages.error(request, "Fitur surat keluar belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    # template_editor is imported from advanced_views, no fallback needed
    
    def document_upload(request, letter_id):
        messages.error(request, "Fitur upload dokumen belum tersedia")
        return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter_id)
    
    def api_upload_document(request):
        return JsonResponse({'success': False, 'message': 'Fitur belum tersedia'})
    
    def api_generate_letter_from_template(request):
        return JsonResponse({'success': False, 'message': 'Fitur belum tersedia'})
from .forms import (
    LetterForm, LetterTypeForm, LetterStatusForm, LetterRecipientForm,
    LetterAttachmentForm, LetterTrackingForm, LetterSearchForm
)
from .services import LetterValidationService
from .utils import get_letter_status_badge, calculate_letter_priority

# Import references models
try:
    from references.models import Penduduk, Dusun
except ImportError:
    Penduduk = None
    Dusun = None

from django.contrib.auth import get_user_model
User = get_user_model()

logger = logging.getLogger(__name__)

# ===========================
# UTILITY FUNCTIONS
# ===========================

def get_client_ip(request):
    """Get client IP address from request"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

def has_letter_permission(user, permission_name, letter=None):
    """Check if user has specific letter permission"""
    if user.is_superuser:
        return True
    
    # Check group permissions
    if user.groups.filter(name__in=['Letter Admin', 'Village Admin']).exists():
        return True
    
    # Check specific permissions
    from django.contrib.contenttypes.models import ContentType
    from django.contrib.auth.models import Permission
    
    content_type = ContentType.objects.get_for_model(Letter)
    permission = Permission.objects.filter(
        content_type=content_type,
        codename=permission_name
    ).first()
    
    if permission and user.has_perm(f'letters.{permission_name}'):
        return True
    
    # Check if user is the creator of the letter
    if letter and hasattr(letter, 'created_by') and letter.created_by == user:
        return True
    
    return False

def require_letter_permission(permission_name):
    """Decorator to require specific letter permission"""
    def decorator(view_func):
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect('admin_panel:login')
            
            letter_id = kwargs.get('letter_id')
            letter = None
            if letter_id:
                letter = get_object_or_404(Letter, id=letter_id)
            
            if not has_letter_permission(request.user, permission_name, letter):
                raise PermissionDenied("You don't have permission to perform this action.")
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def get_user_accessible_letters(user):
    """Get letters accessible by user based on their role"""
    if user.is_superuser or user.groups.filter(name__in=['Letter Admin', 'Village Admin']).exists():
        return Letter.objects.all()
    
    # Regular users can only see their own letters
    return Letter.objects.filter(created_by=user)

# ===========================
# DASHBOARD VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def admin_dashboard(request):
    """Dashboard admin untuk manajemen surat"""
    # Get letters based on user role
    user_letters = get_user_accessible_letters(request.user)
    
    # Cache dashboard statistics
    def get_dashboard_stats():
        # Statistik umum
        total_letters = user_letters.count()
        pending_letters = user_letters.filter(status__in=['draft', 'submitted', 'in_review']).count()
        completed_letters = user_letters.filter(status='completed').count()
        rejected_letters = user_letters.filter(status='rejected').count()
        
        # Statistik bulanan
        current_month = timezone.now().replace(day=1)
        monthly_letters = user_letters.filter(created_at__gte=current_month).count()
        
        # Statistik mingguan
        week_ago = timezone.now() - timedelta(days=7)
        weekly_letters = user_letters.filter(created_at__gte=week_ago).count()
        
        # Statistik harian
        today = timezone.now().date()
        daily_letters = user_letters.filter(created_at__date=today).count()
        
        return {
            'total_letters': total_letters,
            'pending_letters': pending_letters,
            'completed_letters': completed_letters,
            'rejected_letters': rejected_letters,
            'monthly_letters': monthly_letters,
            'weekly_letters': weekly_letters,
            'daily_letters': daily_letters,
            'completion_rate': round((completed_letters / total_letters * 100) if total_letters > 0 else 0, 1)
        }
    
    cache_key = f'dashboard_stats_{request.user.id}'
    stats = cache.get(cache_key)
    if stats is None:
        stats = get_dashboard_stats()
        cache.set(cache_key, stats, 300)  # Cache for 5 minutes
    
    # Jenis surat paling populer
    popular_letter_types = LetterType.objects.filter(
        letter__in=user_letters
    ).annotate(
        letter_count=Count('letter')
    ).order_by('-letter_count')[:5]
    
    # Surat yang perlu perhatian (pending > 3 hari)
    urgent_letters = user_letters.filter(
        status__in=['submitted', 'in_review'],
        submission_date__lt=timezone.now() - timedelta(days=3)
    ).select_related('letter_type', 'applicant').order_by('submission_date')[:10]
    
    # Recent activities
    recent_activities = LetterTracking.objects.filter(
        letter__in=user_letters
    ).select_related('letter', 'performed_by').order_by('-performed_at')[:10]
    
    # Recent letters
    recent_letters = user_letters.select_related(
        'letter_type', 'applicant', 'created_by'
    ).order_by('-created_at')[:10]
    
    # Chart data untuk grafik
    chart_data = get_chart_data(user_letters)
    
    context = {
        'page_title': 'Dashboard Admin - Manajemen Surat',
        'stats': stats,
        'popular_letter_types': popular_letter_types,
        'urgent_letters': urgent_letters,
        'recent_activities': recent_activities,
        'recent_letters': recent_letters,
        'chart_data': chart_data,
        'user_role': 'Admin' if request.user.groups.filter(name__in=['Letter Admin', 'Village Admin']).exists() else 'User',
        'can_manage_all': has_letter_permission(request.user, 'change_letter'),
        'can_view_analytics': has_letter_permission(request.user, 'view_letter'),
        'active_menu': 'letters',
        'active_submenu': 'dashboard',
    }
    
    return render(request, 'admin_panel/letters/dashboard.html', context)

def get_chart_data(user_letters):
    """Generate chart data for dashboard"""
    # Data untuk 30 hari terakhir
    end_date = timezone.now().date()
    start_date = end_date - timedelta(days=30)
    
    chart_data = {
        'labels': [],
        'datasets': [
            {
                'label': 'Surat Masuk',
                'data': [],
                'backgroundColor': 'rgba(54, 162, 235, 0.2)',
                'borderColor': 'rgba(54, 162, 235, 1)',
                'borderWidth': 1
            },
            {
                'label': 'Surat Selesai',
                'data': [],
                'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                'borderColor': 'rgba(75, 192, 192, 1)',
                'borderWidth': 1
            }
        ]
    }
    
    for i in range(30):
        date = start_date + timedelta(days=i)
        chart_data['labels'].append(date.strftime('%d/%m'))
        
        # Count letters for this date
        daily_letters = user_letters.filter(created_at__date=date).count()
        daily_completed = user_letters.filter(
            created_at__date=date,
            status='completed'
        ).count()
        
        chart_data['datasets'][0]['data'].append(daily_letters)
        chart_data['datasets'][1]['data'].append(daily_completed)
    
    return chart_data

# ===========================
# LETTER MANAGEMENT VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def letter_list(request):
    """Daftar semua surat untuk admin"""
    # Get letters based on user role
    letters = get_user_accessible_letters(request.user).select_related(
        'letter_type', 'applicant', 'applicant__dusun', 'created_by'
    ).order_by('-created_at')
    
    # Filter berdasarkan status
    status_filter = request.GET.get('status')
    if status_filter:
        letters = letters.filter(status=status_filter)
    
    # Filter berdasarkan jenis surat
    type_filter = request.GET.get('type')
    if type_filter:
        letters = letters.filter(letter_type_id=type_filter)
    
    # Filter berdasarkan dusun (untuk admin dusun)
    dusun_filter = request.GET.get('dusun')
    if dusun_filter and Dusun:
        letters = letters.filter(applicant__dusun_id=dusun_filter)
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        letters = letters.filter(
            Q(letter_number__icontains=search_query) |
            Q(subject__icontains=search_query) |
            Q(applicant__nama__icontains=search_query) |
            Q(applicant__nik__icontains=search_query)
        )
    
    # Filter berdasarkan tanggal
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    if date_from:
        letters = letters.filter(created_at__date__gte=date_from)
    if date_to:
        letters = letters.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(letters, 20)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Data untuk filter
    letter_types = LetterType.objects.filter(is_active=True)
    status_choices = Letter.STATUS_CHOICES
    dusun_list = Dusun.objects.filter(is_active=True).order_by('name') if Dusun else []
    
    # Statistics
    stats = {
        'total_letters': letters.count(),
        'pending_count': letters.filter(status__in=['draft', 'submitted', 'in_review']).count(),
        'completed_count': letters.filter(status='completed').count(),
        'rejected_count': letters.filter(status='rejected').count(),
    }
    
    context = {
        'page_title': 'Manajemen Surat',
        'letters': page_obj,
        'letter_types': letter_types,
        'status_choices': status_choices,
        'dusun_list': dusun_list,
        'current_status': status_filter,
        'current_type': type_filter,
        'current_dusun': dusun_filter,
        'search_query': search_query,
        'date_from': date_from,
        'date_to': date_to,
        'stats': stats,
        'can_create_letter': has_letter_permission(request.user, 'add_letter'),
        'can_edit_all': has_letter_permission(request.user, 'change_letter'),
        'active_menu': 'letters',
        'active_submenu': 'list',
    }
    
    return render(request, 'admin_panel/letters/letter_list.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_detail(request, letter_id):
    """Detail surat untuk admin dengan fitur editing"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    # Check permission
    if not has_letter_permission(request.user, 'view_letter', letter):
        raise PermissionDenied("You don't have permission to view this letter.")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'update_status':
            new_status = request.POST.get('status')
            notes = request.POST.get('notes', '')
            
            if new_status in dict(Letter.STATUS_CHOICES):
                old_status = letter.status
                letter.status = new_status
                
                # Update dates based on status
                if new_status == 'submitted' and not letter.submission_date:
                    letter.submission_date = timezone.now()
                elif new_status == 'approved' and not letter.approval_date:
                    letter.approval_date = timezone.now()
                    letter.approved_by = request.user
                elif new_status == 'completed' and not letter.completion_date:
                    letter.completion_date = timezone.now()
                
                letter.save()
                
                # Create tracking record
                LetterTracking.objects.create(
                    letter=letter,
                    action=new_status,
                    description=f'Status diubah dari {old_status} ke {new_status}',
                    performed_by=request.user,
                    notes=notes,
                    ip_address=get_client_ip(request)
                )
                
                messages.success(request, f'Status surat berhasil diubah ke {letter.get_status_display()}')
                return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        
        elif action == 'validate':
            # Basic validation without AI
            validation_service = LetterValidationService()
            validation_result = validation_service.validate_letter(
                letter.content, 
                letter.letter_type.name if letter.letter_type else None
            )
            
            messages.success(request, 'Validasi surat berhasil dilakukan')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        
        elif action == 'generate_pdf':
            success = letter.generate_pdf()
            if success:
                messages.success(request, 'File PDF berhasil dibuat')
            else:
                messages.error(request, 'Gagal membuat file PDF')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        
        elif action == 'generate_word':
            success = letter.generate_word_document()
            if success:
                messages.success(request, 'File Word berhasil dibuat')
            else:
                messages.error(request, 'Gagal membuat file Word')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
    
    # Get tracking history
    tracking_history = letter.tracking_history.all().order_by('-performed_at')
    
    # Get recipients
    recipients = letter.recipients.all()
    
    # Get attachments
    attachments = letter.attachments.all()
    
    context = {
        'page_title': f'Detail Surat - {letter.subject}',
        'letter': letter,
        'tracking_history': tracking_history,
        'recipients': recipients,
        'attachments': attachments,
        'status_choices': Letter.STATUS_CHOICES,
        'can_edit': has_letter_permission(request.user, 'change_letter', letter),
        'can_edit_all': has_letter_permission(request.user, 'change_letter', letter),
        'can_delete': has_letter_permission(request.user, 'delete_letter', letter),
        'active_menu': 'letters',
        'active_submenu': 'detail',
    }
    
    return render(request, 'admin_panel/letters/letter_detail.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_preview(request, letter_id):
    """Preview surat untuk print"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    # Check permission
    if not has_letter_permission(request.user, 'view_letter', letter):
        raise PermissionDenied("You don't have permission to preview this letter.")
    
    # Get additional data
    tracking_history = letter.tracking_history.all().order_by('-performed_at')
    recipients = letter.recipients.all()
    attachments = letter.attachments.all()
    
    context = {
        'letter': letter,
        'tracking_history': tracking_history,
        'recipients': recipients,
        'attachments': attachments,
        'print_mode': request.GET.get('print') == '1',
    }
    
    return render(request, 'admin_panel/letters/letter_preview.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_create(request):
    """Buat surat baru oleh admin"""
    if not has_letter_permission(request.user, 'add_letter'):
        raise PermissionDenied("You don't have permission to create letters.")
    
    if request.method == 'POST':
        form = LetterForm(request.POST)
        if form.is_valid():
            letter = form.save(commit=False)
            letter.created_by = request.user
            letter.save()
            
            # Create tracking record
            LetterTracking.objects.create(
                letter=letter,
                action='created',
                description='Surat dibuat oleh admin',
                performed_by=request.user,
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Surat berhasil dibuat')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
    else:
        form = LetterForm()
    
    # Get templates for selection
    templates = LetterTemplate.objects.filter(is_active=True).order_by('-is_default', 'name')
    
    context = {
        'page_title': 'Buat Surat Baru',
        'form': form,
        'templates': templates,
        'active_menu': 'letters',
        'active_submenu': 'create',
    }
    
    return render(request, 'admin_panel/letters/letter_form.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_edit(request, letter_id):
    """Edit surat oleh admin"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    if not has_letter_permission(request.user, 'change_letter', letter):
        raise PermissionDenied("You don't have permission to edit this letter.")
    
    if request.method == 'POST':
        form = LetterForm(request.POST, instance=letter)
        if form.is_valid():
            form.save()
            
            # Create tracking record
            LetterTracking.objects.create(
                letter=letter,
                action='updated',
                description='Surat diperbarui oleh admin',
                performed_by=request.user,
                ip_address=get_client_ip(request)
            )
            
            messages.success(request, 'Surat berhasil diperbarui')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
    else:
        form = LetterForm(instance=letter)
    
    # Get templates for selection
    templates = LetterTemplate.objects.filter(is_active=True).order_by('-is_default', 'name')
    
    context = {
        'page_title': f'Edit Surat - {letter.subject}',
        'form': form,
        'letter': letter,
        'templates': templates,
        'active_menu': 'letters',
        'active_submenu': 'edit',
    }
    
    return render(request, 'admin_panel/letters/letter_form.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_delete(request, letter_id):
    """Hapus surat oleh admin"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    if not has_letter_permission(request.user, 'delete_letter', letter):
        raise PermissionDenied("You don't have permission to delete this letter.")
    
    if request.method == 'POST':
        letter_number = letter.letter_number or letter.id
        letter.delete()
        messages.success(request, f'Surat {letter_number} berhasil dihapus')
        return redirect('admin_panel:letters:admin_letter_list')
    
    context = {
        'page_title': f'Hapus Surat - {letter.subject}',
        'letter': letter,
        'active_menu': 'letters',
        'active_submenu': 'delete',
    }
    
    # Delete confirmation handled by modal, redirect after POST
    return redirect('admin_panel:letters:admin_letter_list')

# ===========================
# LETTER TYPE MANAGEMENT
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def letter_type_list(request):
    """Daftar jenis surat"""
    letter_types = LetterType.objects.all().order_by('name')
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        letter_types = letter_types.filter(
            Q(name__icontains=search_query) |
            Q(code__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(letter_types, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    active_types = letter_types.filter(is_active=True).count()
    inactive_types = letter_types.filter(is_active=False).count()
    
    context = {
        'page_title': 'Manajemen Jenis Surat',
        'letter_types': page_obj,
        'search_query': search_query,
        'active_types': active_types,
        'inactive_types': inactive_types,
        'active_menu': 'letters',
        'active_submenu': 'types',
    }
    
    return render(request, 'admin_panel/letters/letter_type_list.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_type_create(request):
    """Buat jenis surat baru"""
    if request.method == 'POST':
        form = LetterTypeForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis surat berhasil dibuat')
            return redirect('admin_panel:letters:admin_letter_type_list')
    else:
        form = LetterTypeForm()
    
    context = {
        'page_title': 'Buat Jenis Surat Baru',
        'form': form,
        'active_menu': 'letters',
        'active_submenu': 'types',
    }
    
    return render(request, 'admin_panel/letters/letter_type_form.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_type_edit(request, type_id):
    """Edit jenis surat"""
    letter_type = get_object_or_404(LetterType, id=type_id)
    
    if request.method == 'POST':
        form = LetterTypeForm(request.POST, request.FILES, instance=letter_type)
        if form.is_valid():
            form.save()
            messages.success(request, 'Jenis surat berhasil diperbarui')
            return redirect('admin_panel:letters:admin_letter_type_list')
    else:
        form = LetterTypeForm(instance=letter_type)
    
    context = {
        'page_title': f'Edit Jenis Surat - {letter_type.name}',
        'form': form,
        'letter_type': letter_type,
        'active_menu': 'letters',
        'active_submenu': 'types',
    }
    
    return render(request, 'admin_panel/letters/letter_type_form.html', context)

# ===========================
# TEMPLATE MANAGEMENT
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def template_list(request):
    """Daftar template surat"""
    templates = LetterTemplate.objects.all().order_by('-created_at')
    
    # Pencarian
    search_query = request.GET.get('search')
    if search_query:
        templates = templates.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(templates, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Statistics
    active_templates = templates.filter(is_active=True).count()
    inactive_templates = templates.filter(is_active=False).count()
    
    context = {
        'page_title': 'Manajemen Template Surat',
        'templates': page_obj,
        'search_query': search_query,
        'active_templates': active_templates,
        'inactive_templates': inactive_templates,
        'active_menu': 'letters',
        'active_submenu': 'templates',
    }
    
    return render(request, 'admin_panel/letters/template_list.html', context)

# ===========================
# SETTINGS MANAGEMENT
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def settings_view(request):
    """Pengaturan sistem surat"""
    if not request.user.is_superuser:
        raise PermissionDenied("Only superusers can access settings.")
    
    # Get or create settings
    settings_obj, created = LetterSettings.objects.get_or_create(
        is_active=True,
        defaults={
            'village_name': 'Desa Pulosarok',
            'village_address': 'Kecamatan Pulosarok, Kabupaten Indramayu',
            'head_of_village_name': 'Kepala Desa',
            'created_by': request.user
        }
    )
    
    if request.method == 'POST':
        # Update settings
        settings_obj.village_name = request.POST.get('village_name', settings_obj.village_name)
        settings_obj.village_address = request.POST.get('village_address', settings_obj.village_address)
        settings_obj.village_phone = request.POST.get('village_phone', settings_obj.village_phone)
        settings_obj.village_email = request.POST.get('village_email', settings_obj.village_email)
        settings_obj.head_of_village_name = request.POST.get('head_of_village_name', settings_obj.head_of_village_name)
        settings_obj.head_of_village_nip = request.POST.get('head_of_village_nip', settings_obj.head_of_village_nip)
        settings_obj.letter_number_format = request.POST.get('letter_number_format', settings_obj.letter_number_format)
        settings_obj.enable_digital_signature = request.POST.get('enable_digital_signature') == 'on'
        
        settings_obj.save()
        messages.success(request, 'Pengaturan berhasil disimpan')
        return redirect('admin_panel:letters:admin_settings')
    
    context = {
        'page_title': 'Pengaturan Sistem Surat',
        'settings': settings_obj,
        'active_menu': 'letters',
        'active_submenu': 'settings',
    }
    
    return render(request, 'admin_panel/letters/settings.html', context)

# ===========================
# PRINT VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def letter_print(request, letter_id, format_type='pdf'):
    """Print surat dalam format PDF atau Word"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    # Check permission
    if not has_letter_permission(request.user, 'view_letter', letter):
        raise PermissionDenied("You don't have permission to print this letter.")
    
    # Generate file if not exists
    if format_type.lower() == 'pdf':
        if not letter.pdf_file:
            success = letter.generate_pdf()
            if not success:
                messages.error(request, 'Gagal membuat file PDF. Pastikan ReportLab terinstall.')
                return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        
        # Return PDF file
        response = HttpResponse(letter.pdf_file.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename="{letter.letter_number or letter.id}.pdf"'
        return response
        
    elif format_type.lower() == 'word':
        if not letter.word_file:
            success = letter.generate_word_document()
            if not success:
                messages.error(request, 'Gagal membuat file Word. Pastikan python-docx terinstall.')
                return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        
        # Return Word file
        response = HttpResponse(letter.word_file.read(), 
                              content_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document')
        response['Content-Disposition'] = f'inline; filename="{letter.letter_number or letter.id}.docx"'
        return response
    
    else:
        messages.error(request, 'Format file tidak didukung.')
        return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)

# ===========================
# AJAX ENDPOINTS
# ===========================

@csrf_exempt
@require_http_methods(["GET"])
def api_letter_print(request, letter_id):
    """API untuk mendapatkan URL print surat"""
    try:
        letter = get_object_or_404(Letter, id=letter_id)
        format_type = request.GET.get('format', 'pdf')
        
        if format_type.lower() not in ['pdf', 'word']:
            return JsonResponse({
                'success': False,
                'message': 'Format tidak didukung. Gunakan pdf atau word.'
            })
        
        print_url = letter.get_print_url(format_type)
        
        if print_url:
            return JsonResponse({
                'success': True,
                'print_url': print_url,
                'format': format_type,
                'letter_number': letter.letter_number or str(letter.id)
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'Gagal membuat file untuk print.'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })

@csrf_exempt
@require_http_methods(["POST"])
def api_bulk_action(request):
    """API untuk aksi bulk pada surat"""
    try:
        data = json.loads(request.body)
        action = data.get('action')
        letter_ids = data.get('letter_ids', [])
        
        if not action or not letter_ids:
            return JsonResponse({
                'success': False,
                'message': 'Action dan letter_ids diperlukan'
            })
        
        letters = Letter.objects.filter(id__in=letter_ids)
        
        if action == 'approve':
            letters.update(
                status='approved',
                approval_date=timezone.now(),
                approved_by=request.user
            )
            message = f'{letters.count()} surat berhasil disetujui'
            
        elif action == 'reject':
            letters.update(status='rejected')
            message = f'{letters.count()} surat berhasil ditolak'
            
        elif action == 'complete':
            letters.update(
                status='completed',
                completion_date=timezone.now()
            )
            message = f'{letters.count()} surat berhasil diselesaikan'
            
        else:
            return JsonResponse({
                'success': False,
                'message': 'Action tidak valid'
            })
        
        # Create tracking records
        for letter in letters:
            LetterTracking.objects.create(
                letter=letter,
                action=action,
                description=f'Bulk action: {action}',
                performed_by=request.user,
                ip_address=get_client_ip(request)
            )
        
        return JsonResponse({
            'success': True,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Terjadi kesalahan: {str(e)}'
        })

# ===========================
# ANALYTICS VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def analytics_view(request):
    """Analytics surat untuk admin"""
    user_letters = get_user_accessible_letters(request.user)
    
    # Letter Statistics
    total_letters = user_letters.count()
    draft_letters = user_letters.filter(status='draft').count()
    submitted_letters = user_letters.filter(status='submitted').count()
    approved_letters = user_letters.filter(status='approved').count()
    completed_letters = user_letters.filter(status='completed').count()
    rejected_letters = user_letters.filter(status='rejected').count()
    
    # Monthly letter usage
    current_month = timezone.now().replace(day=1)
    monthly_letters = user_letters.filter(
        created_at__gte=current_month
    ).count()
    
    # Recent letters
    recent_letters = user_letters.select_related(
        'applicant', 'letter_type'
    ).order_by('-created_at')[:10]
    
    # Letter type statistics
    letter_type_stats = LetterType.objects.filter(
        letter__in=user_letters
    ).annotate(
        total_count=Count('letter'),
        completed_count=Count('letter', filter=Q(letter__status='completed')),
        pending_count=Count('letter', filter=Q(letter__status__in=['draft', 'submitted', 'in_review']))
    ).order_by('-total_count')
    
    context = {
        'page_title': 'Analytics Surat',
        'total_letters': total_letters,
        'draft_letters': draft_letters,
        'submitted_letters': submitted_letters,
        'approved_letters': approved_letters,
        'completed_letters': completed_letters,
        'rejected_letters': rejected_letters,
        'monthly_letters': monthly_letters,
        'recent_letters': recent_letters,
        'letter_type_stats': letter_type_stats,
        'active_menu': 'letters',
        'active_submenu': 'analytics',
    }
    
    return render(request, 'admin_panel/letters/analytics.html', context)
