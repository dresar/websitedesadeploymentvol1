"""
Advanced Letter Views untuk Sistem Surat Desa Pulosarok
Pemisahan surat masuk dan keluar dengan fitur verifikasi lengkap
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
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import logging
import uuid
from datetime import datetime, timedelta

# Import models
from .models import (
    LetterType, Letter, LetterAttachment, LetterTracking, 
    LetterTemplate, LetterRecipient, LetterSettings
)

# Import advanced models
try:
    from .models_advanced import (
        LetterRequest, SupportingDocument, LetterWorkflow, 
        LetterApproval, LetterNotification
    )
except ImportError:
    # Fallback jika models_advanced belum di-import
    LetterRequest = None
    SupportingDocument = None
    LetterWorkflow = None
    LetterApproval = None
    LetterNotification = None

from .forms import (
    LetterForm, LetterTypeForm, LetterStatusForm, LetterRecipientForm,
    LetterAttachmentForm, LetterTrackingForm, LetterSearchForm, LetterTemplateForm
)

# Import references models
try:
    from references.models import Penduduk, Dusun
except ImportError:
    Penduduk = None
    Dusun = None

# Lazy import User model
def get_user():
    from django.contrib.auth import get_user_model
    return get_user_model()

logger = logging.getLogger(__name__)

# ===========================
# UTILITY FUNCTIONS
# ===========================

def has_letter_permission(user, permission, obj=None):
    """Check if user has permission for letter operations"""
    if user.is_superuser:
        return True
    
    # Add more specific permission checks here
    return user.is_staff

def get_client_ip(request):
    """Get client IP address"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

