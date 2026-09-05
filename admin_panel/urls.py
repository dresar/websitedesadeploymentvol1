from django.urls import path, include
from django.contrib.auth import views as auth_views
from . import admin_views
from .export_import import PendudukExportView, PendudukImportView
from . import export_import
from . import template_generators
from village_profile import admin_views as village_profile_views
from beneficiaries import views as beneficiaries_views
from business import admin_views as business_views
from complaints import views as complaints_views
from documents import views as documents_views
from tourism import views as tourism_views
from posyandu import views as posyandu_public_views
from posyandu import patient_type_views as posyandu_patient_type_views
from news import views as news_views
from references import views as references_views

app_name = 'admin_panel'

urlpatterns = [
    # Authentication URLs
    path('login/', admin_views.custom_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
    # Main Dashboard
    path('', admin_views.admin_dashboard, name='dashboard'),
    
    # Beneficiaries URLs
    path('beneficiaries/', beneficiaries_views.admin_beneficiaries_dashboard, name='beneficiaries_dashboard'),
    path('beneficiaries/list/', beneficiaries_views.admin_beneficiaries_list, name='beneficiaries_list'),
    path('beneficiaries/create/', beneficiaries_views.admin_beneficiary_create, name='beneficiary_create'),
    path('beneficiaries/<int:pk>/', beneficiaries_views.admin_beneficiary_detail, name='beneficiary_detail'),
    path('beneficiaries/<int:pk>/edit/', beneficiaries_views.admin_beneficiary_update, name='beneficiary_edit'),
    path('beneficiaries/<int:pk>/update/', beneficiaries_views.admin_beneficiary_update, name='beneficiary_update'),
    path('beneficiaries/<int:pk>/delete/', beneficiaries_views.admin_beneficiary_delete, name='beneficiary_delete'),
    path('beneficiaries/bulk-delete/', beneficiaries_views.admin_bulk_update_status, name='beneficiaries_bulk_delete'),
    path('beneficiaries/bulk-activate/', beneficiaries_views.admin_bulk_update_status, name='beneficiaries_bulk_activate'),
    path('beneficiaries/bulk-deactivate/', beneficiaries_views.admin_bulk_update_status, name='beneficiaries_bulk_deactivate'),
    path('beneficiaries/bulk-verify/', beneficiaries_views.admin_bulk_verify, name='beneficiaries_bulk_verify'),
    path('beneficiaries/export/excel/', beneficiaries_views.admin_export_beneficiaries_excel, name='beneficiaries_export_excel'),
    path('beneficiaries/export/pdf/', beneficiaries_views.admin_export_beneficiaries_pdf, name='beneficiaries_export_pdf'),
    path('beneficiaries/import/', beneficiaries_views.admin_beneficiaries_list, name='beneficiaries_import'),
    path('beneficiaries/search/', beneficiaries_views.admin_beneficiaries_list, name='beneficiaries_search'),
    path('beneficiaries/stats/', beneficiaries_views.admin_beneficiaries_list, name='beneficiaries_stats'),
    path('beneficiaries/reports/', beneficiaries_views.admin_beneficiaries_reports, name='beneficiaries_reports'),
    path('beneficiaries/analytics/', beneficiaries_views.admin_beneficiaries_reports, name='beneficiaries_analytics'),
    path('beneficiaries/categories/', beneficiaries_views.admin_categories_list, name='beneficiaries_categories'),
    path('beneficiaries/categories/list/', beneficiaries_views.admin_categories_list, name='categories_list'),
    path('beneficiaries/categories/create/', beneficiaries_views.admin_category_create, name='beneficiaries_category_create'),
    path('beneficiaries/categories/<int:pk>/edit/', beneficiaries_views.admin_category_update, name='beneficiaries_category_edit'),
    path('beneficiaries/categories/<int:pk>/delete/', beneficiaries_views.admin_category_delete, name='beneficiaries_category_delete'),
    path('beneficiaries/aid-programs/', beneficiaries_views.admin_aid_programs_list, name='beneficiaries_aid_programs'),
    path('beneficiaries/aid-programs/create/', beneficiaries_views.admin_aid_program_create, name='beneficiaries_aid_program_create'),
    path('beneficiaries/aid-programs/<int:pk>/edit/', beneficiaries_views.admin_aid_program_update, name='beneficiaries_aid_program_edit'),
    path('beneficiaries/aid-programs/<int:pk>/delete/', beneficiaries_views.admin_aid_program_delete, name='beneficiaries_aid_program_delete'),
    path('beneficiaries/distributions/', beneficiaries_views.admin_distributions_list, name='beneficiaries_distributions'),
    path('beneficiaries/distributions/create/', beneficiaries_views.admin_distribution_create, name='beneficiaries_distribution_create'),
    path('beneficiaries/distributions/<int:pk>/update-status/', beneficiaries_views.admin_distribution_update_status, name='beneficiaries_distribution_update_status'),
    path('beneficiaries/verifications/', beneficiaries_views.admin_verifications_list, name='beneficiaries_verifications'),
    path('beneficiaries/verifications/<int:pk>/update/', beneficiaries_views.admin_verification_update, name='beneficiaries_verification_update'),
    path('beneficiaries/verifications/<int:pk>/detail/', beneficiaries_views.admin_verification_detail, name='beneficiaries_verification_detail'),
    path('beneficiaries/verifications/bulk-action/', beneficiaries_views.admin_verification_bulk_action, name='beneficiaries_verification_bulk_action'),
    path('api/beneficiaries/search/', beneficiaries_views.api_beneficiary_search, name='api_beneficiaries_search'),
    path('api/beneficiaries/stats/', beneficiaries_views.api_beneficiary_stats, name='api_beneficiaries_stats'),
    
    # Aid Distribution URLs
    path('beneficiaries/aid-distributions/', beneficiaries_views.admin_distributions_list, name='aid_distributions_list'),
    path('beneficiaries/aid-distributions/create/', beneficiaries_views.admin_distribution_create, name='aid_distribution_create'),
    path('beneficiaries/aid-distributions/<int:pk>/', beneficiaries_views.admin_distribution_detail, name='aid_distribution_detail'),
    path('beneficiaries/aid-distributions/<int:pk>/edit/', beneficiaries_views.admin_distribution_update, name='aid_distribution_update'),
    path('beneficiaries/aid-distributions/<int:pk>/delete/', beneficiaries_views.aid_distribution_delete, name='aid_distribution_delete'),
    path('beneficiaries/aid-distributions/check/', beneficiaries_views.aid_distribution_check, name='aid_distribution_check'),
    
    # Category URLs
    path('beneficiaries/categories/', beneficiaries_views.admin_categories_list, name='categories_list'),
    path('beneficiaries/categories/create/', beneficiaries_views.admin_category_create, name='category_create'),
    path('beneficiaries/categories/<int:pk>/', beneficiaries_views.admin_category_detail, name='category_detail'),
    path('beneficiaries/categories/<int:pk>/edit/', beneficiaries_views.admin_category_update, name='category_update'),
    path('beneficiaries/categories/<int:pk>/delete/', beneficiaries_views.admin_category_delete, name='category_delete'),
    
    # References URLs
    path('references/penduduk/list/', admin_views.references_penduduk_list, name='references_penduduk_list'),
    path('references/penduduk/add/', admin_views.references_penduduk_add, name='references_penduduk_add'),
    path('references/penduduk/edit/<int:penduduk_id>/', admin_views.references_penduduk_edit, name='references_penduduk_edit'),
    path('references/penduduk/update/<int:penduduk_id>/', admin_views.references_penduduk_update, name='references_penduduk_update'),
    path('references/penduduk/delete/<int:penduduk_id>/', admin_views.references_penduduk_delete, name='references_penduduk_delete'),
    path('references/penduduk/detail/<int:penduduk_id>/', admin_views.references_penduduk_detail, name='references_penduduk_detail'),
    path('references/penduduk/export/excel/', admin_views.references_penduduk_export_excel, name='references_penduduk_export_excel'),
    path('references/penduduk/export/csv/', admin_views.references_penduduk_export_csv, name='references_penduduk_export_csv'),
    path('references/penduduk/export/json/', admin_views.references_penduduk_export_json, name='references_penduduk_export_json'),
    path('references/penduduk/export/pdf/', admin_views.references_penduduk_export_pdf, name='references_penduduk_export_pdf'),
    path('references/penduduk/bulk-action/', admin_views.references_bulk_action, name='references_bulk_action'),
    path('references/penduduk/bulk-delete/', admin_views.references_penduduk_bulk_delete, name='references_penduduk_bulk_delete'),
    path('references/penduduk/bulk-activate/', admin_views.references_penduduk_bulk_activate, name='references_penduduk_bulk_activate'),
    path('references/penduduk/bulk-deactivate/', admin_views.references_penduduk_bulk_deactivate, name='references_penduduk_bulk_deactivate'),
    path('references/quick-import/<str:model_name>/', admin_views.references_quick_import, name='references_quick_import'),
    path('references/penduduk/save/', admin_views.references_penduduk_save, name='references_penduduk_save'),
    path('references/pelajar/add/', admin_views.references_pelajar_add, name='references_pelajar_add'),
    path('references/pelajar/update/<int:pelajar_id>/', admin_views.references_pelajar_update, name='references_pelajar_update'),
    path('references/pelajar/export/excel/', admin_views.references_pelajar_export_excel, name='references_pelajar_export_excel'),
    path('references/pelajar/export/csv/', admin_views.references_pelajar_export_csv, name='references_pelajar_export_csv'),
    path('references/pelajar/export/json/', admin_views.references_pelajar_export_json, name='references_pelajar_export_json'),
    path('references/pelajar/export/pdf/', admin_views.references_pelajar_export_pdf, name='references_pelajar_export_pdf'),
    path('api/references/dusun/list/', admin_views.api_references_dusun_list, name='api_references_dusun_list'),
    path('api/references/lorong/', admin_views.api_references_lorong_list, name='api_references_lorong_list'),
    path('api/references/lorong/by-dusun/', admin_views.api_references_lorong_by_dusun, name='api_references_lorong_by_dusun'),
    path('api/references/rw/by-dusun/<int:dusun_id>/', admin_views.api_references_rw_by_dusun, name='api_references_rw_by_dusun'),
    path('api/references/rt/by-rw/<int:rw_id>/', admin_views.api_references_rt_by_rw, name='api_references_rt_by_rw'),
    path('api/references/residents/search/', admin_views.api_references_residents_search, name='api_references_residents_search'),
    path('api/references/penduduk-by-dusun/<int:dusun_id>/', admin_views.api_references_penduduk_by_dusun, name='api_references_penduduk_by_dusun'),
    path('api/references/keluarga/', admin_views.api_references_keluarga_list, name='api_references_keluarga_list'),
    path('api/penduduk/search/', admin_views.api_penduduk_search, name='api_penduduk_search'),
    path('references/dusun/list/', admin_views.references_dusun_list, name='references_dusun_list'),
    path('references/dusun/add/', admin_views.references_dusun_add, name='references_dusun_add'),
    path('references/dusun/edit/<int:dusun_id>/', admin_views.references_dusun_edit, name='references_dusun_edit'),
    path('references/dusun/update/<int:dusun_id>/', admin_views.references_dusun_update, name='references_dusun_update'),
    path('references/dusun/delete/<int:dusun_id>/', admin_views.references_dusun_delete, name='references_dusun_delete'),
    path('references/dusun/detail/<int:dusun_id>/', admin_views.references_dusun_detail, name='references_dusun_detail'),
    path('references/dusun/export/excel/', admin_views.references_dusun_export_excel, name='references_dusun_export_excel'),
    path('references/dusun/export/csv/', admin_views.references_dusun_export_csv, name='references_dusun_export_csv'),
    path('references/dusun/export/json/', admin_views.references_dusun_export_json, name='references_dusun_export_json'),
    path('references/dusun/export/pdf/', admin_views.references_dusun_export_pdf, name='references_dusun_export_pdf'),
    path('references/dusun/bulk-delete/', admin_views.references_dusun_bulk_delete, name='references_dusun_bulk_delete'),
    path('references/dusun/bulk-activate/', admin_views.references_dusun_bulk_activate, name='references_dusun_bulk_activate'),
    path('references/dusun/bulk-deactivate/', admin_views.references_dusun_bulk_deactivate, name='references_dusun_bulk_deactivate'),
    path('references/lorong/list/', admin_views.references_lorong_list, name='references_lorong_list'),
    path('references/lorong/add/', admin_views.references_lorong_add, name='references_lorong_add'),
    path('references/lorong/edit/<int:lorong_id>/', admin_views.references_lorong_edit, name='references_lorong_edit'),
    path('references/lorong/update/<int:lorong_id>/', admin_views.references_lorong_update, name='references_lorong_update'),
    path('references/lorong/delete/<int:lorong_id>/', admin_views.references_lorong_delete, name='references_lorong_delete'),
    path('references/lorong/detail/<int:lorong_id>/', admin_views.references_lorong_detail, name='references_lorong_detail'),
    path('references/lorong/export/excel/', admin_views.references_lorong_export_excel, name='references_lorong_export_excel'),
    path('references/lorong/export/csv/', admin_views.references_lorong_export_csv, name='references_lorong_export_csv'),
    path('references/lorong/export/json/', admin_views.references_lorong_export_json, name='references_lorong_export_json'),
    path('references/lorong/export/pdf/', admin_views.references_lorong_export_pdf, name='references_lorong_export_pdf'),
    path('references/lorong/bulk-delete/', admin_views.references_lorong_bulk_delete, name='references_lorong_bulk_delete'),
    path('references/lorong/bulk-activate/', admin_views.references_lorong_bulk_activate, name='references_lorong_bulk_activate'),
    path('references/lorong/bulk-deactivate/', admin_views.references_lorong_bulk_deactivate, name='references_lorong_bulk_deactivate'),
    path('references/rw/list/', admin_views.references_rw_list, name='references_rw_list'),
    path('references/rw/add/', admin_views.references_rw_add, name='references_rw_add'),
    path('references/rw/edit/<int:rw_id>/', admin_views.references_rw_edit, name='references_rw_edit'),
    path('references/rw/update/<int:rw_id>/', admin_views.references_rw_update, name='references_rw_update'),
    path('references/rw/delete/<int:rw_id>/', admin_views.references_rw_delete, name='references_rw_delete'),
    path('references/rw/detail/<int:rw_id>/', admin_views.references_rw_detail, name='references_rw_detail'),
    path('references/rw/export/excel/', admin_views.references_rw_export_excel, name='references_rw_export_excel'),
    path('references/rw/export/csv/', admin_views.references_rw_export_csv, name='references_rw_export_csv'),
    path('references/rw/export/json/', admin_views.references_rw_export_json, name='references_rw_export_json'),
    path('references/rw/export/pdf/', admin_views.references_rw_export_pdf, name='references_rw_export_pdf'),
    path('references/rw/bulk-delete/', admin_views.references_rw_bulk_delete, name='references_rw_bulk_delete'),
    path('references/rw/bulk-activate/', admin_views.references_rw_bulk_activate, name='references_rw_bulk_activate'),
    path('references/rw/bulk-deactivate/', admin_views.references_rw_bulk_deactivate, name='references_rw_bulk_deactivate'),
    path('references/rt/list/', admin_views.references_rt_list, name='references_rt_list'),
    path('references/rt/add/', admin_views.references_rt_add, name='references_rt_add'),
    path('references/rt/edit/<int:rt_id>/', admin_views.references_rt_edit, name='references_rt_edit'),
    path('references/rt/update/<int:rt_id>/', admin_views.references_rt_update, name='references_rt_update'),
    path('references/rt/delete/<int:rt_id>/', admin_views.references_rt_delete, name='references_rt_delete'),
    path('references/rt/detail/<int:rt_id>/', admin_views.references_rt_detail, name='references_rt_detail'),
    path('references/rt/export/excel/', admin_views.references_rt_export_excel, name='references_rt_export_excel'),
    path('references/rt/export/csv/', admin_views.references_rt_export_csv, name='references_rt_export_csv'),
    path('references/rt/export/json/', admin_views.references_rt_export_json, name='references_rt_export_json'),
    path('references/rt/export/pdf/', admin_views.references_rt_export_pdf, name='references_rt_export_pdf'),
    path('references/rt/bulk-delete/', admin_views.references_rt_bulk_delete, name='references_rt_bulk_delete'),
    path('references/rt/bulk-activate/', admin_views.references_rt_bulk_activate, name='references_rt_bulk_activate'),
    path('references/rt/bulk-deactivate/', admin_views.references_rt_bulk_deactivate, name='references_rt_bulk_deactivate'),
    path('references/disabilitas/list/', admin_views.references_disabilitas_list, name='references_disabilitas_list'),
    path('references/disabilitas/add/', admin_views.references_disabilitas_add, name='references_disabilitas_add'),
    path('references/disabilitas/edit/<int:disabilitas_id>/', admin_views.references_disabilitas_edit, name='references_disabilitas_edit'),
    path('references/disabilitas/update/<int:disabilitas_id>/', admin_views.references_disabilitas_update, name='references_disabilitas_update'),
    path('references/disabilitas/delete/<int:disabilitas_id>/', admin_views.references_disabilitas_delete, name='references_disabilitas_delete'),
    path('references/disabilitas/detail/<int:disabilitas_id>/', admin_views.references_disabilitas_detail, name='references_disabilitas_detail'),
    path('references/disabilitas/export/excel/', admin_views.references_disabilitas_export_excel, name='references_disabilitas_export_excel'),
    path('references/disabilitas/export/csv/', admin_views.references_disabilitas_export_csv, name='references_disabilitas_export_csv'),
    path('references/disabilitas/export/json/', admin_views.references_disabilitas_export_json, name='references_disabilitas_export_json'),
    path('references/disabilitas/export/pdf/', admin_views.references_disabilitas_export_pdf, name='references_disabilitas_export_pdf'),
    path('references/disabilitas/bulk-delete/', admin_views.references_disabilitas_bulk_delete, name='references_disabilitas_bulk_delete'),
    path('references/disabilitas/bulk-activate/', admin_views.references_disabilitas_bulk_activate, name='references_disabilitas_bulk_activate'),
    path('references/disabilitas/bulk-deactivate/', admin_views.references_disabilitas_bulk_deactivate, name='references_disabilitas_bulk_deactivate'),
    path('references/pelajar/list/', admin_views.references_pelajar_list, name='references_pelajar_list'),
    path('references/pelajar/detail/<int:pelajar_id>/', admin_views.references_pelajar_detail, name='references_pelajar_detail'),
    path('references/pelajar/edit/<int:pelajar_id>/', admin_views.references_pelajar_edit, name='references_pelajar_edit'),
    path('references/pelajar/delete/<int:pelajar_id>/', admin_views.references_pelajar_delete, name='references_pelajar_delete'),
    path('references/pelajar/bulk-delete/', admin_views.references_pelajar_bulk_delete, name='references_pelajar_bulk_delete'),
    path('references/pelajar/bulk-activate/', admin_views.references_pelajar_bulk_activate, name='references_pelajar_bulk_activate'),
    path('references/pelajar/bulk-deactivate/', admin_views.references_pelajar_bulk_deactivate, name='references_pelajar_bulk_deactivate'),
    path('references/keluarga/list/', admin_views.references_keluarga_list, name='references_keluarga_list'),
    path('references/keluarga/add/', admin_views.references_keluarga_add, name='references_keluarga_add'),
    path('references/keluarga/edit/<int:keluarga_id>/', admin_views.references_keluarga_edit, name='references_keluarga_edit'),
    path('references/keluarga/update/<int:keluarga_id>/', admin_views.references_keluarga_update, name='references_keluarga_update'),
    path('references/keluarga/delete/<int:keluarga_id>/', admin_views.references_keluarga_delete, name='references_keluarga_delete'),
    path('references/keluarga/detail/<int:keluarga_id>/', admin_views.references_keluarga_detail, name='references_keluarga_detail'),
    path('references/keluarga/export/excel/', admin_views.references_keluarga_export_excel, name='references_keluarga_export_excel'),
    path('references/keluarga/export/csv/', admin_views.references_keluarga_export_csv, name='references_keluarga_export_csv'),
    path('references/keluarga/export/json/', admin_views.references_keluarga_export_json, name='references_keluarga_export_json'),
    path('references/keluarga/export/pdf/', admin_views.references_keluarga_export_pdf, name='references_keluarga_export_pdf'),
    path('references/keluarga/bulk-delete/', admin_views.references_keluarga_bulk_delete, name='references_keluarga_bulk_delete'),
    path('references/keluarga/bulk-activate/', admin_views.references_keluarga_bulk_activate, name='references_keluarga_bulk_activate'),
    path('references/keluarga/bulk-deactivate/', admin_views.references_keluarga_bulk_deactivate, name='references_keluarga_bulk_deactivate'),
    path('references/keluarga/update-anggota/<int:keluarga_id>/', admin_views.references_keluarga_update_anggota, name='references_keluarga_update_anggota'),
    
    path('business/', admin_views.business_dashboard, name='business_dashboard'),
    
    # UMKM URLs
    path('business/umkm/list/', admin_views.umkm_list, name='umkm_list'),
    path('business/umkm/create/', admin_views.umkm_create, name='umkm_create'),
    path('business/umkm/<int:umkm_id>/', admin_views.umkm_detail, name='umkm_detail'),
    path('business/umkm/<int:umkm_id>/edit/', admin_views.umkm_edit, name='umkm_edit'),
    path('business/umkm/<int:umkm_id>/update/', admin_views.umkm_update, name='umkm_update'),
    path('business/umkm/<int:umkm_id>/delete/', admin_views.umkm_delete, name='umkm_delete'),
    
    # Koperasi URLs
    path('business/koperasi/list/', admin_views.koperasi_list, name='koperasi_list'),
    path('business/koperasi/create/', admin_views.koperasi_create, name='koperasi_create'),
    path('business/koperasi/<int:koperasi_id>/', admin_views.koperasi_detail, name='koperasi_detail'),
    path('business/koperasi/<int:koperasi_id>/edit/', admin_views.koperasi_edit, name='koperasi_edit'),
    path('business/koperasi/<int:koperasi_id>/update/', admin_views.koperasi_update, name='koperasi_update'),
    path('business/koperasi/<int:koperasi_id>/delete/', admin_views.koperasi_delete, name='koperasi_delete'),
    
    # BUMG URLs
    path('business/bumg/list/', admin_views.bumg_list, name='bumg_list'),
    path('business/bumg/create/', admin_views.bumg_create, name='bumg_create'),
    path('business/bumg/<int:bumg_id>/', admin_views.bumg_detail, name='bumg_detail'),
    path('business/bumg/<int:bumg_id>/edit/', admin_views.bumg_edit, name='bumg_edit'),
    path('business/bumg/<int:bumg_id>/update/', admin_views.bumg_update, name='bumg_update'),
    path('business/bumg/<int:bumg_id>/delete/', admin_views.bumg_delete, name='bumg_delete'),
    
    # Layanan Jasa URLs
    path('business/layanan-jasa/list/', admin_views.layanan_jasa_list, name='layanan_jasa_list'),
    path('business/layanan-jasa/create/', admin_views.layanan_jasa_create, name='layanan_jasa_create'),
    path('business/layanan-jasa/<int:layanan_id>/', admin_views.layanan_jasa_detail, name='layanan_jasa_detail'),
    path('business/layanan-jasa/<int:layanan_id>/edit/', admin_views.layanan_jasa_edit, name='layanan_jasa_edit'),
    path('business/layanan-jasa/<int:layanan_id>/update/', admin_views.layanan_jasa_update, name='layanan_jasa_update'),
    path('business/layanan-jasa/<int:layanan_id>/delete/', admin_views.layanan_jasa_delete, name='layanan_jasa_delete'),
    
    # Business Categories URLs
    path('business/categories/list/', admin_views.business_categories_list, name='business_categories_list'),
    path('business/categories/create/', admin_views.business_category_create, name='business_category_create'),
    path('business/categories/<int:category_id>/', admin_views.business_category_detail, name='business_category_detail'),
    path('business/categories/<int:category_id>/edit/', admin_views.business_category_edit, name='business_category_edit'),
    path('business/categories/<int:category_id>/update/', admin_views.business_category_update, name='business_category_update'),
    path('business/categories/<int:category_id>/delete/', admin_views.business_category_delete, name='business_category_delete'),
    path('business/categories/<int:category_id>/delete/confirm/', admin_views.business_category_delete_confirm, name='business_category_delete_confirm'),
    
    # Business Registration URLs
    path('business/registrations/', business_views.business_registration_list, name='business_registration_list'),
    path('business/registrations/<int:registration_id>/', business_views.business_registration_detail, name='business_registration_detail'),
    path('business/registrations/<int:registration_id>/approve/', business_views.business_registration_approve, name='business_registration_approve'),
    path('business/registrations/<int:registration_id>/reject/', business_views.business_registration_reject, name='business_registration_reject'),
    path('business/registrations/<int:registration_id>/review/', business_views.business_registration_under_review, name='business_registration_under_review'),
    
    # Business API URLs
    path('business/api/penduduk-search/', admin_views.api_business_penduduk_search, name='api_business_penduduk_search'),
    path('business/api/umkm-search/', admin_views.api_business_umkm_search, name='api_business_umkm_search'),
    path('business/api/koperasi-search/', admin_views.api_business_koperasi_search, name='api_business_koperasi_search'),
    path('business/api/bumg-search/', admin_views.api_business_bumg_search, name='api_business_bumg_search'),
    path('business/api/layanan-search/', admin_views.api_business_layanan_search, name='api_business_layanan_search'),
    path('complaints/', admin_views.complaints_dashboard, name='complaints_dashboard'),
    path('complaints/list/', admin_views.complaints_list, name='complaints_list'),
    path('complaints/categories/list/', admin_views.complaint_categories_list, name='complaint_categories_list'),
    path('complaints/categories/create/', complaints_views.admin_category_create, name='complaint_category_create'),
    path('complaints/categories/<int:pk>/update/', complaints_views.admin_category_update, name='complaint_category_update'),
    path('complaints/categories/<int:pk>/delete/', complaints_views.admin_category_delete, name='complaint_category_delete'),
    path('complaints/<int:pk>/', admin_views.complaint_detail, name='complaint_detail'),
    path('complaints/<int:pk>/edit/', admin_views.complaint_edit, name='complaint_edit'),
    path('complaints/<int:pk>/update/', admin_views.complaint_update, name='complaint_update'),
    path('complaints/<int:pk>/delete/', admin_views.complaint_delete, name='complaint_delete'),
    path('complaints/<int:pk>/add-update/', admin_views.complaint_add_update, name='complaint_add_update'),
    path('complaints/<int:pk>/update-admin-notes/', complaints_views.complaint_update_admin_notes, name='complaint_update_admin_notes'),
    # Documents URLs - redirect to documents app
    path('documents/', documents_views.documents_dashboard, name='documents_dashboard'),
    path('documents/list/', documents_views.documents_list, name='documents_list'),
    path('documents/create/', documents_views.document_create, name='document_create'),
    path('documents/<int:pk>/', documents_views.document_detail, name='document_detail'),
    path('documents/<int:pk>/edit/', documents_views.document_edit, name='document_edit'),
    path('documents/<int:pk>/delete/', documents_views.document_delete, name='document_delete'),
    path('documents/<int:pk>/comment/', documents_views.document_comment_add, name='document_comment_add'),
    path('documents/<int:pk>/preview/', documents_views.document_preview, name='document_preview'),
    path('documents/categories/', documents_views.document_categories_list, name='document_categories_list'),
    path('documents/categories/create/', documents_views.document_category_create, name='document_category_create'),
    path('documents/categories/<int:pk>/edit/', documents_views.document_category_edit, name='document_category_edit'),
    path('documents/categories/<int:pk>/delete/', documents_views.document_category_delete, name='document_category_delete'),
    path('documents/api/stats/', documents_views.api_documents_stats, name='api_documents_stats'),
    # Tourism URLs
    path('tourism/', admin_views.tourism_dashboard, name='tourism_dashboard'),
    
    # Tourism Locations
    path('tourism/locations/', admin_views.tourism_locations_list, name='tourism_locations_list'),
    path('tourism/locations/create/', admin_views.tourism_location_create, name='tourism_location_create'),
    path('tourism/locations/<int:location_id>/', admin_views.tourism_location_detail, name='tourism_location_detail'),
    path('tourism/locations/<int:location_id>/edit/', admin_views.tourism_location_edit, name='tourism_location_edit'),
    path('tourism/locations/<int:location_id>/delete/', admin_views.tourism_location_delete, name='tourism_location_delete'),
    path('tourism/locations/<int:location_id>/toggle-status/', admin_views.tourism_location_toggle_status, name='tourism_location_toggle_status'),
    path('tourism/locations/<int:location_id>/toggle-featured/', admin_views.tourism_location_toggle_featured, name='tourism_location_toggle_featured'),
    
    # Tourism Categories
    path('tourism/categories/', admin_views.tourism_categories_list, name='tourism_categories_list'),
    path('tourism/categories/create/', admin_views.tourism_category_create, name='tourism_category_create'),
    path('tourism/categories/<int:category_id>/', admin_views.tourism_category_detail, name='tourism_category_detail'),
    path('tourism/categories/<int:category_id>/edit/', admin_views.tourism_category_edit, name='tourism_category_edit'),
    path('tourism/categories/<int:category_id>/delete/', admin_views.tourism_category_delete, name='tourism_category_delete'),
    
    # Tourism Packages
    path('tourism/packages/', admin_views.tourism_packages_list, name='tourism_packages_list'),
    path('tourism/packages/create/', admin_views.tourism_package_create, name='tourism_package_create'),
    path('tourism/packages/<int:package_id>/', admin_views.tourism_package_detail, name='tourism_package_detail'),
    path('tourism/packages/<int:package_id>/edit/', admin_views.tourism_package_edit, name='tourism_package_edit'),
    path('tourism/packages/<int:package_id>/delete/', admin_views.tourism_package_delete, name='tourism_package_delete'),
    
    # Tourism Events
    path('tourism/events/', admin_views.tourism_events_list, name='tourism_events_list'),
    path('tourism/events/create/', admin_views.tourism_event_create, name='tourism_event_create'),
    path('tourism/events/<int:event_id>/', admin_views.tourism_event_detail, name='tourism_event_detail'),
    path('tourism/events/<int:event_id>/edit/', admin_views.tourism_event_edit, name='tourism_event_edit'),
    path('tourism/events/<int:event_id>/delete/', admin_views.tourism_event_delete, name='tourism_event_delete'),
    
    # Tourism Reviews
    path('tourism/reviews/', admin_views.tourism_reviews_list, name='tourism_reviews_list'),
    path('tourism/reviews/<int:review_id>/', admin_views.tourism_review_detail, name='tourism_review_detail'),
    path('tourism/reviews/<int:review_id>/edit/', admin_views.tourism_review_edit, name='tourism_review_edit'),
    path('tourism/reviews/<int:review_id>/approve/', admin_views.tourism_review_approve, name='tourism_review_approve'),
    path('tourism/reviews/<int:review_id>/reject/', admin_views.tourism_review_reject, name='tourism_review_reject'),
    path('tourism/reviews/<int:review_id>/delete/', admin_views.tourism_review_delete, name='tourism_review_delete'),
    
    # Tourism Gallery
    path('tourism/gallery/', admin_views.tourism_gallery_list, name='tourism_gallery_list'),
    path('tourism/gallery/create/', admin_views.tourism_gallery_create, name='tourism_gallery_create'),
    path('tourism/gallery/<int:gallery_id>/edit/', admin_views.tourism_gallery_edit, name='tourism_gallery_edit'),
    path('tourism/gallery/<int:gallery_id>/delete/', admin_views.tourism_gallery_delete, name='tourism_gallery_delete'),
    
    # Tourism FAQ
    path('tourism/faq/', admin_views.tourism_faq_list, name='tourism_faq_list'),
    path('tourism/faq/create/', admin_views.tourism_faq_create, name='tourism_faq_create'),
    path('tourism/faq/<int:faq_id>/', admin_views.tourism_faq_detail, name='tourism_faq_detail'),
    path('tourism/faq/<int:faq_id>/edit/', admin_views.tourism_faq_edit, name='tourism_faq_edit'),
    path('tourism/faq/<int:faq_id>/delete/', admin_views.tourism_faq_delete, name='tourism_faq_delete'),
    
    # Tourism Reports
    path('tourism/reports/', admin_views.tourism_reports, name='tourism_reports'),
    path('tourism/export/', admin_views.tourism_export_data, name='tourism_export_data'),
    path('tourism/bulk-operations/', admin_views.tourism_bulk_operations, name='tourism_bulk_operations'),
    
    # Tourism Settings
    path('tourism/settings/', admin_views.tourism_settings, name='tourism_settings'),
    
    # Tourism API
    path('tourism/api/locations/', admin_views.tourism_api_locations, name='tourism_api_locations'),
    path('tourism/api/categories/', admin_views.tourism_api_categories, name='tourism_api_categories'),
    path('tourism/api/statistics/', admin_views.tourism_api_statistics, name='tourism_api_statistics'),
    path('tourism/api/search-locations/', admin_views.tourism_search_locations, name='tourism_search_locations'),
    path('tourism/api/location-stats/<int:location_id>/', admin_views.tourism_location_stats, name='tourism_location_stats'),
    # Village Profile URLs - include village_profile URLs
    path('village-profile/', include('village_profile.urls')),
    path('news/', admin_views.news_dashboard, name='news_dashboard'),
    path('news/list/', admin_views.news_list, name='news_list'),
    path('news/create/', admin_views.news_create, name='news_create'),
    path('news/categories/list/', admin_views.news_categories_list, name='news_categories_list'),
    path('news/categories/create/', admin_views.news_category_create, name='news_category_create'),
    path('news/announcements/', admin_views.announcements_list, name='news_announcements_list'),
    path('news/announcements/create/', admin_views.announcement_create, name='news_announcement_create'),
    path('news/announcements/<int:pk>/', admin_views.announcement_detail, name='news_announcement_detail'),
    path('news/announcements/<int:pk>/edit/', admin_views.announcement_edit, name='news_announcement_edit'),
    path('news/announcements/<int:pk>/delete/', admin_views.announcement_delete, name='news_announcement_delete'),
    path('news/announcements/<int:pk>/toggle-status/', admin_views.announcement_toggle_status, name='news_announcement_toggle_status'),
    path('news/announcements/<int:pk>/toggle-pin/', admin_views.announcement_toggle_pin, name='news_announcement_toggle_pin'),
    path('news/comments/', admin_views.news_comments, name='news_comments'),
    path('news/<int:pk>/', admin_views.news_detail, name='news_detail'),
    path('news/<int:pk>/edit/', admin_views.news_edit, name='news_edit'),
    path('news/<int:pk>/delete/', admin_views.news_delete, name='news_delete'),
    path('news/upload-image/', admin_views.news_upload_image, name='news_upload_image'),
    path('news/categories/<int:pk>/edit/', admin_views.news_category_edit, name='news_category_edit'),
    path('news/categories/<int:pk>/update/', admin_views.news_category_update, name='news_category_update'),
    path('news/categories/<int:pk>/delete/', admin_views.news_category_delete, name='news_category_delete'),
    path('news/tags/', admin_views.news_tags_list, name='news_tags_list'),
    path('news/tags/create/', admin_views.news_tag_create, name='news_tag_create'),
    path('news/tags/<int:pk>/edit/', admin_views.news_tag_edit, name='news_tag_edit'),
    path('news/tags/<int:pk>/update/', admin_views.news_tag_update, name='news_tag_update'),
    path('news/tags/<int:pk>/delete/', admin_views.news_tag_delete, name='news_tag_delete'),
    path('news/comments/<int:pk>/approve/', admin_views.news_comment_approve, name='news_comment_approve'),
    path('news/comments/<int:pk>/reject/', admin_views.news_comment_reject, name='news_comment_reject'),
    path('news/comments/<int:pk>/delete/', admin_views.news_comment_delete, name='news_comment_delete'),
    path('news/comments/<int:pk>/spam/', admin_views.news_comment_spam, name='news_comment_spam'),
    path('news/<int:pk>/duplicate/', admin_views.news_duplicate, name='news_duplicate'),
    path('news/<int:pk>/preview/', admin_views.news_preview, name='news_preview'),
    path('news/<int:pk>/analytics/', admin_views.news_analytics_detail, name='news_analytics_detail'),
    path('news/generate-slug/', admin_views.news_generate_slug, name='news_generate_slug'),
    path('news/bulk-update/', admin_views.news_bulk_update, name='news_bulk_update'),
    path('news/export/', admin_views.news_export, name='news_export'),
    path('news/reports/', admin_views.news_reports, name='news_reports'),
    # Posyandu Module - include posyandu URLs
    path('posyandu/', include(('posyandu.urls', 'posyandu'))),
    path('reports/', admin_views.reports_dashboard, name='reports_dashboard'),
    path('settings/', admin_views.settings_dashboard, name='settings_dashboard'),
    path('export/', admin_views.export_data, name='export_data'),
    path('test-roles/', admin_views.test_roles, name='test_roles'),
    path('profile/', admin_views.profile, name='profile'),
    path('profile/update/', admin_views.profile_update, name='profile_update'),
    path('profile/change-password/', admin_views.change_password, name='change_password'),
    path('api/dashboard-stats/', admin_views.dashboard_stats_api, name='dashboard_stats_api'),
    path('api/references/dashboard-data/', admin_views.api_references_dashboard_data, name='api_references_dashboard_data'),
    path('api/references/penduduk/', admin_views.api_references_penduduk_list, name='api_references_penduduk_list'),
    
    # Penduduk URLs
    path('references/penduduk/', admin_views.references_penduduk_list, name='references_penduduk_list'),
    path('references/penduduk/add/', admin_views.references_penduduk_add, name='references_penduduk_add'),
    path('references/penduduk/edit/<int:penduduk_id>/', admin_views.references_penduduk_edit, name='references_penduduk_edit'),
    path('references/penduduk/detail/<int:penduduk_id>/', admin_views.references_penduduk_detail, name='references_penduduk_detail'),
    path('references/penduduk/delete/<int:penduduk_id>/', admin_views.references_penduduk_delete, name='references_penduduk_delete'),
    path('references/penduduk/upload-photo/<int:penduduk_id>/', admin_views.references_penduduk_upload_photo, name='references_penduduk_upload_photo'),
    path('references/penduduk/bulk-delete/', admin_views.references_penduduk_bulk_delete, name='references_penduduk_bulk_delete'),
    path('references/penduduk/bulk-activate/', admin_views.references_penduduk_bulk_activate, name='references_penduduk_bulk_activate'),
    path('references/penduduk/bulk-deactivate/', admin_views.references_penduduk_bulk_deactivate, name='references_penduduk_bulk_deactivate'),
    path('references/penduduk/export-excel/', admin_views.references_penduduk_export_excel, name='references_penduduk_export_excel'),
    path('references/penduduk/export-csv/', admin_views.references_penduduk_export_csv, name='references_penduduk_export_csv'),
    path('references/penduduk/export-json/', admin_views.references_penduduk_export_json, name='references_penduduk_export_json'),
    path('references/penduduk/export-pdf/', admin_views.references_penduduk_export_pdf, name='references_penduduk_export_pdf'),
    
    # Organization Module
    path('organization/', include(('organization.admin_urls', 'organization'))),
    
    # Layanan Module
    path('layanan/', include(('layanan.admin_urls', 'layanan'))),
    
    # Letters Module
    path('letters/', include(('letters.admin_urls', 'letters'))),
    
    # Hero Images Module
    path('hero-images/', include('admin_panel.hero_image_urls')),
    
    # Export/Import for References
    path('references/export/penduduk/', PendudukExportView.as_view(), name='export_penduduk'),
    path('references/import/penduduk/', export_import.quick_import, {'model_name': 'penduduk'}, name='import_penduduk'),
    path('references/get-template/<str:model_name>/', template_generators.get_import_template, name='references_get_template'),
    
    # Additional short URL patterns for CRUD operations (must be at the end to avoid conflicts)
    path('references/dusun/<int:dusun_id>/', admin_views.references_dusun_detail, name='references_dusun_detail_short'),
    path('references/lorong/<int:lorong_id>/', admin_views.references_lorong_detail, name='references_lorong_detail_short'),
    path('references/rw/<int:rw_id>/', admin_views.references_rw_detail, name='references_rw_detail_short'),
    path('references/rt/<int:rt_id>/', admin_views.references_rt_detail, name='references_rt_detail_short'),
    path('references/disabilitas/<int:disabilitas_id>/', admin_views.references_disabilitas_detail, name='references_disabilitas_detail_short'),
    path('references/pelajar/<int:pelajar_id>/', admin_views.references_pelajar_detail, name='references_pelajar_detail_short'),
    
    # ============================================================================
    # UTILITIES URLs (Admin Panel Utility Models)
    # ============================================================================
    path('utilities/', include('admin_panel.utility_urls')),
    
    # References Dashboard (MUST be at the very end to avoid conflicts with specific URLs)
    path('references/', admin_views.references_dashboard, name='references_dashboard'),
]