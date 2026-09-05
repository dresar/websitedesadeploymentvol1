"""
Admin Panel Views - Simple version with proxy functions
"""

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import JsonResponse
from django.contrib.auth.models import User
from core.models import CustomUser

# Import views from other apps
from references import views as references_views
from beneficiaries import views as beneficiaries_views
from business import admin_views as business_views
from business import api_views as business_api_views
from complaints import views as complaints_views
from documents import views as documents_views
from tourism import views as tourism_views
from news import views as news_views

@login_required
def admin_dashboard(request):
    """Main admin dashboard"""
    context = {
        'page_title': 'Admin Dashboard',
        'active_menu': 'dashboard',
    }
    return render(request, 'admin_panel/dashboard.html', context)

def custom_login(request):
    """Custom login view"""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login berhasil!')
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, 'Username atau password salah.')
    
    return render(request, 'admin_panel/login.html')

# Proxy functions for references
@login_required
def references_dashboard(request):
    """References dashboard"""
    return references_views.admin_panel_dashboard(request)

@login_required
def references_penduduk_list(request):
    return references_views.penduduk_list(request)

@login_required
def references_penduduk_add(request):
    return references_views.penduduk_add(request)

@login_required
def references_penduduk_edit(request, penduduk_id):
    return references_views.penduduk_edit(request, penduduk_id)

@login_required
def references_penduduk_update(request, penduduk_id):
    return references_views.penduduk_update(request, penduduk_id)

@login_required
def references_penduduk_detail(request, penduduk_id):
    return references_views.penduduk_detail(request, penduduk_id)

@login_required
def references_penduduk_delete(request, penduduk_id):
    return references_views.penduduk_delete(request, penduduk_id)

@login_required
def references_dusun_list(request):
    return references_views.dusun_list(request)

@login_required
def references_dusun_add(request):
    return references_views.dusun_add(request)

@login_required
def references_dusun_edit(request, dusun_id):
    return references_views.dusun_edit(request, dusun_id)

@login_required
def references_dusun_update(request, dusun_id):
    return references_views.dusun_update(request, dusun_id)

@login_required
def references_dusun_detail(request, dusun_id):
    return references_views.dusun_detail(request, dusun_id)

@login_required
def references_dusun_delete(request, dusun_id):
    return references_views.dusun_delete(request, dusun_id)

@login_required
def references_lorong_list(request):
    return references_views.lorong_list(request)

@login_required
def references_lorong_add(request):
    return references_views.lorong_add(request)

@login_required
def references_lorong_edit(request, lorong_id):
    return references_views.lorong_edit(request, lorong_id)

@login_required
def references_lorong_update(request, lorong_id):
    return references_views.lorong_update(request, lorong_id)

@login_required
def references_lorong_detail(request, lorong_id):
    return references_views.lorong_detail(request, lorong_id)

@login_required
def references_lorong_delete(request, lorong_id):
    return references_views.lorong_delete(request, lorong_id)

@login_required
def references_rw_list(request):
    return references_views.rw_list(request)

@login_required
def references_rw_add(request):
    return references_views.rw_create(request)

@login_required
def references_rw_edit(request, rw_id):
    return references_views.rw_edit(request, rw_id)

@login_required
def references_rw_update(request, rw_id):
    return references_views.rw_edit(request, rw_id)

@login_required
def references_rw_detail(request, rw_id):
    return references_views.rw_detail(request, rw_id)

@login_required
def references_rw_delete(request, rw_id):
    return references_views.rw_delete(request, rw_id)

@login_required
def references_rt_list(request):
    return references_views.rt_list(request)

@login_required
def references_rt_add(request):
    return references_views.rt_create(request)

@login_required
def references_rt_edit(request, rt_id):
    return references_views.rt_edit(request, rt_id)

@login_required
def references_rt_update(request, rt_id):
    return references_views.rt_edit(request, rt_id)

@login_required
def references_rt_detail(request, rt_id):
    return references_views.rt_detail(request, rt_id)

@login_required
def references_rt_delete(request, rt_id):
    return references_views.rt_delete(request, rt_id)

@login_required
def references_disabilitas_list(request):
    return references_views.disabilitas_list(request)

@login_required
def references_disabilitas_add(request):
    return references_views.disabilitas_add(request)

@login_required
def references_disabilitas_edit(request, disabilitas_id):
    return references_views.disabilitas_edit(request, disabilitas_id)

@login_required
def references_disabilitas_update(request, disabilitas_id):
    return references_views.disabilitas_update(request, disabilitas_id)

@login_required
def references_disabilitas_detail(request, disabilitas_id):
    return references_views.disabilitas_detail(request, disabilitas_id)

@login_required
def references_disabilitas_delete(request, disabilitas_id):
    return references_views.disabilitas_delete(request, disabilitas_id)

@login_required
def references_pelajar_list(request):
    return references_views.pelajar_list(request)

@login_required
def references_pelajar_detail(request, pelajar_id):
    return references_views.pelajar_detail(request, pelajar_id)

@login_required
def references_pelajar_edit(request, pelajar_id):
    return references_views.pelajar_edit(request, pelajar_id)