# ===========================
# LETTER REQUEST VIEWS (SURAT MASUK)
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def letter_request_list(request):
    """Daftar permintaan surat dari penduduk"""
    if not LetterRequest:
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    # Filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    priority_filter = request.GET.get('priority', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base queryset
    requests = LetterRequest.objects.select_related(
        'letter_type', 'applicant', 'verified_by'
    ).prefetch_related('supporting_documents')
    
    # Apply filters
    if search_query:
        requests = requests.filter(
            Q(applicant__nama__icontains=search_query) |
            Q(applicant__nik__icontains=search_query) |
            Q(purpose__icontains=search_query) |
            Q(request_number__icontains=search_query)
        )
    
    if status_filter:
        requests = requests.filter(status=status_filter)
    
    if priority_filter:
        requests = requests.filter(priority=priority_filter)
    
    if date_from:
        requests = requests.filter(submitted_at__date__gte=date_from)
    
    if date_to:
        requests = requests.filter(submitted_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(requests, 10)
    page_number = request.GET.get('page')
    requests_page = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total': LetterRequest.objects.count(),
        'pending': LetterRequest.objects.filter(status='pending').count(),
        'verified': LetterRequest.objects.filter(status='verified').count(),
        'in_progress': LetterRequest.objects.filter(status='in_progress').count(),
        'completed': LetterRequest.objects.filter(status='completed').count(),
        'rejected': LetterRequest.objects.filter(status='rejected').count(),
    }
    
    context = {
        'page_title': 'Permintaan Surat',
        'requests': requests_page,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
        'priority_filter': priority_filter,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': LetterRequest.STATUS_CHOICES,
        'priority_choices': LetterRequest.PRIORITY_CHOICES,
        'active_menu': 'letters',
        'active_submenu': 'requests',
    }
    
    return render(request, 'admin_panel/letters/letter_request_list.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_request_detail(request, request_id):
    """Detail permintaan surat"""
    if not LetterRequest:
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_list')
    
    letter_request = get_object_or_404(LetterRequest, id=request_id)
    
    # Check permission
    if not has_letter_permission(request.user, 'view_letter_request', letter_request):
        raise PermissionDenied("You don't have permission to view this request.")
    
    if request.method == 'POST':
        action = request.POST.get('action')
        
        if action == 'verify':
            letter_request.status = 'verified'
            letter_request.verified_by = request.user
            letter_request.verification_date = timezone.now()
            letter_request.verification_notes = request.POST.get('verification_notes', '')
            letter_request.save()
            
            messages.success(request, 'Permintaan surat berhasil diverifikasi')
            return redirect('admin_panel:letters:letter_request_detail', request_id=letter_request.id)
        
        elif action == 'reject':
            letter_request.status = 'rejected'
            letter_request.rejected_by = request.user
            letter_request.rejection_date = timezone.now()
            letter_request.rejection_reason = request.POST.get('rejection_reason', '')
            letter_request.save()
            
            messages.success(request, 'Permintaan surat ditolak')
            return redirect('admin_panel:letters:letter_request_detail', request_id=letter_request.id)
        
        elif action == 'generate_letter':
            # Generate letter from request
            letter = Letter.objects.create(
                letter_type=letter_request.letter_type,
                applicant=letter_request.applicant,
                subject=f"Surat {letter_request.letter_type.name}",
                content="",  # Will be filled by template
                purpose=letter_request.purpose,
                status='draft',
                created_by=request.user
            )
            
            letter_request.generated_letter = letter
            letter_request.status = 'in_progress'
            letter_request.save()
            
            messages.success(request, 'Surat berhasil dibuat dari permintaan')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
    
    # Get supporting documents
    supporting_docs = letter_request.supporting_documents.all()
    
    context = {
        'page_title': f'Detail Permintaan - {letter_request.request_number}',
        'letter_request': letter_request,
        'supporting_docs': supporting_docs,
        'can_verify': has_letter_permission(request.user, 'verify_letter_request', letter_request),
        'can_reject': has_letter_permission(request.user, 'reject_letter_request', letter_request),
        'can_generate': has_letter_permission(request.user, 'generate_letter', letter_request),
        'active_menu': 'letters',
        'active_submenu': 'requests',
    }
    
    return render(request, 'admin_panel/letters/letter_request_detail.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_request_create(request):
    """Buat permintaan surat baru (untuk admin)"""
    if not LetterRequest:
        messages.error(request, "Fitur permintaan surat belum tersedia")
        return redirect('admin_panel:letters:admin_letter_create')
    
    if request.method == 'POST':
        # Handle form submission
        letter_type_id = request.POST.get('letter_type')
        applicant_id = request.POST.get('applicant')
        purpose = request.POST.get('purpose')
        detailed_purpose = request.POST.get('detailed_purpose', '')
        urgency_reason = request.POST.get('urgency_reason', '')
        priority = request.POST.get('priority', 'normal')
        
        try:
            letter_type = LetterType.objects.get(id=letter_type_id)
            applicant = Penduduk.objects.get(id=applicant_id)
            
            # Generate unique request number
            timestamp = timezone.now().strftime('%Y%m%d%H%M%S')
            request_number = f"REQ/{timestamp}/{uuid.uuid4().hex[:6].upper()}"
            
            letter_request = LetterRequest.objects.create(
                request_number=request_number,
                letter_type=letter_type,
                applicant=applicant,
                purpose=purpose,
                detailed_purpose=detailed_purpose,
                urgency_reason=urgency_reason,
                priority=priority,
                status='verified',  # Auto-verified for admin created requests
                verified_by=request.user,
                verification_date=timezone.now(),
                verification_notes='Permintaan dibuat langsung oleh admin'
            )
            
            # Handle file uploads
            files = request.FILES.getlist('documents')
            if files:
                for file in files:
                    SupportingDocument.objects.create(
                        request=letter_request,
                        title=file.name,
                        description=f'Dokumen pendukung untuk {letter_type.name}',
                        file=file,
                        uploaded_by=request.user,
                        file_size=file.size
                    )
            
            messages.success(request, f'Permintaan surat berhasil dibuat dengan nomor {request_number}')
            return redirect('admin_panel:letters:letter_request_detail', request_id=letter_request.id)
            
        except (LetterType.DoesNotExist, Penduduk.DoesNotExist):
            messages.error(request, 'Data tidak valid')
        except Exception as e:
            logger.error(f"Error creating letter request: {str(e)}")
            messages.error(request, 'Terjadi kesalahan saat membuat permintaan surat')
    
    # Get available data
    letter_types = LetterType.objects.filter(is_active=True)
    penduduks = Penduduk.objects.all()[:100]  # Limit for performance
    
    context = {
        'page_title': 'Buat Permintaan Surat',
        'letter_types': letter_types,
        'penduduks': penduduks,
        'priority_choices': LetterRequest.PRIORITY_CHOICES,
        'active_menu': 'letters',
        'active_submenu': 'requests',
    }
    
    return render(request, 'admin_panel/letters/letter_request_create.html', context)

@staff_member_required(login_url='/admin-panel/login/')
def letter_request_edit(request, request_id):
    """Edit permintaan surat yang sudah ada"""
    try:
        request_obj = LetterRequest.objects.get(id=request_id)
    except LetterRequest.DoesNotExist:
        messages.error(request, "Permintaan surat tidak ditemukan")
        return redirect('admin_panel:letters:letter_request_list')
    
    if request.method == 'POST':
        # Handle form submission
        letter_type_id = request.POST.get('letter_type')
        applicant_id = request.POST.get('applicant')
        purpose = request.POST.get('purpose')
        detailed_purpose = request.POST.get('detailed_purpose', '')
        urgency_reason = request.POST.get('urgency_reason', '')
        priority = request.POST.get('priority', 'normal')
        
        try:
            letter_type = LetterType.objects.get(id=letter_type_id)
            applicant = Penduduk.objects.get(id=applicant_id)
            
            # Update request
            request_obj.letter_type = letter_type
            request_obj.applicant = applicant
            request_obj.purpose = purpose
            request_obj.detailed_purpose = detailed_purpose
            request_obj.urgency_reason = urgency_reason
            request_obj.priority = priority
            request_obj.save()
            
            # Handle new file uploads
            files = request.FILES.getlist('documents')
            if files:
                for file in files:
                    SupportingDocument.objects.create(
                        request=request_obj,
                        title=file.name,
                        description=f'Dokumen pendukung untuk {letter_type.name}',
                        file=file,
                        uploaded_by=request.user,
                        file_size=file.size
                    )
            
            messages.success(request, f'Permintaan surat {request_obj.request_number} berhasil diperbarui')
            return redirect('admin_panel:letters:letter_request_detail', request_id=request_obj.id)
            
        except (LetterType.DoesNotExist, Penduduk.DoesNotExist):
            messages.error(request, 'Data tidak valid')
        except Exception as e:
            logger.error(f"Error updating letter request: {str(e)}")
            messages.error(request, 'Terjadi kesalahan saat memperbarui permintaan surat')
    
    # Get available data
    letter_types = LetterType.objects.filter(is_active=True)
    penduduks = Penduduk.objects.all()[:100]
    
    context = {
        'page_title': 'Edit Permintaan Surat',
        'request_obj': request_obj,
        'letter_types': letter_types,
        'penduduks': penduduks,
        'priority_choices': LetterRequest.PRIORITY_CHOICES,
        'active_menu': 'letters',
        'active_submenu': 'requests',
    }
    
    return render(request, 'admin_panel/letters/letter_request_edit.html', context)

# ===========================
# OUTGOING LETTERS VIEWS (SURAT KELUAR)
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def outgoing_letters_list(request):
    """Daftar surat keluar (yang sudah dibuat oleh admin)"""
    # Filter parameters
    search_query = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    letter_type_filter = request.GET.get('letter_type', '')
    date_from = request.GET.get('date_from', '')
    date_to = request.GET.get('date_to', '')
    
    # Base queryset - only letters created by staff
    letters = Letter.objects.filter(
        created_by__is_staff=True
    ).select_related(
        'letter_type', 'applicant', 'created_by', 'approved_by'
    ).prefetch_related('attachments')
    
    # Apply filters
    if search_query:
        letters = letters.filter(
            Q(subject__icontains=search_query) |
            Q(letter_number__icontains=search_query) |
            Q(applicant__nama__icontains=search_query) |
            Q(content__icontains=search_query)
        )
    
    if status_filter:
        letters = letters.filter(status=status_filter)
    
    if letter_type_filter:
        letters = letters.filter(letter_type_id=letter_type_filter)
    
    if date_from:
        letters = letters.filter(created_at__date__gte=date_from)
    
    if date_to:
        letters = letters.filter(created_at__date__lte=date_to)
    
    # Pagination
    paginator = Paginator(letters, 20)
    page_number = request.GET.get('page')
    letters_page = paginator.get_page(page_number)
    
    # Statistics
    stats = {
        'total': Letter.objects.filter(created_by__is_staff=True).count(),
        'draft': Letter.objects.filter(created_by__is_staff=True, status='draft').count(),
        'submitted': Letter.objects.filter(created_by__is_staff=True, status='submitted').count(),
        'approved': Letter.objects.filter(created_by__is_staff=True, status='approved').count(),
        'completed': Letter.objects.filter(created_by__is_staff=True, status='completed').count(),
    }
    
    # Get filter options
    letter_types = LetterType.objects.filter(is_active=True)
    
    context = {
        'page_title': 'Surat Keluar',
        'letters': letters_page,
        'stats': stats,
        'search_query': search_query,
        'status_filter': status_filter,
        'letter_type_filter': letter_type_filter,
        'date_from': date_from,
        'date_to': date_to,
        'status_choices': Letter.STATUS_CHOICES,
        'letter_types': letter_types,
        'active_menu': 'letters',
        'active_submenu': 'outgoing',
    }
    
    return render(request, 'admin_panel/letters/outgoing_letters_list.html', context)

# ===========================
# TEMPLATE MANAGEMENT VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def template_editor(request, template_id=None):
    """Editor template surat"""
    template = None
    if template_id:
        template = get_object_or_404(LetterTemplate, id=template_id)
    
    if request.method == 'POST':
        form = LetterTemplateForm(request.POST, instance=template)
        if form.is_valid():
            template = form.save(commit=False)
            if not template_id:  # New template
                template.created_by = request.user
            template.save()
            
            messages.success(request, 'Template berhasil disimpan')
            return redirect('admin_panel:letters:template_editor', template_id=template.id)
        else:
            messages.error(request, 'Data tidak valid')
    else:
        form = LetterTemplateForm(instance=template)
    
    context = {
        'page_title': 'Editor Template' if template else 'Buat Template Baru',
        'form': form,
        'template': template,
        'template_types': LetterTemplate.TEMPLATE_TYPE_CHOICES,
        'active_menu': 'letters',
        'active_submenu': 'templates',
    }
    
    return render(request, 'admin_panel/letters/template_editor.html', context)

# ===========================
# DOCUMENT MANAGEMENT VIEWS
# ===========================

@staff_member_required(login_url='/admin-panel/login/')
def document_upload(request, letter_id):
    """Upload dokumen pendukung untuk surat"""
    letter = get_object_or_404(Letter, id=letter_id)
    
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description', '')
        file = request.FILES.get('file')
        
        if title and file:
            attachment = LetterAttachment.objects.create(
                letter=letter,
                title=title,
                description=description,
                file=file,
                uploaded_by=request.user
            )
            
            messages.success(request, 'Dokumen berhasil diupload')
            return redirect('admin_panel:letters:admin_letter_detail', letter_id=letter.id)
        else:
            messages.error(request, 'Judul dan file harus diisi')
    
    context = {
        'page_title': 'Upload Dokumen',
        'letter': letter,
        'active_menu': 'letters',
        'active_submenu': 'documents',
    }
    
    return render(request, 'admin_panel/letters/document_upload.html', context)

# ===========================
# API ENDPOINTS
# ===========================

@csrf_exempt
@require_http_methods(["POST"])
def api_upload_document(request):
    """API untuk upload dokumen"""
    try:
        data = json.loads(request.body)
        letter_id = data.get('letter_id')
        title = data.get('title')
        description = data.get('description', '')
        
        letter = get_object_or_404(Letter, id=letter_id)
        
        # Handle file upload
        if 'file' in request.FILES:
            file = request.FILES['file']
            attachment = LetterAttachment.objects.create(
                letter=letter,
                title=title,
                description=description,
                file=file,
                uploaded_by=request.user
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Dokumen berhasil diupload',
                'attachment_id': attachment.id
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'File tidak ditemukan'
            })
            
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })

@csrf_exempt
@require_http_methods(["POST"])
def api_generate_letter_from_template(request):
    """API untuk generate surat dari template"""
    try:
        data = json.loads(request.body)
        template_id = data.get('template_id')
        letter_id = data.get('letter_id')
        variables = data.get('variables', {})
        
        template = get_object_or_404(LetterTemplate, id=template_id)
        letter = get_object_or_404(Letter, id=letter_id)
        
        # Generate content from template
        content = template.content_template
        for key, value in variables.items():
            content = content.replace(f'{{{key}}}', str(value))
        
        letter.content = content
        letter.template = template
        letter.save()
        
        return JsonResponse({
            'success': True,
            'message': 'Surat berhasil di-generate dari template',
            'content': content
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': str(e)
        })
