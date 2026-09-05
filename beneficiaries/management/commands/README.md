# Management Commands - Beneficiaries

## create_beneficiary_data

Management command untuk membuat data dummy penerima bantuan (beneficiaries) dengan mengambil data dari Penduduk secara random.

### Fitur

Command ini akan membuat:
1. **Header Halaman** - Header untuk halaman penerima bantuan
2. **Kategori Bantuan** - 8 kategori penerima bantuan (Keluarga Miskin, Sangat Miskin, Lansia, Disabilitas, dll)
3. **Program Bantuan** - 7 program bantuan (BLT, BPNT, PKH, Pendidikan, Kesehatan, Perumahan, Modal Usaha)
4. **Data Penerima Bantuan** - 150 penerima bantuan dari data penduduk (random)
5. **Data Taraf Kehidupan** - 100 data taraf kehidupan untuk beneficiaries
6. **Data Bantuan** - Data bantuan yang diterima oleh penduduk
7. **Distribusi Bantuan** - Data distribusi bantuan kepada penerima
8. **Verifikasi** - Data verifikasi penerima bantuan

### Cara Penggunaan

#### 1. Membuat data dummy (default 150 orang)

```bash
python manage.py create_beneficiary_data
```

#### 2. Membuat data dummy dengan jumlah custom

```bash
python manage.py create_beneficiary_data --count 200
```

#### 3. Hapus data lama dan buat data baru

```bash
python manage.py create_beneficiary_data --clear
```

#### 4. Hapus data lama dan buat dengan jumlah custom

```bash
python manage.py create_beneficiary_data --clear --count 100
```

### Catatan Penting

- ⚠️ **Pastikan sudah ada data Penduduk** sebelum menjalankan command ini
- Command ini akan mengambil data penduduk yang aktif (`is_active=True`) dan masih hidup (`is_alive=True`)
- Data dipilih secara **random** dari database Penduduk
- Jika menggunakan `--clear`, semua data beneficiaries yang lama akan **dihapus terlebih dahulu**
- Status ekonomi dan nilai bantuan disesuaikan dengan kategori penerima bantuan
- Data yang dibuat sangat realistis dengan variasi yang beragam

### Contoh Output

```
Mulai membuat data dummy Beneficiaries...

📄 Membuat Page Header...
  ✓ Header halaman berhasil dibuat

📁 Membuat Kategori Penerima Bantuan...
  ✓ Kategori "Keluarga Miskin" berhasil dibuat
  ✓ Kategori "Keluarga Sangat Miskin" berhasil dibuat
  ...

🎁 Membuat Program Bantuan...
  ✓ Program "Bantuan Langsung Tunai (BLT)" berhasil dibuat
  ...

👥 Membuat 150 Data Penerima Bantuan...
  ✓ 10 penerima bantuan berhasil dibuat...
  ✓ 20 penerima bantuan berhasil dibuat...
  ...
  ✓ Total 150 penerima bantuan berhasil dibuat!

📊 Membuat Data Taraf Kehidupan...
  ✓ 100 data taraf kehidupan berhasil dibuat!

💰 Membuat Data Bantuan yang Diterima...
  ✓ 180 data bantuan berhasil dibuat!

📦 Membuat Data Distribusi Bantuan...
  ✓ 120 data distribusi bantuan berhasil dibuat!

✅ Membuat Data Verifikasi...
  ✓ 75 data verifikasi berhasil dibuat!

======================================================================
✓ Semua data dummy Beneficiaries berhasil dibuat! (150 penerima bantuan)
======================================================================
```

### Data yang Dibuat

#### Kategori Penerima Bantuan
- Keluarga Miskin
- Keluarga Sangat Miskin
- Lansia Terlantar
- Disabilitas
- Anak Yatim/Piatu
- Ibu Hamil & Balita
- Korban Bencana
- Pengangguran

#### Program Bantuan
- Bantuan Langsung Tunai (BLT) - Rp 300.000/orang
- Bantuan Pangan Non Tunai (BPNT) - Rp 200.000/orang
- Program Keluarga Harapan (PKH) - Rp 500.000/orang
- Bantuan Pendidikan - Rp 1.000.000/orang
- Bantuan Kesehatan (Jamkesmas) - Rp 150.000/orang
- Bantuan Perumahan - Rp 10.000.000/orang
- Bantuan Modal Usaha - Rp 2.000.000/orang

### Troubleshooting

**Error: Tidak ada data Penduduk**
```
Solusi: Jalankan command untuk membuat data penduduk terlebih dahulu
```

**Error: Kategori sudah ada**
```
Solusi: Gunakan flag --clear untuk menghapus data lama
```