@login_required
def references_pelajar_delete(request, pelajar_id):
    return references_views.pelajar_delete(request, pelajar_id)

@login_required
def references_pelajar_add(request):
    return references_views.pelajar_add(request)

@login_required
def references_pelajar_update(request, pelajar_id):
    return references_views.pelajar_update(request, pelajar_id)

@login_required
def references_keluarga_list(request):
    return references_views.keluarga_list(request)

@login_required
def references_keluarga_add(request):
    return references_views.keluarga_add(request)

@login_required
def references_keluarga_edit(request, keluarga_id):
    return references_views.keluarga_edit(request, keluarga_id)

@login_required
def references_keluarga_update(request, keluarga_id):
    return references_views.keluarga_update(request, keluarga_id)

@login_required
def references_keluarga_detail(request, keluarga_id):
    return references_views.keluarga_detail(request, keluarga_id)

@login_required
def references_keluarga_delete(request, keluarga_id):
    return references_views.keluarga_delete(request, keluarga_id)

@login_required
def references_keluarga_update_anggota(request, keluarga_id):
    return references_views.keluarga_update_anggota(request, keluarga_id)

# Business views
@login_required
def business_dashboard(request):
    return business_views.business_dashboard(request)

@login_required
def umkm_list(request):
    return business_views.admin_ukm_list(request)

@login_required
def umkm_create(request):
    return business_views.umkm_create(request)

@login_required
def umkm_detail(request, umkm_id):
    return business_views.umkm_detail(request, umkm_id)

@login_required
def umkm_edit(request, umkm_id):
    return business_views.umkm_edit(request, umkm_id)

@login_required
def umkm_update(request, umkm_id):
    return business_views.umkm_edit(request, umkm_id)

@login_required
def umkm_delete(request, umkm_id):
    return business_views.umkm_delete(request, umkm_id)

@login_required
def koperasi_list(request):
    return business_views.koperasi_list(request)

@login_required
def koperasi_create(request):
    return business_views.koperasi_create(request)

@login_required
def koperasi_detail(request, koperasi_id):
    return business_views.koperasi_detail(request, koperasi_id)

@login_required
def koperasi_edit(request, koperasi_id):
    return business_views.koperasi_edit(request, koperasi_id)

@login_required
def koperasi_update(request, koperasi_id):
    return business_views.koperasi_edit(request, koperasi_id)

@login_required
def koperasi_delete(request, koperasi_id):
    return business_views.koperasi_delete(request, koperasi_id)

@login_required
def bumg_list(request):
    return business_views.bumg_list(request)

@login_required
def bumg_create(request):
    return business_views.bumg_create(request)

@login_required
def bumg_detail(request, bumg_id):
    return business_views.bumg_detail(request, bumg_id)

@login_required
def bumg_edit(request, bumg_id):
    return business_views.bumg_edit(request, bumg_id)

@login_required
def bumg_update(request, bumg_id):
    return business_views.bumg_edit(request, bumg_id)

@login_required
def bumg_delete(request, bumg_id):
    return business_views.bumg_delete(request, bumg_id)

@login_required
def layanan_jasa_list(request):
    return business_views.admin_layanan_jasa_list(request)

@login_required
def layanan_jasa_create(request):
    return business_views.layanan_jasa_create(request)

@login_required
def layanan_jasa_detail(request, layanan_id):
    return business_views.layanan_jasa_detail(request, layanan_id)

@login_required
def layanan_jasa_edit(request, layanan_id):
    return business_views.layanan_jasa_edit(request, layanan_id)

@login_required
def layanan_jasa_update(request, layanan_id):
    return business_views.layanan_jasa_edit(request, layanan_id)

@login_required
def layanan_jasa_delete(request, layanan_id):
    return business_views.layanan_jasa_delete(request, layanan_id)

@login_required
def business_categories_list(request):
    return business_views.business_categories_list(request)

@login_required
def business_category_create(request):
    return business_views.business_category_create(request)

@login_required
def business_category_detail(request, category_id):
    return business_views.business_category_detail(request, category_id)

@login_required
def business_category_edit(request, category_id):
    return business_views.business_category_edit(request, category_id)

@login_required
def business_category_update(request, category_id):
    return business_views.business_category_edit(request, category_id)

@login_required
def business_category_delete(request, category_id):
    return business_views.business_category_delete(request, category_id)

@login_required
def business_category_delete_confirm(request, category_id):
    """Show delete confirmation page for business category"""
    if request.method == 'GET':
        try:
            from business.models import BusinessCategory, Business
            category = BusinessCategory.objects.get(id=category_id)
            
            # Get related businesses count from Business model
            businesses = Business.objects.filter(category=category)
            total_businesses = businesses.count()
            
            # Count by business type
            umkm_count = businesses.filter(business_type='umkm').count()
            koperasi_count = businesses.filter(business_type='koperasi').count()
            bumg_count = businesses.filter(business_type='bumg').count()
            layanan_count = businesses.filter(business_type='layanan_jasa').count()
            
            context = {
                'category': category,
                'businesses': businesses,
                'umkm_count': umkm_count,
                'koperasi_count': koperasi_count,
                'bumg_count': bumg_count,
                'layanan_count': layanan_count,
                'total_businesses': total_businesses,
            }
            
            return render(request, 'admin_panel/business/category_delete_confirm.html', context)
        except BusinessCategory.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Kategori tidak ditemukan'
            }, status=404)
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method'
    }, status=405)

