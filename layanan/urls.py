from django.urls import path
from . import views

app_name = 'layanan'

urlpatterns = [
    # Main pages
    path('', views.LayananIndexView.as_view(), name='index'),
    path('keluhan/', views.ComplaintServicesView.as_view(), name='complaint_services'),
    
    # Document services - redirect to letters system
    path('dokumen/', views.DocumentServicesView.as_view(), name='document_services'),
    path('dokumen/ajukan/', views.DocumentRequestView.as_view(), name='document_request'),
    path('dokumen/status/', views.RequestStatusView.as_view(), name='request_status'),
    
    # Other services
    path('posyandu/', views.PosyanduServicesView.as_view(), name='posyandu_services'),
    path('bisnis/', views.BusinessServicesView.as_view(), name='business_services'),
    path('wisata/', views.TourismServicesView.as_view(), name='tourism_services'),
    
    # Letter services
    path('surat/', views.LetterServicesView.as_view(), name='letter_services'),
    path('surat/ajukan/', views.LetterRequestView.as_view(), name='letter_request'),
    path('surat/status/', views.LetterStatusView.as_view(), name='letter_status'),
    path('surat/riwayat/', views.LetterHistoryView.as_view(), name='letter_history'),
    path('surat/panduan/', views.LetterGuidelinesView.as_view(), name='letter_guidelines'),
    path('surat/faq/', views.LetterFAQView.as_view(), name='letter_faq'),
    path('surat/download/<int:letter_id>/', views.letter_download, name='letter_download'),
    
    # API endpoints
    path('api/document-types/', views.api_document_types, name='api_document_types'),
    path('api/request-status/', views.api_request_status, name='api_request_status'),
    path('api/letter-types/', views.api_letter_types, name='api_letter_types'),
    path('api/letter-status/', views.api_letter_status, name='api_letter_status'),
]




