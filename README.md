# Skin Tone Detector

## Overview

Skin Tone Detector adalah aplikasi web berbasis Streamlit yang mendeteksi wajah dari foto (upload atau kamera), lalu menganalisis warna kulit untuk mengklasifikasikannya ke dalam salah satu dari empat kategori — **Fair**, **Light**, **Medium**, atau **Dark** — berdasarkan nilai HSV dari area wajah yang terdeteksi. Berdasarkan hasil klasifikasi, aplikasi menampilkan rekomendasi produk makeup (blush, foundation, lipstick) yang sesuai dengan skin tone tersebut.

## Features

- **Deskripsi Skin Tone** — halaman informasi yang menjelaskan karakteristik masing-masing kategori skin tone (Fair, Light, Medium, Dark).
- **Deteksi via Upload Foto** — upload foto (jpg/png/jpeg), sistem mendeteksi wajah dan menampilkan bounding box sebelum dianalisis.
- **Deteksi via Kamera** — ambil foto langsung dari kamera device untuk dianalisis secara real-time.
- **Klasifikasi Skin Tone** — analisis warna kulit menggunakan deteksi wajah (Haar Cascade) dan perhitungan median HSV pada area wajah.
- **Rekomendasi Produk** — menampilkan rekomendasi blush, foundation, dan lipstick berdasarkan hasil klasifikasi skin tone.
- **Profil Developer** — halaman yang menampilkan daftar anggota tim pengembang.

## Tech Stack

- **[Streamlit](https://streamlit.io/)** — framework untuk membangun antarmuka web aplikasi.
- **[streamlit-option-menu](https://pypi.org/project/streamlit-option-menu/)** — komponen navigasi sidebar.
- **[OpenCV](https://opencv.org/)** (`opencv-python-headless`) — deteksi wajah (Haar Cascade) dan konversi ruang warna (RGB/BGR/HSV).
- **[NumPy](https://numpy.org/)** — operasi array/matriks untuk pemrosesan pixel gambar.
- **[Pillow (PIL)](https://python-pillow.org/)** — pemrosesan dan manipulasi gambar (buka, convert, gambar bounding box).
- **Python** 3.x

## Project Structure

```
Skin-Tone/
├── images/
│   ├── DARK/{Blush,Foundation,Lipstick}/*.png
│   ├── FAIR/{Blush,Foundation,Lipstick}/*.png
│   ├── LIGHT/{Blush,Foundation,Lipstick}/*.png
│   ├── MEDIUM/{Blush,Foundation,Lipstick}/*.png
│   └── Teams.jpg
├── mainsec.py          # entry point aplikasi
├── main_test.py         # file eksperimen (belum stabil, jangan dijalankan)
└── requirements.txt
```

## Run in Dev

1. **Clone repository & masuk ke folder project**
   ```bash
   git clone <repo-url>
   cd Skin-Tone
   ```

2. **Buat virtual environment** (disarankan)
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. **Install dependencies**
   ```powershell
   pip install -r requirements.txt
   ```

4. **Jalankan aplikasi**
   ```powershell
   streamlit run mainsec.py
   ```

   Aplikasi akan otomatis terbuka di browser pada `http://localhost:8501`.

### Catatan

- `main_test.py` adalah file eksperimen terpisah dan tidak perlu dijalankan — gunakan `mainsec.py` sebagai entry point utama.
- Jika mengalami error `AttributeError: module 'cv2' has no attribute 'CascadeClassifier'`, pastikan versi `opencv-python-headless` yang terinstall adalah versi 4.x (bukan 5.x), karena OpenCV 5.x mengubah layout binding Python-nya.