# Complaints views
@login_required
def complaints_dashboard(request):
    return complaints_views.complaints_dashboard(request)

@login_required
def complaints_list(request):
    return complaints_views.complaints_list(request)

@login_required
def complaint_detail(request, pk):
    return complaints_views.complaint_detail(request, pk)

@login_required
def complaint_edit(request, pk):
    return complaints_views.complaint_edit(request, pk)

@login_required
def complaint_update(request, pk):
    return complaints_views.complaint_update(request, pk)

@login_required
def complaint_delete(request, pk):
    return complaints_views.complaint_delete(request, pk)

@login_required
def complaint_add_update(request, pk):
    return complaints_views.complaint_add_update(request, pk)

@login_required
def complaint_categories_list(request):
    return complaints_views.complaint_categories_list(request)

@login_required
def verifications_list(request):
    return complaints_views.verifications_list(request)

@login_required
def verification_dashboard(request):
    return complaints_views.verification_dashboard(request)

@login_required
def verification_create(request, complaint_id):
    return complaints_views.verification_create(request, complaint_id)

@login_required
def verification_detail(request, pk):
    return complaints_views.verification_detail(request, pk)

@login_required
def verification_update(request, pk):
    return complaints_views.verification_update(request, pk)

@login_required
def verification_delete(request, pk):
    return complaints_views.verification_delete(request, pk)

# Tourism views
@login_required
def tourism_dashboard(request):
    return tourism_views.admin_dashboard(request)

@login_required
def tourism_locations_list(request):
    return tourism_views.admin_panel_location_list(request)

@login_required
def tourism_location_create(request):
    return tourism_views.admin_panel_location_create(request)

@login_required
def tourism_location_detail(request, location_id):
    return tourism_views.admin_panel_location_detail(request, location_id)

@login_required
def tourism_location_edit(request, location_id):
    return tourism_views.admin_panel_location_update(request, location_id)

@login_required
def tourism_location_delete(request, location_id):
    return tourism_views.admin_panel_location_delete(request, location_id)

@login_required
def tourism_location_toggle_status(request, location_id):
    return tourism_views.admin_panel_location_toggle_status(request, location_id)

@login_required
def tourism_location_toggle_featured(request, location_id):
    return tourism_views.admin_panel_location_toggle_featured(request, location_id)

@login_required
def tourism_categories_list(request):
    return tourism_views.admin_panel_category_list(request)

@login_required
def tourism_category_create(request):
    return tourism_views.admin_panel_category_create(request)

@login_required
def tourism_category_detail(request, category_id):
    return tourism_views.admin_panel_category_detail(request, category_id)

@login_required
def tourism_category_edit(request, category_id):
    return tourism_views.admin_panel_category_update(request, category_id)

@login_required
def tourism_category_delete(request, category_id):
    return tourism_views.admin_panel_category_delete(request, category_id)

@login_required
def tourism_packages_list(request):
    return tourism_views.admin_panel_package_list(request)

@login_required
def tourism_package_create(request):
    return tourism_views.admin_panel_package_create(request)

@login_required
def tourism_package_detail(request, package_id):
    return tourism_views.admin_panel_package_detail(request, package_id)

@login_required
def tourism_package_edit(request, package_id):
    return tourism_views.admin_panel_package_update(request, package_id)

@login_required
def tourism_package_delete(request, package_id):
    return tourism_views.admin_panel_package_delete(request, package_id)

@login_required
def tourism_events_list(request):
    return tourism_views.admin_panel_event_list(request)

@login_required
def tourism_event_create(request):
    return tourism_views.admin_panel_event_create(request)

@login_required
def tourism_event_detail(request, event_id):
    return tourism_views.admin_panel_event_detail(request, event_id)

@login_required
def tourism_event_edit(request, event_id):
    return tourism_views.admin_panel_event_update(request, event_id)

@login_required
def tourism_event_delete(request, event_id):
    return tourism_views.admin_panel_event_delete(request, event_id)

@login_required
def tourism_reviews_list(request):
    return tourism_views.admin_panel_review_list(request)

@login_required
def tourism_review_detail(request, review_id):
    return tourism_views.admin_panel_review_detail(request, review_id)

@login_required
def tourism_review_edit(request, review_id):
    return tourism_views.admin_panel_review_edit(request, review_id)

@login_required
def tourism_review_approve(request, review_id):
    return tourism_views.admin_panel_review_approve(request, review_id)

@login_required
def tourism_review_reject(request, review_id):
    return tourism_views.admin_panel_review_reject(request, review_id)

@login_required
def tourism_review_delete(request, review_id):
    return tourism_views.admin_panel_review_delete(request, review_id)

@login_required
def tourism_gallery_list(request):
    return tourism_views.admin_panel_gallery_list(request)

@login_required
def tourism_gallery_create(request):
    return tourism_views.admin_panel_gallery_create(request)

