"""
Script untuk generate template Excel untuk import data
"""
import pandas as pd
import os
from datetime import date

def create_penduduk_template():
    """Template untuk import data Penduduk"""
    # Header dengan format yang benar
    template_data = {
        'NIK': ['Contoh: 1234567890123456'],
        'Nama Lengkap': ['Contoh: John Doe'],
        'Jenis Kelamin': ['L atau P'],
        'Tempat Lahir': ['Contoh: Jakarta'],
        'Tanggal Lahir': ['Format: YYYY-MM-DD (Contoh: 1990-01-01)'],
        'Agama': ['Islam, Kristen Protestan, Kristen Katolik, Hindu, Buddha, Konghucu, Kepercayaan'],
        'Pendidikan': ['TIDAK_BELUM_SEKOLAH, BELUM_TAMAT_SD, TAMAT_SD, SLTP, SLTA, D1, D2, D3, D4_S1, S2, S3'],
        'Pekerjaan': ['Contoh: Karyawan'],
        'Status Perkawinan': ['BELUM_KAWIN, KAWIN, CERAI_HIDUP, CERAI_MATI'],
        'Golongan Darah': ['A, B, AB, O'],
        'Nomor Telepon': ['Contoh: 081234567890'],
        'Email': ['Contoh: john@email.com'],
        'Dusun': ['Contoh: Dusun A (Opsional)'],
        'Lorong': ['Contoh: Lorong 1 (Opsional)'],
        'RW': ['Contoh: 001 (Opsional)'],
        'RT': ['Contoh: 001 (Opsional)'],
        'Nomor Rumah': ['Contoh: 001'],
        'Alamat': ['Contoh: Jl. Test 1'],
        'Kewarganegaraan': ['WNI atau WNA'],
        'Status Aktif': ['Aktif atau Tidak Aktif'],
        'Status Hidup': ['Hidup atau Meninggal']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_penduduk.xlsx', index=False)
    print("Template Penduduk berhasil dibuat!")

def create_penduduk_sample():
    """Sample data untuk Penduduk"""
    sample_data = {
        'NIK': ['1234567890123456', '1234567890123457', '1234567890123458'],
        'Nama Lengkap': ['John Doe', 'Jane Smith', 'Bob Johnson'],
        'Jenis Kelamin': ['L', 'P', 'L'],
        'Tempat Lahir': ['Jakarta', 'Bandung', 'Surabaya'],
        'Tanggal Lahir': ['1990-01-01', '1991-02-02', '1992-03-03'],
        'Agama': ['Islam', 'Kristen Protestan', 'Islam'],
        'Pendidikan': ['SLTA', 'D4_S1', 'SLTA'],
        'Pekerjaan': ['Karyawan', 'Guru', 'Wiraswasta'],
        'Status Perkawinan': ['BELUM_KAWIN', 'KAWIN', 'BELUM_KAWIN'],
        'Golongan Darah': ['A', 'B', 'O'],
        'Nomor Telepon': ['081234567890', '081234567891', '081234567892'],
        'Email': ['john@email.com', 'jane@email.com', 'bob@email.com'],
        'Dusun': ['Dusun A', 'Dusun B', 'Dusun C'],
        'Lorong': ['Lorong 1', 'Lorong 2', 'Lorong 3'],
        'RW': ['001', '002', '003'],
        'RT': ['001', '002', '003'],
        'Nomor Rumah': ['001', '002', '003'],
        'Alamat': ['Jl. Test 1', 'Jl. Test 2', 'Jl. Test 3'],
        'Kewarganegaraan': ['WNI', 'WNI', 'WNI'],
        'Status Aktif': ['Aktif', 'Aktif', 'Aktif'],
        'Status Hidup': ['Hidup', 'Hidup', 'Hidup']
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel('sample_data/sample_data_penduduk.xlsx', index=False)
    print("Sample data Penduduk berhasil dibuat!")

def create_dusun_template():
    """Template untuk import data Dusun"""
    template_data = {
        'Nama Dusun': ['Contoh: Dusun A'],
        'Kode Dusun': ['Contoh: D001'],
        'Deskripsi': ['Contoh: Dusun A - Wilayah Utara'],
        'Luas Area (Hektar)': ['Contoh: 5.5'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_dusun.xlsx', index=False)
    print("Template Dusun berhasil dibuat!")

def create_dusun_sample():
    """Sample data untuk Dusun"""
    sample_data = {
        'Nama Dusun': ['Dusun A', 'Dusun B', 'Dusun C'],
        'Kode Dusun': ['D001', 'D002', 'D003'],
        'Deskripsi': ['Dusun A - Wilayah Utara', 'Dusun B - Wilayah Selatan', 'Dusun C - Wilayah Timur'],
        'Luas Area (Hektar)': [5.5, 7.2, 4.8],
        'Status Aktif': [True, True, True]
    }
    
    df = pd.DataFrame(sample_data)
    df.to_excel('sample_data/sample_data_dusun.xlsx', index=False)
    print("Sample data Dusun berhasil dibuat!")

def create_lorong_template():
    """Template untuk import data Lorong"""
    template_data = {
        'Nama Lorong': ['Contoh: Lorong 1'],
        'Kode Lorong': ['Contoh: L001'],
        'Dusun': ['Contoh: Dusun A'],
        'Deskripsi': ['Contoh: Lorong 1 - Jalan Utama'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_lorong.xlsx', index=False)
    print("Template Lorong berhasil dibuat!")

def create_rw_template():
    """Template untuk import data RW"""
    template_data = {
        'Nomor RW': ['Contoh: 001'],
        'Kode RW': ['Contoh: RW001'],
        'Dusun': ['Contoh: Dusun A'],
        'Ketua RW': ['Contoh: Nama Ketua RW'],
        'Deskripsi': ['Contoh: RW 001 - Wilayah Utara'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_rw.xlsx', index=False)
    print("Template RW berhasil dibuat!")

def create_rt_template():
    """Template untuk import data RT"""
    template_data = {
        'Nomor RT': ['Contoh: 001'],
        'Kode RT': ['Contoh: RT001'],
        'RW': ['Contoh: 001'],
        'Ketua RT': ['Contoh: Nama Ketua RT'],
        'Deskripsi': ['Contoh: RT 001 - Wilayah Utara'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_rt.xlsx', index=False)
    print("Template RT berhasil dibuat!")

def create_keluarga_template():
    """Template untuk import data Keluarga"""
    template_data = {
        'Nomor KK': ['Contoh: 1234567890123456'],
        'Nama Kepala Keluarga': ['Contoh: John Doe'],
        'NIK Kepala Keluarga': ['Contoh: 1234567890123456'],
        'Alamat': ['Contoh: Jl. Test 1'],
        'Dusun': ['Contoh: Dusun A'],
        'Lorong': ['Contoh: Lorong 1'],
        'RW': ['Contoh: 001'],
        'RT': ['Contoh: 001'],
        'Nomor Rumah': ['Contoh: 001'],
        'Kode Pos': ['Contoh: 12345'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_keluarga.xlsx', index=False)
    print("Template Keluarga berhasil dibuat!")

def create_pelajar_template():
    """Template untuk import data Pelajar"""
    template_data = {
        'NIK': ['Contoh: 1234567890123456'],
        'Nama Lengkap': ['Contoh: John Doe'],
        'Jenis Kelamin': ['L atau P'],
        'Tanggal Lahir': ['Format: YYYY-MM-DD'],
        'Sekolah': ['Contoh: SD Negeri 1'],
        'Kelas': ['Contoh: 6A'],
        'Jurusan': ['Contoh: IPA (untuk SMA)'],
        'Status Pendidikan': ['AKTIF, LULUS, PUTUS'],
        'Nama Orang Tua': ['Contoh: Jane Doe'],
        'Nomor Telepon Orang Tua': ['Contoh: 081234567890'],
        'Alamat': ['Contoh: Jl. Test 1'],
        'Dusun': ['Contoh: Dusun A'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_pelajar.xlsx', index=False)
    print("Template Pelajar berhasil dibuat!")

def create_disabilitas_template():
    """Template untuk import data Disabilitas"""
    template_data = {
        'NIK': ['Contoh: 1234567890123456'],
        'Nama Lengkap': ['Contoh: John Doe'],
        'Jenis Disabilitas': ['TUNANETRA, TUNARUNGU, TUNAGRAHITA, TUNALARAS, TUNARUNGU, TUNANETRA, TUNANETRA, TUNANETRA'],
        'Tingkat Disabilitas': ['RINGAN, SEDANG, BERAT'],
        'Tanggal Diagnosis': ['Format: YYYY-MM-DD'],
        'Dokter': ['Contoh: Dr. Smith'],
        'Rumah Sakit': ['Contoh: RS Umum'],
        'Keterangan': ['Contoh: Keterangan tambahan'],
        'Status Aktif': ['True atau False']
    }
    
    df = pd.DataFrame(template_data)
    df.to_excel('excel_templates/template_import_disabilitas.xlsx', index=False)
    print("Template Disabilitas berhasil dibuat!")

def main():
    """Generate semua template"""
    print("Membuat template Excel untuk import data...")
    print("=" * 50)
    
    # Buat folder jika belum ada
    os.makedirs('excel_templates', exist_ok=True)
    os.makedirs('sample_data', exist_ok=True)
    
    # Generate templates
    create_penduduk_template()
    create_penduduk_sample()
    create_dusun_template()
    create_dusun_sample()
    create_lorong_template()
    create_rw_template()
    create_rt_template()
    create_keluarga_template()
    create_pelajar_template()
    create_disabilitas_template()
    
    print("=" * 50)
    print("Semua template berhasil dibuat!")
    print("\nFile yang dibuat:")
    print("excel_templates/")
    print("   - template_import_penduduk.xlsx")
    print("   - template_import_dusun.xlsx")
    print("   - template_import_lorong.xlsx")
    print("   - template_import_rw.xlsx")
    print("   - template_import_rt.xlsx")
    print("   - template_import_keluarga.xlsx")
    print("   - template_import_pelajar.xlsx")
    print("   - template_import_disabilitas.xlsx")
    print("\nsample_data/")
    print("   - sample_data_penduduk.xlsx")
    print("   - sample_data_dusun.xlsx")

if __name__ == "__main__":
    main()
