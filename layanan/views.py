from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.core.paginator import Paginator
from django.db.models import Q
import json

# Import models from different apps
from documents.models import Document
from .models import LayananDocumentRequest
from business.models import LayananJasa
from posyandu.models import PosyanduLocation, PosyanduSchedule
from tourism.models import TourismLocation, TourismEvent
from news.models import Announcement

# Import letters models
try:
    from letters.models import LetterType, Letter, LetterAttachment, LetterTracking
    LETTERS_AVAILABLE = True
except ImportError:
    LETTERS_AVAILABLE = False
    LetterType = Letter = LetterAttachment = LetterTracking = None


class LayananIndexView(TemplateView):
    """Main layanan page with overview of all services"""
    template_name = 'public/layanan/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent announcements
        context['recent_announcements'] = Announcement.objects.filter(
            status='published'
        ).order_by('-created_at')[:3]
        
        # Get document types count
        context['document_types_count'] = len(LayananDocumentRequest.DOCUMENT_TYPE_CHOICES)
        
        # Get business services count
        context['business_services_count'] = LayananJasa.objects.filter(
            status='aktif'
        ).count()
        
        # Get posyandu locations count
        context['posyandu_locations_count'] = PosyanduLocation.objects.filter(
            is_active=True
        ).count()
        
        # Get tourism locations count
        context['tourism_locations_count'] = TourismLocation.objects.filter(
            is_active=True
        ).count()
        
        return context


