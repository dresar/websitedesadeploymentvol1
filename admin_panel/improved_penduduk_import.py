"""
Improved Penduduk Import View
Memastikan data penduduk langsung aktif setelah import
"""

from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction
import pandas as pd
from references.models import Penduduk, Dusun, Lorong

@method_decorator(csrf_exempt, name='dispatch')
class ImprovedPendudukImportView(View):
    """Improved view untuk import data penduduk dengan validasi lengkap"""
    
    def post(self, request):
        try:
            if 'file' not in request.FILES:
                return JsonResponse({
                    'success': False,
                    'error': 'Tidak ada file yang diupload'
                })
            
            file = request.FILES['file']
            skip_errors = request.POST.get('skip_errors', False)
            
            # Validasi file
            if not file.name.endswith(('.xlsx', '.csv')):
                return JsonResponse({
                    'success': False,
                    'error': 'Format file tidak didukung. Gunakan .xlsx atau .csv'
                })
            
            # Process file
            if file.name.endswith('.xlsx'):
                df = pd.read_excel(file)
            else:
                df = pd.read_csv(file)
            
            # Validasi kolom required
            required_columns = ['NIK', 'Nama Lengkap', 'Jenis Kelamin', 'Tempat Lahir', 'Tanggal Lahir', 'Dusun']
            missing_columns = [col for col in required_columns if col not in df.columns]
            
            if missing_columns:
                return JsonResponse({
                    'success': False,
                    'error': f'Kolom yang diperlukan tidak ditemukan: {", ".join(missing_columns)}'
                })
            
            print(f"📊 Processing {len(df)} rows of data...")
            
            # Process data with transaction
            with transaction.atomic():
                success_count = 0
                error_count = 0
                errors = []
                
                for index, row in df.iterrows():
                    try:
                        # Get dusun
                        dusun_name = str(row['Dusun']).strip()
                        dusun = Dusun.objects.filter(name__icontains=dusun_name).first()
                        
                        if not dusun:
                            if not skip_errors:
                                errors.append(f"Baris {index + 2}: Dusun '{dusun_name}' tidak ditemukan")
                                error_count += 1
                                continue
                            else:
                                continue
                        
                        # Get lorong if provided
                        lorong = None
                        if 'Lorong' in df.columns and pd.notna(row['Lorong']):
                            lorong_name = str(row['Lorong']).strip()
                            lorong = Lorong.objects.filter(nama_lorong__icontains=lorong_name, dusun=dusun).first()
                        
                        # Validate required fields
                        if pd.isna(row['Tanggal Lahir']):
                            if not skip_errors:
                                errors.append(f"Baris {index + 2}: Tanggal Lahir harus diisi")
                                error_count += 1
                                continue
                            else:
                                continue
                        
                        # Create penduduk data
                        gender_value = str(row['Jenis Kelamin']).strip().upper()
                        gender_mapping = {
                            'LAKI-LAKI': 'L',
                            'L': 'L',
                            'PEREMPUAN': 'P',
                            'P': 'P'
                        }
                        mapped_gender = gender_mapping.get(gender_value, 'L')
                        
                        penduduk_data = {
                            'nik': str(row['NIK']).strip(),
                            'name': str(row['Nama Lengkap']).strip(),
                            'gender': mapped_gender,
                            'birth_place': str(row['Tempat Lahir']).strip(),
                            'birth_date': pd.to_datetime(row['Tanggal Lahir']).date(),
                            'dusun': dusun,
                            'lorong': lorong,
                            'religion': 'Islam',
                            'marital_status': 'BELUM_KAWIN',
                            'address': str(row.get('Alamat', 'Alamat tidak diisi')).strip() if pd.notna(row.get('Alamat', '')) else 'Alamat tidak diisi',
                            'is_active': True,  # Always True for imported data
                            'is_alive': True,   # Always True for imported data
                            'citizenship': 'WNI',
                        }
                        
                        # Optional fields mapping
                        if 'Agama' in df.columns and pd.notna(row['Agama']):
                            agama_value = str(row['Agama']).strip().upper()
                            agama_mapping = {
                                'ISLAM': 'Islam',
                                'KRISTEN': 'Kristen Protestan',
                                'KATOLIK': 'Kristen Katolik',
                                'HINDU': 'Hindu',
                                'BUDDHA': 'Buddha',
                                'KONGHUCU': 'Konghucu'
                            }
                            penduduk_data['religion'] = agama_mapping.get(agama_value, 'Islam')
                        
                        if 'Status Kawin' in df.columns and pd.notna(row['Status Kawin']):
                            status_value = str(row['Status Kawin']).strip().upper()
                            status_mapping = {
                                'BELUM KAWIN': 'BELUM_KAWIN',
                                'KAWIN': 'KAWIN',
                                'CERAI HIDUP': 'CERAI_HIDUP',
                                'CERAI MATI': 'CERAI_MATI'
                            }
                            penduduk_data['marital_status'] = status_mapping.get(status_value, 'BELUM_KAWIN')
                        
                        # Create or update penduduk
                        penduduk, created = Penduduk.objects.update_or_create(
                            nik=penduduk_data['nik'],
                            defaults=penduduk_data
                        )
                        
                        # Force update to ensure it's active
                        penduduk.is_active = True
                        penduduk.is_alive = True
                        penduduk.save()
                        
                        if created:
                            print(f"✅ Created: {penduduk.name} (NIK: {penduduk.nik})")
                        else:
                            print(f"🔄 Updated: {penduduk.name} (NIK: {penduduk.nik})")
                        
                        success_count += 1
                        
                    except Exception as e:
                        error_msg = f"Baris {index + 2}: {str(e)}"
                        print(f"❌ Error: {error_msg}")
                        if not skip_errors:
                            errors.append(error_msg)
                        error_count += 1
                
                # Final validation
                print(f"\n=== FINAL VALIDATION ===")
                total_penduduk = Penduduk.objects.count()
                active_penduduk = Penduduk.objects.filter(is_active=True).count()
                alive_penduduk = Penduduk.objects.filter(is_alive=True).count()
                
                print(f"Total penduduk: {total_penduduk}")
                print(f"Active penduduk: {active_penduduk}")
                print(f"Alive penduduk: {alive_penduduk}")
                
                # Fix any remaining inactive penduduks
                if active_penduduk < total_penduduk:
                    print("🔧 Fixing remaining inactive penduduks...")
                    fixed_count = Penduduk.objects.filter(is_active=False).update(is_active=True, is_alive=True)
                    print(f"Fixed {fixed_count} penduduks")
                    active_penduduk = Penduduk.objects.filter(is_active=True).count()
                
                # Return response
                if success_count > 0:
                    message = f"Import berhasil! {success_count} data berhasil diimport"
                    if error_count > 0:
                        message += f", {error_count} data error"
                    message += f". Total penduduk aktif: {active_penduduk}"
                    
                    return JsonResponse({
                        'success': True,
                        'message': message,
                        'success_count': int(success_count),
                        'error_count': int(error_count),
                        'total_active_penduduk': active_penduduk,
                        'errors': errors[:10]
                    })
                else:
                    message = f"Import gagal! Tidak ada data yang berhasil diimport. {error_count} data error"
                    return JsonResponse({
                        'success': False,
                        'message': message,
                        'success_count': int(success_count),
                        'error_count': int(error_count),
                        'errors': errors[:10]
                    })
            
        except Exception as e:
            print(f"❌ Import error: {str(e)}")
            return JsonResponse({
                'success': False,
                'error': f'Terjadi kesalahan: {str(e)}'
            })
