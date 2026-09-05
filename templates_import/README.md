# 📋 Templates Import Data

Folder ini berisi template Excel untuk import berbagai jenis data ke sistem Desa Pulosarok.

## 📁 Struktur Folder

```
templates_import/
├── excel_templates/          # Template kosong untuk import
├── sample_data/            # Contoh data untuk testing
├── generate_templates.py   # Script untuk generate templates
└── README.md              # Dokumentasi ini
```

## 📊 Template yang Tersedia

### 1. **Penduduk** (`template_import_penduduk.xlsx`)
Template untuk import data penduduk desa.

**Kolom yang diperlukan:**
- `NIK` - Nomor Induk Kependudukan (16 digit)
- `Nama Lengkap` - Nama lengkap penduduk
- `Jenis Kelamin` - `L` (Laki-laki) atau `P` (Perempuan)
- `Tempat Lahir` - Tempat lahir
- `Tanggal Lahir` - Format: `YYYY-MM-DD`
- `Agama` - Pilihan: `Islam`, `Kristen Protestan`, `Kristen Katolik`, `Hindu`, `Buddha`, `Konghucu`, `Kepercayaan`
- `Pendidikan` - Pilihan: `TIDAK_BELUM_SEKOLAH`, `BELUM_TAMAT_SD`, `TAMAT_SD`, `SLTP`, `SLTA`, `D1`, `D2`, `D3`, `D4_S1`, `S2`, `S3`
  - **Format Alternatif yang Didukung**: `TIDAK SEKOLAH`, `SD`, `TAMATSD`, `SMP`, `SMA`, `D4`, `S1`
- `Pekerjaan` - Pekerjaan penduduk
- `Status Perkawinan` - Pilihan: `BELUM_KAWIN`, `KAWIN`, `CERAI_HIDUP`, `CERAI_MATI`
  - **Format Alternatif yang Didukung**: `BELUM KAWIN`, `CERAI HIDUP`, `CERAIHIDUP`, `CERAI MATI`, `CERAIMATI`
- `Golongan Darah` - Pilihan: `A`, `B`, `AB`, `O`
- `Nomor Telepon` - Nomor telepon
- `Email` - Alamat email
- `Dusun` - Nama dusun (opsional)
- `Lorong` - Nama lorong (opsional)
- `RW` - Nomor RW (opsional)
- `RT` - Nomor RT (opsional)
- `Nomor Rumah` - Nomor rumah
- `Alamat` - Alamat lengkap
- `Kewarganegaraan` - `WNI` atau `WNA`
- `Status Aktif` - `Aktif` atau `Tidak Aktif`
- `Status Hidup` - `Hidup` atau `Meninggal`

### 2. **Dusun** (`template_import_dusun.xlsx`)
Template untuk import data dusun/hamlet.

**Kolom yang diperlukan:**
- `Nama Dusun` - Nama dusun
- `Kode Dusun` - Kode unik dusun
- `Deskripsi` - Deskripsi dusun
- `Luas Area (Hektar)` - Luas area dalam hektar
- `Status Aktif` - `True` atau `False`

### 3. **Lorong** (`template_import_lorong.xlsx`)
Template untuk import data lorong/gang.

**Kolom yang diperlukan:**
- `Nama Lorong` - Nama lorong
- `Kode Lorong` - Kode unik lorong
- `Dusun` - Nama dusun tempat lorong berada
- `Deskripsi` - Deskripsi lorong
- `Status Aktif` - `True` atau `False`

### 4. **RW** (`template_import_rw.xlsx`)
Template untuk import data Rukun Warga.

**Kolom yang diperlukan:**
- `Nomor RW` - Nomor RW
- `Kode RW` - Kode unik RW
- `Dusun` - Nama dusun tempat RW berada
- `Ketua RW` - Nama ketua RW
- `Deskripsi` - Deskripsi RW
- `Status Aktif` - `True` atau `False`

### 5. **RT** (`template_import_rt.xlsx`)
Template untuk import data Rukun Tetangga.

**Kolom yang diperlukan:**
- `Nomor RT` - Nomor RT
- `Kode RT` - Kode unik RT
- `RW` - Nomor RW tempat RT berada
- `Ketua RT` - Nama ketua RT
- `Deskripsi` - Deskripsi RT
- `Status Aktif` - `True` atau `False`

### 6. **Keluarga** (`template_import_keluarga.xlsx`)
Template untuk import data keluarga.