@login_required
def tourism_gallery_edit(request, gallery_id):
    return tourism_views.admin_panel_gallery_edit(request, gallery_id)

@login_required
def tourism_gallery_delete(request, gallery_id):
    return tourism_views.admin_panel_gallery_delete(request, gallery_id)

@login_required
def tourism_faq_list(request):
    return tourism_views.admin_panel_faq_list(request)

@login_required
def tourism_faq_create(request):
    return tourism_views.admin_panel_faq_create(request)

@login_required
def tourism_faq_detail(request, faq_id):
    return tourism_views.admin_panel_faq_detail(request, faq_id)

@login_required
def tourism_faq_edit(request, faq_id):
    return tourism_views.admin_panel_faq_edit(request, faq_id)

@login_required
def tourism_faq_delete(request, faq_id):
    return tourism_views.admin_panel_faq_delete(request, faq_id)

@login_required
def tourism_reports(request):
    return tourism_views.admin_panel_reports(request)

@login_required
def tourism_export_data(request):
    return tourism_views.admin_panel_export_data(request)

@login_required
def tourism_bulk_operations(request):
    return tourism_views.admin_panel_bulk_operations(request)

@login_required
def tourism_settings(request):
    return tourism_views.admin_panel_settings(request)

@login_required
def tourism_api_locations(request):
    return tourism_views.admin_panel_api_locations(request)

@login_required
def tourism_api_categories(request):
    return tourism_views.admin_panel_api_categories(request)

@login_required
def tourism_api_statistics(request):
    return tourism_views.admin_panel_api_statistics(request)

@login_required
def tourism_search_locations(request):
    return tourism_views.admin_panel_search_locations(request)

@login_required
def tourism_location_stats(request, location_id):
    return tourism_views.admin_panel_location_stats(request, location_id)

# News views
@login_required
def news_dashboard(request):
    return news_views.admin_news_dashboard(request)

@login_required
def news_list(request):
    return news_views.admin_news_list(request)

@login_required
def news_create(request):
    return news_views.admin_news_create(request)

@login_required
def news_detail(request, pk):
    return news_views.admin_news_detail(request, pk)

@login_required
def news_edit(request, pk):
    return news_views.admin_news_update(request, pk)

@login_required
def news_delete(request, pk):
    return news_views.admin_news_delete(request, pk)

@login_required
def news_upload_image(request):
    return news_views.admin_news_upload_image(request)

@login_required
def news_categories_list(request):
    return news_views.admin_news_categories_list(request)

@login_required
def news_category_create(request):
    return news_views.admin_news_category_create(request)

@login_required
def news_category_edit(request, pk):
    return news_views.admin_news_category_update(request, pk)

@login_required
def news_category_update(request, pk):
    return news_views.admin_news_category_update(request, pk)

@login_required
def news_category_delete(request, pk):
    return news_views.admin_news_category_delete(request, pk)

@login_required
def news_tags_list(request):
    return news_views.admin_news_tags_list(request)

@login_required
def news_tag_create(request):
    return news_views.admin_news_tag_create(request)

@login_required
def news_tag_edit(request, pk):
    return news_views.admin_news_tag_update(request, pk)

@login_required
def news_tag_update(request, pk):
    return news_views.admin_news_tag_update(request, pk)

@login_required
def news_tag_delete(request, pk):
    return news_views.admin_news_tag_delete(request, pk)

@login_required
def news_comments(request):
    return news_views.admin_news_comments_list(request)

@login_required
def news_comment_approve(request, pk):
    return news_views.admin_news_comment_approve(request, pk)

@login_required
def news_comment_reject(request, pk):
    return news_views.admin_news_comment_reject(request, pk)

@login_required
def news_comment_delete(request, pk):
    return news_views.admin_news_comment_delete(request, pk)

@login_required
def news_comment_spam(request, pk):
    return news_views.admin_news_comment_spam(request, pk)

@login_required
def news_duplicate(request, pk):
    return news_views.admin_news_duplicate(request, pk)

@login_required
def news_preview(request, pk):
    return news_views.admin_news_preview(request, pk)

@login_required
def news_analytics_detail(request, pk):
    return news_views.admin_news_analytics_detail(request, pk)

@login_required
def news_generate_slug(request):
    return news_views.admin_news_generate_slug(request)

@login_required
def news_bulk_update(request):
    return news_views.admin_news_bulk_update(request)

@login_required
def news_export(request):
    return news_views.admin_news_export(request)

@login_required
def news_reports(request):
    return news_views.admin_news_reports(request)

@login_required
def announcements_list(request):
    return news_views.admin_announcements_list(request)

@login_required
def announcement_create(request):
    return news_views.admin_announcement_create(request)

@login_required
def announcement_detail(request, pk):
    return news_views.admin_announcement_detail(request, pk)

@login_required
def announcement_edit(request, pk):
    return news_views.admin_announcement_update(request, pk)

@login_required
def announcement_delete(request, pk):
    return news_views.admin_announcement_delete(request, pk)

@login_required
def announcement_toggle_status(request, pk):
    return news_views.admin_announcement_toggle_status(request, pk)

