"""
URLs untuk Admin Panel Sistem Surat
"""

from django.urls import path, include
from . import admin_views

app_name = 'letters'

urlpatterns = [
    # Dashboard
    path('dashboard/', admin_views.admin_dashboard, name='admin_dashboard'),

    # Letter Management (All Letters)
    path('', admin_views.letter_list, name='admin_letter_list'),
    path('create/', admin_views.letter_create, name='admin_letter_create'),
    path('<int:letter_id>/', admin_views.letter_detail, name='admin_letter_detail'),
    path('<int:letter_id>/preview/', admin_views.letter_preview, name='admin_letter_preview'),
    path('<int:letter_id>/edit/', admin_views.letter_edit, name='admin_letter_edit'),
    path('<int:letter_id>/delete/', admin_views.letter_delete, name='admin_letter_delete'),

    # Letter Requests (Surat Masuk)
    path('requests/', admin_views.letter_request_list, name='letter_request_list'),
    path('requests/create/', admin_views.letter_request_create, name='letter_request_create'),
    path('requests/<int:request_id>/', admin_views.letter_request_detail, name='letter_request_detail'),
    path('requests/<int:request_id>/edit/', admin_views.letter_request_edit, name='letter_request_edit'),

    # Outgoing Letters (Surat Keluar)
    path('outgoing/', admin_views.outgoing_letters_list, name='outgoing_letters_list'),

    # Letter Types Management
    path('types/', admin_views.letter_type_list, name='admin_letter_type_list'),
    path('types/create/', admin_views.letter_type_create, name='admin_letter_type_create'),
    path('types/<int:type_id>/edit/', admin_views.letter_type_edit, name='admin_letter_type_edit'),

    # Template Management
    path('templates/', admin_views.template_list, name='admin_template_list'),
    path('templates/editor/', admin_views.template_editor, name='template_editor'),
    path('templates/editor/<int:template_id>/', admin_views.template_editor, name='template_editor_edit'),

    # Document Management
    path('<int:letter_id>/upload/', admin_views.document_upload, name='document_upload'),

    # Settings
    path('settings/', admin_views.settings_view, name='admin_settings'),

    # Print
    path('print/<int:letter_id>/<str:format_type>/', admin_views.letter_print, name='admin_letter_print'),

    # Analytics
    path('analytics/', admin_views.analytics_view, name='admin_analytics'),

    # API Endpoints
    path('api/print/<int:letter_id>/', admin_views.api_letter_print, name='api_letter_print'),
    path('api/bulk-action/', admin_views.api_bulk_action, name='api_bulk_action'),
    path('api/upload-document/', admin_views.api_upload_document, name='api_upload_document'),
    path('api/generate-from-template/', admin_views.api_generate_letter_from_template, name='api_generate_from_template'),
]
