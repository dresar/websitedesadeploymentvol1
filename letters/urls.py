from django.urls import path, re_path, include
from . import views

app_name = 'letters'

urlpatterns = [
    # Public routes for document services
    path('', views.document_services, name='document_services'),
    path('info/<int:document_type_id>/', views.document_info, name='document_info'),
    path('info/', views.document_services, name='document_info_list'),
    re_path(r'info/(?P<document_type_id>\d+)/$', views.document_info, name='document_info_alt'),

    path('request/', views.document_request, name='document_request'),
    path('request/<int:document_type_id>/', views.document_request, name='document_request_type'),
    re_path(r'request/(?P<document_type_id>\d+)/$', views.document_request, name='document_request_type_alt'),

    path('status/', views.request_status, name='request_status'),
    path('detail/<int:letter_id>/', views.letter_detail, name='letter_detail'),
    path('chat/', views.chat_layanan, name='chat_layanan'),

    # API Endpoints for public use
    path('api/document-types/', views.api_document_types, name='api_document_types'),
    path('api/search-residents/', views.api_search_residents, name='api_search_residents'),
    path('api/submit-request/', views.api_submit_request, name='api_submit_request'),
    path('api/request-status/', views.api_request_status, name='api_request_status'),
    path('api/request-status/<int:request_id>/', views.api_request_detail, name='api_request_detail'),
    path('api/chat/', views.api_chat_message, name='api_chat_message'),

    # Print endpoints for public use
    path('print/<int:letter_id>/<str:format_type>/', views.admin_letter_print, name='admin_letter_print'),
    path('api/print/<int:letter_id>/', views.api_letter_print, name='api_letter_print'),

    # Admin panel routes
    path('admin/', include('letters.admin_urls')),
]