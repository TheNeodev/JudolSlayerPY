# JudolSlayerPY

**JudolSlayerPY** adalah alat berbasis Python yang menggunakan YouTube Data API v3 untuk mendeteksi dan menghapus komentar spam dari video di channel YouTube Anda. Proyek ini dirancang untuk membantu kreator konten menjaga kebersihan kolom komentar mereka dari spam dan komentar yang tidak diinginkan.

## Fitur

- **Otentikasi OAuth 2.0**: Menggunakan OAuth 2.0 untuk otorisasi akses ke YouTube Data API.
- **Deteksi Komentar Spam**: Mendeteksi komentar spam berdasarkan normalisasi Unicode dan daftar kata-kata terlarang yang ditentukan dalam `blockedword.json`.
- **Penghapusan Komentar Spam**: Menghapus komentar yang terdeteksi sebagai spam dengan mengubah status moderasinya menjadi "rejected".
- **Pengambilan Daftar Video**: Mengambil daftar semua video yang diunggah ke channel YouTube Anda untuk dianalisis.

## Persiapan

Sebelum menjalankan aplikasi ini, ikuti langkah-langkah berikut:

1. **Clone Repository**  
   Clone repository ini ke komputer lokal Anda:
   ```bash
   git clone https://github.com/TheNeodev/JudolSlayerPY.git
   cd JudolSlayerPY

2. **Instal Python**
Pastikan Python telah terinstal di sistem Anda. Anda dapat mengunduhnya dari [python.org](https://python.org)

4. **Instal Visual Studio Code**
Disarankan untuk menggunakan [Visual Studio Code](https://code.visualstudio.com/) sebagai editor kode Anda.


5. **Aktifkan YouTube Data API dan Buat OAuth Client ID**

- Kunjungi Google Cloud Console.
Aktifkan YouTube Data API v3 untuk proyek Anda.
Buat OAuth Client ID untuk aplikasi desktop dan unduh file `credentials.json`.

6. **Buka Terminal di VS Code**

 - Buka terminal di Visual Studio Code untuk menjalankan perintah CLI.


7. **Siapkan File yang Diperlukan**
Pastikan file-file berikut tersedia di direktori proyek:
- `credentials.json`: Kredensial OAuth 2.0 dari Google Cloud Console.


- `.env`: File konfigurasi lingkungan.

  8. **Edit File .env**

- Buka file `.env` dan atur variabel YOUTUBE_CHANNEL_ID sesuai dengan ID channel YouTube Anda:
```
YOUTUBE_CHANNEL_ID=ID_CHANNEL_ANDA

```
> [!NOTE]  
> Channel ID dapat ditemukan pada laman: https://www.youtube.com/account_advanced



9. **Jalankan Aplikasi**
Setelah semua pengaturan selesai, jalankan aplikasi dengan perintah:

```
python main.py
```

# Struktur Proyek

```
JudolSlayerPY/
├── .env                  # File konfigurasi lingkungan
├── src/blockedword.json      # Daftar kata-kata terlarang(judol)
├── credentials.json      # Kredensial OAuth 2.0
├── token.json            # Token hasil otorisasi (dihasilkan otomatis)
├── requirements.txt      # Daftar dependensi Python
└── main.py               # File utama aplikasi

```

# Catatan Tambahan
Pastikan akun Google Anda memiliki akses ke channel YouTube yang akan dianalisis.

Simpan file `credentials.json` dan `token.json` dengan aman dan jangan dibagikan secara publik.

Jika mengalami masalah saat otorisasi, pastikan tanggal dan waktu sistem Anda sudah benar

# Lisensi
Proyek ini dilisensikan di bawah [BSD-3-Clause license](https://github.com/TheNeodev/JudolSlayerPY/tree/main#).


# Kontak
Untuk pertanyaan atau saran, silakan buka issue di repository ini atau hubungi pengembang melalui [GitHub](https://github.com/TheNeodev).


