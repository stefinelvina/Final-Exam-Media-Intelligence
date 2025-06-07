# Tropicode Dashboard - Laporan Media Intelligence

Dashboard ini dibuat sebagai bagian dari tugas UAS mata kuliah **Deploying Media Intelligence Web App** yang dibimbing oleh **Dr. Achmad Istamar**.

## Tujuan
Aplikasi ini bertujuan untuk membantu visualisasi dan analisis data media sosial Tropicode, khususnya data dari Instagram, berdasarkan sentimen dan tingkat interaksi (engagement).

## Fitur Utama

1. **Visualisasi Data**
   - Grafik pie distribusi sentimen (positif, negatif, netral)
   - Grafik batang engagement per platform
   - Grafik garis perubahan engagement dari waktu ke waktu
   - Proporsi jenis media
   - Lokasi dengan engagement tertinggi

2. **Ringkasan Statistik**
   - Menampilkan jumlah total data
   - Total engagement
   - Jumlah sentimen positif

3. **Insight Otomatis dari AI**
   - Aplikasi dapat menghasilkan analisis ringkas berdasarkan data yang diunggah
   - Menggunakan model gratis `deepseek/deepseek-r1-0528-qwen3-8b:free` via OpenRouter

4. **Tanya Jawab dengan AI**
   - Pengguna dapat bertanya langsung berdasarkan data yang diunggah
   - Cocok untuk eksplorasi lebih lanjut

5. **Export Laporan**
   - Bisa disimpan dalam format `.txt` dan `.pdf`

## Cara Menggunakan
1. Jalankan perintah:
  py -m streamlit run streamlit_app.py
2. Upload file CSV yang berisi kolom: Date, Platform, Sentiment, Engagements, Location, dan Media_Type.
3. Klik tombol "Generate Insight dari AI" untuk mendapatkan analisis.
4. Gunakan fitur export untuk menyimpan hasil insight.

## Teknologi yang Digunakan
- Python 3.11
- Streamlit
- Plotly Express
- OpenRouter AI
- FPDF

Dikerjakan oleh: [Nama Lengkap]
Univ
Parodi
Semester Genap 2025