class ComplaintServicesView(TemplateView):
    """Complaint services page - uses the same template as complaints"""
    template_name = 'public/complaints/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from complaints.forms import ComplaintForm
        from complaints.models import ComplaintCategory
        
        context['form'] = ComplaintForm()
        context['categories'] = ComplaintCategory.objects.filter(is_active=True)
        context['page_title'] = 'Formulir Pengaduan'
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle form submission"""
        from complaints.forms import ComplaintForm
        from complaints.models import ComplaintCategory
        from django.contrib import messages
        
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            complaint = form.save()
            
            # Kirim notifikasi email ke pelapor
            from complaints.views import send_complaint_notification, send_admin_notification
            send_complaint_notification(complaint, 'new')
            send_admin_notification(complaint, 'new')
            
            messages.success(request, f'Pengaduan berhasil dikirim! ID Pengaduan Anda: {complaint.complaint_id}')
            return redirect('complaints:complaint_success', complaint_id=complaint.complaint_id)
        else:
            messages.error(request, 'Terjadi kesalahan dalam pengisian form. Silakan periksa kembali.')
        
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)


class DocumentServicesView(TemplateView):
    """Document services listing page - uses letters system"""
    template_name = 'public/layanan/document_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all letter types from letters app with pagination
        if LETTERS_AVAILABLE:
            from django.core.paginator import Paginator
            
            document_types = LetterType.objects.filter(is_active=True).order_by('name')
            paginator = Paginator(document_types, 6)  # 6 items per page
            
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context['document_types'] = page_obj
            context['page_obj'] = page_obj
            
            # Get recent requests (no pagination for sidebar)
            context['recent_requests'] = Letter.objects.filter(
                status__in=['submitted', 'processing', 'approved', 'rejected']
            ).order_by('-created_at')[:5]
        else:
            context['document_types'] = []
            context['recent_requests'] = []
            context['page_obj'] = None
        
        return context


class DocumentInfoView(TemplateView):
    """Document information page"""
    template_name = 'public/layanan/document_info.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        document_type = self.kwargs.get('document_type', '')
        
        if document_type:
            # Map URL parameters to document type choices
            type_mapping = {
                'surat_keterangan': 'Surat Keterangan',
                'surat_pengantar': 'Surat Pengantar',
                'surat_izin': 'Surat Izin',
                'surat_rekomendasi': 'Surat Rekomendasi',
                'surat_kepemilikan': 'Surat Kepemilikan',
                'surat_lainnya': 'Surat Lainnya',
            }
            
            # Get the mapped name or use the original parameter
            mapped_name = type_mapping.get(document_type, document_type)
            
            # Find the selected document type from choices
            selected_type = None
            for choice_value, choice_label in LayananDocumentRequest.DOCUMENT_TYPE_CHOICES:
                if mapped_name.lower() in choice_label.lower() or document_type.lower() in choice_label.lower():
                    selected_type = {'value': choice_value, 'label': choice_label}
                    break
            context['selected_document_type'] = selected_type
        
        # Get all document types for selection
        context['document_types'] = LayananDocumentRequest.DOCUMENT_TYPE_CHOICES
        
        return context


class DocumentRequestView(TemplateView):
    """Document request form page - redirects to letters system"""
    template_name = 'public/layanan/document_request.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get all letter types from letters app
        if LETTERS_AVAILABLE:
            context['document_types'] = LetterType.objects.filter(is_active=True).order_by('name')
        else:
            context['document_types'] = []
        
        return context


class DocumentRequestSubmitView(TemplateView):
    """Handle document request submission"""
    template_name = 'public/layanan/document_request_success.html'
    
    def post(self, request, *args, **kwargs):
        # Handle form submission
        full_name = request.POST.get('full_name')
        nik = request.POST.get('nik')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        address = request.POST.get('address')
        document_type = request.POST.get('document_type')
        purpose = request.POST.get('purpose')
        description = request.POST.get('description')
        
        # Create document request
        try:
            LayananDocumentRequest.objects.create(
                full_name=full_name,
                nik=nik,
                phone=phone,
                email=email,
                address=address,
                document_type=document_type,
                purpose=purpose,
                description=description,
                status='pending'
            )
            messages.success(request, 'Permintaan dokumen berhasil diajukan!')
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
        
        return self.get(request, *args, **kwargs)


class BusinessServicesView(TemplateView):
    """Business services listing page"""
    template_name = 'public/layanan/business_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from django.core.paginator import Paginator
        
        # Get business services with pagination
        business_services = LayananJasa.objects.filter(
            status='aktif'
        ).order_by('nama')
        
        paginator = Paginator(business_services, 8)  # 8 items per page
        page_number = self.request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        
        context['business_services'] = page_obj
        context['page_obj'] = page_obj
        
        return context


class HealthServicesView(TemplateView):
    """Health services listing page"""
    template_name = 'public/layanan/health_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get posyandu locations
        context['posyandu_locations'] = PosyanduLocation.objects.filter(
            is_active=True
        ).order_by('name')
        
        # Get posyandu schedules
        context['posyandu_schedules'] = PosyanduSchedule.objects.all().order_by('schedule_date')
        
        return context


class TourismServicesView(TemplateView):
    """Tourism services listing page"""
    template_name = 'public/layanan/tourism_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from django.core.paginator import Paginator
        
        # Get tourism locations with pagination
        tourism_locations = TourismLocation.objects.filter(
            is_active=True
        ).order_by('title')
        
        paginator_locations = Paginator(tourism_locations, 6)  # 6 items per page
        page_number_locations = self.request.GET.get('page_locations', 1)
        page_obj_locations = paginator_locations.get_page(page_number_locations)
        
        context['tourism_locations'] = page_obj_locations
        context['page_obj_locations'] = page_obj_locations
        
        # Get tourism events with pagination
        tourism_events = TourismEvent.objects.filter(
            is_active=True
        ).order_by('-start_date')
        
        paginator_events = Paginator(tourism_events, 8)  # 8 items per page
        page_number_events = self.request.GET.get('page_events', 1)
        page_obj_events = paginator_events.get_page(page_number_events)
        
        context['tourism_events'] = page_obj_events
        context['page_obj_events'] = page_obj_events
        
        return context


class ContactView(TemplateView):
    """Contact page"""
    template_name = 'public/layanan/contact.html'


class RequestStatusView(TemplateView):
    """Request status page - uses letters system"""
    template_name = 'public/layanan/request_status.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Get recent requests from letters system with pagination
        if LETTERS_AVAILABLE:
            from django.core.paginator import Paginator
            
            recent_requests = Letter.objects.filter(
                status__in=['submitted', 'processing', 'approved', 'rejected']
            ).order_by('-created_at')
            
            paginator = Paginator(recent_requests, 10)  # 10 items per page
            page_number = self.request.GET.get('page')
            page_obj = paginator.get_page(page_number)
            
            context['recent_requests'] = page_obj
            context['page_obj'] = page_obj
        else:
            context['recent_requests'] = []
            context['page_obj'] = None
        
        return context


class PosyanduServicesView(TemplateView):
    """Posyandu services page"""
    template_name = 'public/posyandu/posyandu_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        from django.core.paginator import Paginator
        
        # Get posyandu locations with pagination
        posyandu_locations = PosyanduLocation.objects.filter(
            is_active=True
        ).order_by('name')
        
        paginator_locations = Paginator(posyandu_locations, 6)  # 6 items per page
        page_number_locations = self.request.GET.get('page_locations', 1)
        page_obj_locations = paginator_locations.get_page(page_number_locations)
        
        context['posyandu_locations'] = page_obj_locations
        context['page_obj_locations'] = page_obj_locations
        
        # Get posyandu schedules with pagination
        posyandu_schedules = PosyanduSchedule.objects.all().order_by('schedule_date')
        
        paginator_schedules = Paginator(posyandu_schedules, 8)  # 8 items per page
        page_number_schedules = self.request.GET.get('page_schedules', 1)
        page_obj_schedules = paginator_schedules.get_page(page_number_schedules)
        
        context['posyandu_schedules'] = page_obj_schedules
        context['page_obj_schedules'] = page_obj_schedules
        
        return context


@csrf_exempt
def api_document_types(request):
    """API endpoint for document types"""
    if request.method == 'GET':
        document_types = LayananDocumentRequest.DOCUMENT_TYPE_CHOICES
        data = {
            'success': True,
            'document_types': [
                {'value': choice[0], 'label': choice[1]} 
                for choice in document_types
            ]
        }
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def api_request_status(request):
    """API endpoint for request status"""
    if request.method == 'GET':
        nik = request.GET.get('nik', '')
        
        if nik:
            requests = LayananDocumentRequest.objects.filter(nik=nik).order_by('-created_at')
            data = {
                'success': True,
                'requests': [
                    {
                        'id': req.id,
                        'document_type': req.get_document_type_display(),
                        'status': req.get_status_display(),
                        'created_at': req.created_at.strftime('%d %B %Y'),
                        'purpose': req.purpose
                    }
                    for req in requests
                ]
            }
        else:
            data = {
                'success': False,
                'message': 'NIK tidak ditemukan'
            }
        
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


# ===========================
# LETTER SERVICES VIEWS
# ===========================

class LetterServicesView(TemplateView):
    """Letter services listing page"""
    template_name = 'public/layanan/letter_services.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            # Get all active letter types
            context['letter_types'] = LetterType.objects.filter(is_active=True).order_by('name')
            context['letter_types_count'] = context['letter_types'].count()
        else:
            context['letter_types'] = []
            context['letter_types_count'] = 0
        
        return context


class LetterRequestView(TemplateView):
    """Letter request form page"""
    template_name = 'public/layanan/letter_request.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            # Get all active letter types
            context['letter_types'] = LetterType.objects.filter(is_active=True).order_by('name')
            
            # Get selected letter type from URL parameter
            letter_type_id = self.request.GET.get('type')
            if letter_type_id:
                try:
                    context['selected_letter_type'] = LetterType.objects.get(id=letter_type_id, is_active=True)
                except LetterType.DoesNotExist:
                    context['selected_letter_type'] = None
        else:
            context['letter_types'] = []
            context['selected_letter_type'] = None
        
        return context
    
    def post(self, request, *args, **kwargs):
        """Handle letter submission"""
        if not LETTERS_AVAILABLE:
            messages.error(request, 'Layanan surat menyurat sedang tidak tersedia.')
            return redirect('layanan:letter_services')
        
        try:
            # Get form data
            full_name = request.POST.get('full_name')
            nik = request.POST.get('nik')
            phone = request.POST.get('phone')
            email = request.POST.get('email', '')
            address = request.POST.get('address')
            letter_type_id = request.POST.get('letter_type')
            subject = request.POST.get('subject')
            purpose = request.POST.get('purpose')
            content = request.POST.get('content')
            notes = request.POST.get('notes', '')
            priority = request.POST.get('priority', 'normal')
            
            # Validate required fields
            if not all([full_name, nik, phone, address, letter_type_id, subject, purpose, content]):
                messages.error(request, 'Mohon lengkapi semua field yang wajib diisi.')
                return redirect('layanan:letter_request')
            
            # Get letter type
            try:
                letter_type = LetterType.objects.get(id=letter_type_id, is_active=True)
            except LetterType.DoesNotExist:
                messages.error(request, 'Jenis surat tidak valid.')
                return redirect('layanan:letter_services')
            
            # Create or get applicant (using Penduduk model from references app)
            from references.models import Penduduk
            applicant, created = Penduduk.objects.get_or_create(
                nik=nik,
                defaults={
                    'name': full_name,
                    'phone_number': phone,
                    'email': email,
                    'address': address
                }
            )
            
            # Create letter
            letter = Letter.objects.create(
                letter_type=letter_type,
                applicant=applicant,
                subject=subject,
                content=content,
                purpose=purpose,
                priority=priority,
                notes=notes,
                status='submitted'
            )
            
            # Handle file uploads
            if 'ktp_file' in request.FILES:
                LetterAttachment.objects.create(
                    letter=letter,
                    file=request.FILES['ktp_file'],
                    attachment_type='ktp',
                    description='Fotokopi KTP'
                )
            
            if 'kk_file' in request.FILES:
                LetterAttachment.objects.create(
                    letter=letter,
                    file=request.FILES['kk_file'],
                    attachment_type='kk',
                    description='Fotokopi KK'
                )
            
            if 'additional_file' in request.FILES:
                LetterAttachment.objects.create(
                    letter=letter,
                    file=request.FILES['additional_file'],
                    attachment_type='additional',
                    description='Dokumen tambahan'
                )
            
            # Create tracking record
            LetterTracking.objects.create(
                letter=letter,
                status='submitted',
                notes='Surat diajukan melalui website'
            )
            
            messages.success(request, f'Surat berhasil diajukan dengan nomor: {letter.letter_number}')
            return redirect('layanan:letter_status')
            
        except Exception as e:
            messages.error(request, f'Terjadi kesalahan: {str(e)}')
            return redirect('layanan:letter_request')


class LetterStatusView(TemplateView):
    """Letter status check page"""
    template_name = 'public/layanan/letter_status.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            # Check if search was performed
            letter_number = self.request.GET.get('letter_number', '').strip()
            nik = self.request.GET.get('nik', '').strip()
            
            context['search_performed'] = bool(letter_number or nik)
            context['letters'] = []
            
            if context['search_performed']:
                # Search for letters
                letters_query = Letter.objects.all()
                
                if letter_number:
                    letters_query = letters_query.filter(letter_number__icontains=letter_number)
                
                if nik:
                    letters_query = letters_query.filter(applicant__nik__icontains=nik)
                
                context['letters'] = letters_query.order_by('-created_at')[:10]
        else:
            context['search_performed'] = False
            context['letters'] = []
        
        return context


class LetterHistoryView(TemplateView):
    """Letter history page"""
    template_name = 'public/layanan/letter_history.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            # Get letters by NIK (if provided)
            nik = self.request.GET.get('nik', '').strip()
            
            if nik:
                context['letters'] = Letter.objects.filter(
                    applicant__nik__icontains=nik
                ).order_by('-created_at')
                context['search_performed'] = True
            else:
                context['letters'] = []
                context['search_performed'] = False
        else:
            context['letters'] = []
            context['search_performed'] = False
        
        return context


class LetterGuidelinesView(TemplateView):
    """Letter guidelines page"""
    template_name = 'public/layanan/letter_guidelines.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            context['letter_types'] = LetterType.objects.filter(is_active=True).order_by('name')
        else:
            context['letter_types'] = []
        
        return context


class LetterFAQView(TemplateView):
    """Letter FAQ page"""
    template_name = 'public/layanan/letter_faq.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        if LETTERS_AVAILABLE:
            context['letter_types'] = LetterType.objects.filter(is_active=True).order_by('name')
        else:
            context['letter_types'] = []
        
        return context


def letter_download(request, letter_id):
    """Download completed letter"""
    if not LETTERS_AVAILABLE:
        messages.error(request, 'Layanan surat menyurat sedang tidak tersedia.')
        return redirect('layanan:letter_services')
    
    try:
        letter = get_object_or_404(Letter, id=letter_id, status='completed')
        
        # Check if letter has generated file
        if hasattr(letter, 'generated_file') and letter.generated_file:
            from django.http import FileResponse
            return FileResponse(
                letter.generated_file.open(),
                as_attachment=True,
                filename=f"{letter.letter_number}.pdf"
            )
        else:
            messages.error(request, 'File surat belum tersedia.')
            return redirect('layanan:letter_status')
            
    except Exception as e:
        messages.error(request, f'Terjadi kesalahan: {str(e)}')
        return redirect('layanan:letter_status')


# ===========================
# LETTER API ENDPOINTS
# ===========================

@csrf_exempt
def api_letter_types(request):
    """API endpoint for letter types"""
    if request.method == 'GET':
        if LETTERS_AVAILABLE:
            letter_types = LetterType.objects.filter(is_active=True).order_by('name')
            data = {
                'success': True,
                'letter_types': [
                    {
                        'id': lt.id,
                        'name': lt.name,
                        'code': lt.code,
                        'description': lt.description,
                        'processing_time_days': lt.processing_time_days,
                        'fee_amount': float(lt.fee_amount)
                    }
                    for lt in letter_types
                ]
            }
        else:
            data = {
                'success': False,
                'message': 'Layanan surat menyurat tidak tersedia'
            }
        
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)


@csrf_exempt
def api_letter_status(request):
    """API endpoint for letter status"""
    if request.method == 'GET':
        if not LETTERS_AVAILABLE:
            return JsonResponse({
                'success': False,
                'message': 'Layanan surat menyurat tidak tersedia'
            })
        
        letter_number = request.GET.get('letter_number', '').strip()
        nik = request.GET.get('nik', '').strip()
        
        if letter_number or nik:
            letters_query = Letter.objects.all()
            
            if letter_number:
                letters_query = letters_query.filter(letter_number__icontains=letter_number)
            
            if nik:
                letters_query = letters_query.filter(applicant__nik__icontains=nik)
            
            letters = letters_query.order_by('-created_at')[:10]
            
            data = {
                'success': True,
                'letters': [
                    {
                        'id': letter.id,
                        'letter_number': letter.letter_number,
                        'letter_type': letter.letter_type.name if letter.letter_type else 'N/A',
                        'subject': letter.subject,
                        'status': letter.get_status_display(),
                        'status_code': letter.status,
                        'created_at': letter.created_at.strftime('%d %B %Y, %H:%M'),
                        'applicant_name': letter.applicant.nama if hasattr(letter.applicant, 'nama') else str(letter.applicant)
                    }
                    for letter in letters
                ]
            }
        else:
            data = {
                'success': False,
                'message': 'Nomor surat atau NIK harus diisi'
            }
        
        return JsonResponse(data)
    
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