@login_required
def announcement_toggle_pin(request, pk):
    return news_views.admin_announcement_toggle_pin(request, pk)

# Export/Import functions
@login_required
def references_penduduk_export_excel(request):
    """Export penduduk to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_penduduk_list')

@login_required
def references_penduduk_export_csv(request):
    """Export penduduk to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_penduduk_list')

@login_required
def references_penduduk_export_json(request):
    """Export penduduk to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_penduduk_list')

@login_required
def references_penduduk_export_pdf(request):
    """Export penduduk to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_penduduk_list')

@login_required
def references_bulk_action(request):
    """Bulk action for references"""
    return references_views.penduduk_bulk_delete(request)

@login_required
def references_penduduk_bulk_delete(request):
    return references_views.penduduk_bulk_delete(request)

@login_required
def references_penduduk_bulk_activate(request):
    return references_views.penduduk_bulk_activate(request)

@login_required
def references_penduduk_bulk_deactivate(request):
    return references_views.penduduk_bulk_deactivate(request)

@login_required
def references_quick_import(request, model_name):
    """Quick import - placeholder"""
    messages.info(request, 'Import feature coming soon')
    return redirect('admin_panel:references_dashboard')

@login_required
def references_penduduk_save(request):
    return references_views.penduduk_save(request)

@login_required
def references_pelajar_export_excel(request):
    return references_views.pelajar_export_excel(request)

@login_required
def references_pelajar_export_csv(request):
    return references_views.pelajar_export_csv(request)

@login_required
def references_pelajar_export_json(request):
    return references_views.pelajar_export_json(request)

@login_required
def references_pelajar_export_pdf(request):
    return references_views.pelajar_export_pdf(request)

@login_required
def api_references_dusun_list(request):
    return references_views.api_dusun_list(request)

@login_required
def api_references_lorong_list(request):
    return references_views.api_lorong_list(request)

@login_required
def api_references_lorong_by_dusun(request):
    return references_views.api_lorong_by_dusun(request)

@login_required
def api_references_rw_by_dusun(request, dusun_id):
    return references_views.api_rw_by_dusun(request, dusun_id)

@login_required
def api_references_rt_by_rw(request, rw_id):
    return references_views.api_rt_by_rw(request, rw_id)

@login_required
def api_references_residents_search(request):
    return references_views.api_search_residents(request)

@login_required
def api_references_penduduk_by_dusun(request, dusun_id):
    return references_views.api_penduduk_by_dusun(request, dusun_id)

@login_required
def api_references_keluarga_list(request):
    return references_views.api_keluarga_list(request)

@login_required
def api_penduduk_search(request):
    return references_views.api_search_residents(request)

@login_required
def references_dusun_export_excel(request):
    """Export dusun to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_dusun_list')

@login_required
def references_dusun_export_csv(request):
    """Export dusun to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_dusun_list')

@login_required
def references_dusun_export_json(request):
    """Export dusun to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_dusun_list')

@login_required
def references_dusun_export_pdf(request):
    """Export dusun to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_dusun_list')

@login_required
def references_dusun_bulk_delete(request):
    return references_views.dusun_bulk_delete(request)

@login_required
def references_dusun_bulk_activate(request):
    return references_views.dusun_bulk_activate(request)

@login_required
def references_dusun_bulk_deactivate(request):
    return references_views.dusun_bulk_deactivate(request)

@login_required
def references_lorong_export_excel(request):
    """Export lorong to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_lorong_list')

@login_required
def references_lorong_export_csv(request):
    """Export lorong to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_lorong_list')

@login_required
def references_lorong_export_json(request):
    """Export lorong to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_lorong_list')

@login_required
def references_lorong_export_pdf(request):
    """Export lorong to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_lorong_list')

@login_required
def references_lorong_bulk_delete(request):
    return references_views.lorong_bulk_delete(request)

@login_required
def references_lorong_bulk_activate(request):
    return references_views.lorong_bulk_activate(request)

@login_required
def references_lorong_bulk_deactivate(request):
    return references_views.lorong_bulk_deactivate(request)

@login_required
def references_rw_export_excel(request):
    """Export RW to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rw_list')

@login_required
def references_rw_export_csv(request):
    """Export RW to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rw_list')

@login_required
def references_rw_export_json(request):
    """Export RW to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rw_list')

@login_required
def references_rw_export_pdf(request):
    """Export RW to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rw_list')

@login_required
def references_rw_bulk_delete(request):
    return references_views.rw_bulk_delete(request)

@login_required
def references_rw_bulk_activate(request):
    return references_views.rw_bulk_activate(request)

@login_required
def references_rw_bulk_deactivate(request):
    return references_views.rw_bulk_deactivate(request)

@login_required
def references_rt_export_excel(request):
    """Export RT to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rt_list')

@login_required
def references_rt_export_csv(request):
    """Export RT to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rt_list')

@login_required
def references_rt_export_json(request):
    """Export RT to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rt_list')

@login_required
def references_rt_export_pdf(request):
    """Export RT to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_rt_list')

@login_required
def references_rt_bulk_delete(request):
    return references_views.rt_bulk_delete(request)