**Kolom yang diperlukan:**
- `Nomor KK` - Nomor Kartu Keluarga
- `Nama Kepala Keluarga` - Nama kepala keluarga
- `NIK Kepala Keluarga` - NIK kepala keluarga
- `Alamat` - Alamat keluarga
- `Dusun` - Nama dusun
- `Lorong` - Nama lorong
- `RW` - Nomor RW
- `RT` - Nomor RT
- `Nomor Rumah` - Nomor rumah
- `Kode Pos` - Kode pos
- `Status Aktif` - `True` atau `False`

### 7. **Pelajar** (`template_import_pelajar.xlsx`)
Template untuk import data pelajar/mahasiswa.

**Kolom yang diperlukan:**
- `NIK` - NIK pelajar
- `Nama Lengkap` - Nama lengkap pelajar
- `Jenis Kelamin` - `L` atau `P`
- `Tanggal Lahir` - Format: `YYYY-MM-DD`
- `Sekolah` - Nama sekolah/kampus
- `Kelas` - Kelas/jurusan
- `Jurusan` - Jurusan (untuk SMA/PT)
- `Status Pendidikan` - `AKTIF`, `LULUS`, `PUTUS`
- `Nama Orang Tua` - Nama orang tua
- `Nomor Telepon Orang Tua` - Nomor telepon orang tua
- `Alamat` - Alamat pelajar
- `Dusun` - Nama dusun
- `Status Aktif` - `True` atau `False`

### 8. **Disabilitas** (`template_import_disabilitas.xlsx`)
Template untuk import data penyandang disabilitas.

**Kolom yang diperlukan:**
- `NIK` - NIK penyandang disabilitas
- `Nama Lengkap` - Nama lengkap
- `Jenis Disabilitas` - Jenis disabilitas
- `Tingkat Disabilitas` - `RINGAN`, `SEDANG`, `BERAT`
- `Tanggal Diagnosis` - Format: `YYYY-MM-DD`
- `Dokter` - Nama dokter yang mendiagnosis
- `Rumah Sakit` - Nama rumah sakit
- `Keterangan` - Keterangan tambahan
- `Status Aktif` - `True` atau `False`

## 🚀 Cara Penggunaan

### 1. **Download Template**
- Pilih template yang sesuai dengan data yang akan diimport
- Download file Excel dari folder `excel_templates/`

### 2. **Isi Data**
- Buka file Excel template
- Isi data sesuai dengan format yang ditentukan
- Pastikan menggunakan nilai yang valid untuk setiap kolom

### 3. **Import Data**
- Buka halaman import di sistem: `http://localhost:8000/admin-panel/references/global-import/`
- Upload file Excel yang sudah diisi
- Pilih opsi "Validasi Saja" untuk mengecek data terlebih dahulu
- Jika tidak ada error, hapus centang "Validasi Saja" dan import data

### 4. **Troubleshooting**

#### Error Umum:
- **Error "Nilai 'X' bukan pilihan yang valid"**: 
  - Pastikan menggunakan format yang benar untuk field choices
  - Gunakan format alternatif yang didukung (lihat dokumentasi di atas)
  - Contoh: Gunakan `CERAI_HIDUP` bukan `CERAIHIDUP`, atau `TAMAT_SD` bukan `TAMATSD`

- **Error NIK**: 
  - Pastikan NIK berupa 16 digit angka
  - Tidak boleh ada spasi atau karakter khusus

- **Error Tanggal**: 
  - Gunakan format `YYYY-MM-DD`
  - Contoh: `1990-01-01` bukan `01/01/1990`

#### Tips Import:
- Jika ada error validation, periksa kembali format data
- Pastikan menggunakan nilai yang valid sesuai dengan pilihan yang tersedia
- Untuk field yang opsional, bisa dikosongkan atau diisi dengan `null`
- **Sistem sudah mendukung format alternatif** untuk field choices, jadi tidak perlu khawatir dengan variasi penulisan

## 📝 Catatan Penting

1. **Format Tanggal**: Selalu gunakan format `YYYY-MM-DD` (contoh: `1990-01-01`)
2. **NIK**: Harus berupa angka 16 digit
3. **Pilihan Terbatas**: Beberapa field memiliki pilihan terbatas, pastikan menggunakan nilai yang benar
4. **Field Opsional**: Field yang tidak wajib bisa dikosongkan
5. **Validasi**: Selalu gunakan opsi "Validasi Saja" terlebih dahulu sebelum import data

## 🔄 Regenerate Templates

Jika ingin membuat ulang semua template:

```bash
cd templates_import
python generate_templates.py
```

## 📞 Bantuan

Jika mengalami kesulitan atau ada pertanyaan, silakan hubungi administrator sistem.
