from django.urls import path
from . import views

app_name = 'documents'

urlpatterns = [
    # Public Documents Views
    path('', views.public_documents_list, name='public_list'),
    path('detail/<slug:slug>/', views.public_document_detail, name='public_detail'),
    path('download/<slug:slug>/', views.public_document_download, name='public_download'),
    
    # Public Pages by Category
    path('transparansi-anggaran/', views.public_transparansi_anggaran, name='transparansi_anggaran'),
    path('produk-hukum/', views.public_produk_hukum, name='produk_hukum'),
    path('profil-desa/', views.public_profil_desa, name='profil_desa'),
    path('laporan/', views.public_laporan, name='laporan'),
]