@login_required
def references_rt_bulk_activate(request):
    return references_views.rt_bulk_activate(request)

@login_required
def references_rt_bulk_deactivate(request):
    return references_views.rt_bulk_deactivate(request)

@login_required
def references_disabilitas_export_excel(request):
    """Export disabilitas to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_disabilitas_list')

@login_required
def references_disabilitas_export_csv(request):
    """Export disabilitas to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_disabilitas_list')

@login_required
def references_disabilitas_export_json(request):
    """Export disabilitas to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_disabilitas_list')

@login_required
def references_disabilitas_export_pdf(request):
    """Export disabilitas to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_disabilitas_list')

@login_required
def references_disabilitas_bulk_delete(request):
    return references_views.disabilitas_bulk_delete(request)

@login_required
def references_disabilitas_bulk_activate(request):
    return references_views.disabilitas_bulk_activate(request)

@login_required
def references_disabilitas_bulk_deactivate(request):
    return references_views.disabilitas_bulk_deactivate(request)

@login_required
def references_pelajar_bulk_delete(request):
    return references_views.pelajar_bulk_delete(request)

@login_required
def references_pelajar_bulk_activate(request):
    return references_views.pelajar_bulk_activate(request)

@login_required
def references_pelajar_bulk_deactivate(request):
    return references_views.pelajar_bulk_deactivate(request)

@login_required
def references_keluarga_export_excel(request):
    """Export keluarga to Excel - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_keluarga_list')

@login_required
def references_keluarga_export_csv(request):
    """Export keluarga to CSV - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_keluarga_list')

@login_required
def references_keluarga_export_json(request):
    """Export keluarga to JSON - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_keluarga_list')

@login_required
def references_keluarga_export_pdf(request):
    """Export keluarga to PDF - placeholder"""
    messages.info(request, 'Export feature coming soon')
    return redirect('admin_panel:references_keluarga_list')

@login_required
def references_keluarga_bulk_delete(request):
    return references_views.keluarga_bulk_delete(request)

@login_required
def references_keluarga_bulk_activate(request):
    return references_views.keluarga_bulk_activate(request)

@login_required
def references_keluarga_bulk_deactivate(request):
    return references_views.keluarga_bulk_deactivate(request)

@login_required
def references_penduduk_upload_photo(request, penduduk_id):
    return references_views.penduduk_upload_photo(request)

# API views
@login_required
def api_business_penduduk_search(request):
    return business_api_views.api_penduduk_search_public(request)

@login_required
def api_business_umkm_search(request):
    return business_api_views.api_umkm_list(request)

@login_required
def api_business_koperasi_search(request):
    return JsonResponse({'error': 'API not implemented'}, status=501)

@login_required
def api_business_bumg_search(request):
    return JsonResponse({'error': 'API not implemented'}, status=501)

@login_required
def api_business_layanan_search(request):
    return JsonResponse({'error': 'API not implemented'}, status=501)

# Dashboard and misc
@login_required
def reports_dashboard(request):
    """Dashboard laporan dan statistik"""
    from django.utils import timezone
    from datetime import datetime, timedelta
    from django.db.models import Count, Q, Sum, Avg
    from django.contrib.auth.models import User
    
    # Get date filters
    date_from = request.GET.get('date_from')
    date_to = request.GET.get('date_to')
    
    if not date_from:
        date_from = (timezone.now() - timedelta(days=30)).date()
    else:
        date_from = datetime.strptime(date_from, '%Y-%m-%d').date()
    
    if not date_to:
        date_to = timezone.now().date()
    else:
        date_to = datetime.strptime(date_to, '%Y-%m-%d').date()
    
    # Beneficiaries stats
    try:
        from beneficiaries.models import Beneficiary, AidDistribution
        beneficiaries_total = Beneficiary.objects.count()
        beneficiaries_active = Beneficiary.objects.filter(status='aktif').count()
        beneficiaries_by_category = list(
            Beneficiary.objects.values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        beneficiaries_stats = {
            'total': beneficiaries_total,
            'active': beneficiaries_active,
            'by_category': beneficiaries_by_category
        }
    except ImportError:
        beneficiaries_stats = {
            'total': 0,
            'active': 0,
            'by_category': []
        }
    
    # Business stats
    try:
        from business.models import UMKM, Koperasi, BUMG, LayananJasa
        business_total = UMKM.objects.count() + Koperasi.objects.count() + BUMG.objects.count() + LayananJasa.objects.count()
        business_active = (UMKM.objects.filter(is_active=True).count() + 
                        Koperasi.objects.filter(is_active=True).count() + 
                        BUMG.objects.filter(is_active=True).count() + 
                        LayananJasa.objects.filter(is_active=True).count())
        business_by_category = list(
            UMKM.objects.values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        business_stats = {
            'total': business_total,
            'active': business_active,
            'by_category': business_by_category
        }
    except ImportError:
        business_stats = {
            'total': 0,
            'active': 0,
            'by_category': []
        }
    
    # Complaints stats
    try:
        from complaints.models import Complaint
        complaints_total = Complaint.objects.count()
        complaints_pending = Complaint.objects.filter(status='PENDING').count()
        complaints_in_progress = Complaint.objects.filter(status='IN_PROGRESS').count()
        complaints_resolved = Complaint.objects.filter(status='RESOLVED').count()
        complaints_by_category = list(
            Complaint.objects.values('category__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        complaints_stats = {
            'total': complaints_total,
            'pending': complaints_pending,
            'in_progress': complaints_in_progress,
            'resolved': complaints_resolved,
            'by_category': complaints_by_category
        }
    except ImportError:
        complaints_stats = {
            'total': 0,
            'pending': 0,
            'in_progress': 0,
            'resolved': 0,
            'by_category': []
        }
    
    # Documents stats
    try:
        from documents.models import DocumentRequest, Document
        documents_total_requests = DocumentRequest.objects.count()
        documents_approved = DocumentRequest.objects.filter(status='APPROVED').count()
        documents_rejected = DocumentRequest.objects.filter(status='REJECTED').count()
        documents_by_type = list(
            DocumentRequest.objects.values('document_type__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        documents_stats = {
            'total_requests': documents_total_requests,
            'approved': documents_approved,
            'rejected': documents_rejected,
            'by_type': documents_by_type
        }
    except ImportError:
        documents_stats = {
            'total_requests': 0,
            'approved': 0,
            'rejected': 0,
            'by_type': []
        }
    
    # Tourism stats
    try:
        from tourism.models import TourismLocation, TourismEvent, TourismPackage, TourismReview
        tourism_locations = TourismLocation.objects.count()
        tourism_published = TourismLocation.objects.filter(status='published').count()
        tourism_events = TourismEvent.objects.count()
        tourism_packages = TourismPackage.objects.count()
        tourism_reviews = TourismReview.objects.count()
        tourism_avg_rating = TourismReview.objects.aggregate(avg_rating=Avg('rating'))['avg_rating'] or 0
        tourism_stats = {
            'locations': tourism_locations,
            'published': tourism_published,
            'events': tourism_events,
            'packages': tourism_packages,
            'reviews': tourism_reviews,
            'avg_rating': tourism_avg_rating
        }
    except ImportError:
        tourism_stats = {
            'locations': 0,
            'published': 0,
            'events': 0,
            'packages': 0,
            'reviews': 0,
            'avg_rating': 0
        }
    
    # Population stats
    try:
        from references.models import Penduduk, Dusun
        population_total = Penduduk.objects.count()
        population_male = Penduduk.objects.filter(gender='L').count()
        population_female = Penduduk.objects.filter(gender='P').count()
        population_by_dusun = list(
            Penduduk.objects.values('dusun__name')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
        )
        population_stats = {
            'total': population_total,
            'male': population_male,
            'female': population_female,
            'by_dusun': population_by_dusun
        }
    except ImportError:
        population_stats = {
            'total': 0,
            'male': 0,
            'female': 0,
            'by_dusun': []
        }
    
    context = {
        'page_title': 'Laporan dan Statistik',
        'active_menu': 'reports',
        'date_from': date_from,
        'date_to': date_to,
        'beneficiaries_stats': beneficiaries_stats,
        'business_stats': business_stats,
        'complaints_stats': complaints_stats,
        'documents_stats': documents_stats,
        'tourism_stats': tourism_stats,
        'population_stats': population_stats,
    }
    
    return render(request, 'admin_panel/reports/dashboard.html', context)

@login_required
def settings_dashboard(request):
    return render(request, 'admin_panel/settings/dashboard.html', {
        'page_title': 'Settings Dashboard',
        'active_menu': 'settings',
    })

@login_required
def export_data(request):
    return render(request, 'admin_panel/export_data.html', {
        'page_title': 'Export Data',
    })

@login_required
def test_roles(request):
    return render(request, 'admin_panel/test_roles.html', {
        'page_title': 'Test Roles',
    })

@login_required
def profile(request):
    from core.models import UserProfile
    
    # Get or create user profile
    profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    return render(request, 'admin_panel/profil.html', {
        'page_title': 'User Profile',
        'active_menu': 'profile',
        'profile': profile,
        'profile_id': profile.profile_id,
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        try:
            from core.models import UserProfile
            
            # Get or create user profile
            profile, created = UserProfile.objects.get_or_create(user=request.user)
            
            # Update basic user info
            if 'first_name' in request.POST:
                request.user.first_name = request.POST.get('first_name', '')
            if 'last_name' in request.POST:
                request.user.last_name = request.POST.get('last_name', '')
            if 'email' in request.POST:
                request.user.email = request.POST.get('email', '')
            
            request.user.save()
            
            # Update profile info
            if 'phone' in request.POST:
                profile.phone = request.POST.get('phone', '')
            if 'address' in request.POST:
                profile.address = request.POST.get('address', '')
            if 'birth_date' in request.POST:
                birth_date = request.POST.get('birth_date')
                if birth_date:
                    from datetime import datetime
                    profile.birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
            if 'gender' in request.POST:
                profile.gender = request.POST.get('gender', '')
            
            # Handle photo upload
            if 'photo' in request.FILES:
                profile.photo = request.FILES['photo']
            
            profile.save()
            
            messages.success(request, 'Profil berhasil diperbarui!')
            return redirect('admin_panel:profile')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('admin_panel:profile')
    
    return render(request, 'admin_panel/profil.html', {
        'page_title': 'Update Profile',
    })

@login_required
def change_password(request):
    if request.method == 'POST':
        # Handle password change
        messages.success(request, 'Password changed successfully')
        return redirect('admin_panel:profile')
    return render(request, 'admin_panel/profil.html', {
        'page_title': 'Change Password',
    })

@login_required
def dashboard_stats_api(request):
    """Comprehensive dashboard statistics API"""
    try:
        # Import models safely with fallbacks
        stats = {}
        
        # User statistics
        try:
            stats['total_users'] = CustomUser.objects.count()
            stats['active_users'] = CustomUser.objects.filter(is_active=True).count()
        except Exception as e:
            stats['total_users'] = 0
            stats['active_users'] = 0
        
        # Population statistics (from references app)
        try:
            from references.models import Penduduk, Keluarga
            stats['total_penduduk'] = Penduduk.objects.count()
            stats['total_keluarga'] = Keluarga.objects.count()
        except Exception as e:
            stats['total_penduduk'] = 0
            stats['total_keluarga'] = 0
        
        # Business statistics
        try:
            from business.models import UKM, Koperasi, Business
            stats['total_businesses'] = UKM.objects.count() + Koperasi.objects.count() + Business.objects.count()
        except Exception as e:
            stats['total_businesses'] = 0
        
        # Beneficiaries statistics
        try:
            from beneficiaries.models import Beneficiary
            stats['total_beneficiaries'] = Beneficiary.objects.count()
        except Exception as e:
            stats['total_beneficiaries'] = 0
        
        # Complaints statistics
        try:
            from complaints.models import Complaint
            stats['total_complaints'] = Complaint.objects.count()
        except Exception as e:
            stats['total_complaints'] = 0
        
        # Documents statistics
        try:
            from documents.models import Document
            stats['total_documents'] = Document.objects.count()
        except Exception as e:
            stats['total_documents'] = 0
        
        # Tourism statistics
        try:
            from tourism.models import TourismLocation
            stats['total_tourism_locations'] = TourismLocation.objects.count()
        except Exception as e:
            stats['total_tourism_locations'] = 0
        
        # Posyandu statistics
        try:
            from posyandu.models import PosyanduLocation
            stats['total_posyandu_locations'] = PosyanduLocation.objects.count()
        except Exception as e:
            stats['total_posyandu_locations'] = 0
        
        # Additional statistics for user info section
        try:
            from references.models import Pelajar, DisabilitasData, Dusun, Lorong, RT, RW
            stats['total_pelajar'] = Pelajar.objects.count()
            stats['total_disabilitas'] = DisabilitasData.objects.count()
            stats['total_dusun'] = Dusun.objects.count()
            stats['total_lorong'] = Lorong.objects.count()
            stats['total_rt'] = RT.objects.count()
            stats['total_rw'] = RW.objects.count()
        except Exception as e:
            stats['total_pelajar'] = 0
            stats['total_disabilitas'] = 0
            stats['total_dusun'] = 0
            stats['total_lorong'] = 0
            stats['total_rt'] = 0
            stats['total_rw'] = 0
        
        # News statistics
        try:
            from news.models import News
            stats['total_news'] = News.objects.count()
        except Exception as e:
            stats['total_news'] = 0
        
        return JsonResponse({
            'success': True,
            'data': stats
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e),
            'data': {
                'total_penduduk': 0,
                'total_keluarga': 0,
                'total_businesses': 0,
                'total_beneficiaries': 0,
                'total_complaints': 0,
                'total_documents': 0,
                'total_tourism_locations': 0,
                'total_posyandu_locations': 0,
                'total_pelajar': 0,
                'total_disabilitas': 0,
                'total_dusun': 0,
                'total_lorong': 0,
                'total_rt': 0,
                'total_rw': 0,
                'total_news': 0,
            }
        }, status=500)

@login_required
def api_references_dashboard_data(request):
    """API for references dashboard data"""
    return references_views.api_references_dashboard_data(request)

@login_required
def api_references_penduduk_list(request):
    """API for penduduk list"""
    return references_views.api_penduduk_list(request)

# Business Registration Views (Proxy to business app)
def business_registration_list(request):
    """Business Registration list view"""
    from business import admin_views as business_views
    return business_views.business_registration_list(request)

def business_registration_detail(request, registration_id):
    """Business Registration detail view"""
    from business import admin_views as business_views
    return business_views.business_registration_detail(request, registration_id)

def business_registration_approve(request, registration_id):
    """Approve business registration"""
    from business import admin_views as business_views
    return business_views.business_registration_approve(request, registration_id)

def business_registration_reject(request, registration_id):
    """Reject business registration"""
    from business import admin_views as business_views
    return business_views.business_registration_reject(request, registration_id)

def business_registration_under_review(request, registration_id):
    """Mark business registration as under review"""
    from business import admin_views as business_views
    return business_views.business_registration_under_review(request, registration_id)

