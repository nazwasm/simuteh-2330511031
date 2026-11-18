# Praktikum SIMUTEH Computer Vision (P1 - P6)
**NAMA:** Nazwa Syafiya Mirzal | **NIM / SEED:** 2330511031 / 1031 | **KELAS:** 7A

## Cara Menjalankan
1. Clone repositori ini ke Google Drive atau eksekusi langsung via Google Colab.
2. Hubungkan (mount) Google Drive di sel pertama setiap notebook.
3. Jalankan notebook secara berurutan:
   - Evaluasi P1-P4: `notebook/B1_lingkungan.ipynb` hingga `notebook/B5_praproses.ipynb`
   - Pertemuan 5 (Deteksi Tepi): `notebook/P5_tepi.ipynb`
   - Pertemuan 6 (Morfologi & Komponen Terhubung): `notebook/P6_morfologi.ipynb`
4. Gunakan opsi **Runtime > Restart and run all** untuk memastikan hasil dapat direproduksi tanpa error.

---

## Ringkasan Hasil (v0.1-praproses)
- **Kanal Warna:** Kanal R (Merah) terbukti paling optimal memisahkan bercak dari daun sehat (KB tertinggi di berbagai kondisi).
- **Perbaikan Cahaya:** Metode CLAHE pada kanal V (dari ruang warna HSV) dengan `clipLimit=2.0` dan `tileGridSize=8x8` berhasil mengangkat detail pada kondisi gelap dan bayangan tanpa menimbulkan *false color*.
- **Penapisan Spasial:** Penapis Median dengan ukuran kernel 5x5 dipilih karena paling tangguh meredam derau *salt-and-pepper* (garam-merica) bawaan sensor sekaligus menjaga batas bercak kecil agar tidak ikut pudar.
- **Parameter Praproses Final:**
  - Lebar citra: 640px
  - Koreksi Gamma: 1.0 (dinamis)
  - CLAHE: clip 2.0, tile 8
  - Penapis derau: Median, kernel 5
  - Penajaman (Unsharp Mask): Dimatikan (0.0)

---

## Ringkasan Hasil Pertemuan 5 — Deteksi Tepi (v0.2-tepi)
- **Perbandingan Operator & Kanal (40 Citra Berbercak):**
  Kanal **R** sesudah praproses menghasilkan rerata skor **F1** tertinggi dibandingkan kanal Gray pada seluruh operator:
  - **Canny (`30/90, sigma=2.0`):** `F1 = 0.981` (`P = 0.975`, `R = 0.986`)
  - **LoG (`sigma=3.0, frac=0.2`):** `F1 = 0.949` (`P = 0.912`, `R = 0.997`)
  - **Prewitt (`T = 75`):** `F1 = 0.928` (`P = 0.873`, `R = 0.996`)
  - **Sobel (`T = 100`):** `F1 = 0.924` (`P = 0.867`, `R = 0.996`)
- **Parameter Canny & Perbaikan Ambang Otomatis (`canny_persentil`):**
  - Kombinasi `sigma = 1.0, ambang = 100/200` meraih F1 total tertinggi (`0.988`), sedangkan `sigma = 2.0, ambang = 30/90` (`F1 = 0.981`) dan `sigma = 1.0, ambang = 50/150` (`F1 = 0.984`) menjaga *recall* tepi bercak ringan tetap tinggi (`0.900 - 0.914`).
  - Ambang otomatis berbasis persentil magnitudo gradien (`canny_persentil`) bekerja optimal pada **`q = 98`** (`F1 = 0.971` di kanal R), sesuai proporsi piksel tepi (~2% luas citra).
- **Tepi Palsu pada Daun Sehat & Keputusan Pemakaian Tepi:**
  - Kanal R menghasilkan **`0.0 piksel`** tepi palsu di bagian dalam daun sehat pada seluruh kondisi cahaya, sedangkan kanal Gray menghasilkan **`654.8 - 877.2 piksel`** tepi palsu akibat tulang daun.
  - Deteksi tepi tidak digunakan untuk mengisi wilayah bercak (segmentasi luas), melainkan digantikan oleh pengambangan intensitas kanal R dan operasi morfologi pada Pertemuan 6.

---

## Ringkasan Hasil Pertemuan 6 — Morfologi & Modul Bercak (v0.3-morfologi)
- **Operasi Morfologi & Penyaringan Komponen:**
  - Menggunakan ambang awal `bercak_awal` pada **kanal R (`kanal = 2, k = 4.0`)**, diikuti operasi **Opening (`se_open = 5`)** lalu **Closing (`se_close = 5`)** dengan *Structuring Element* berbentuk **elips (`se_bentuk = "elips"`)**.
  - Penyaringan komponen terhubung (konektivitas 8) berdasarkan ukuran dan bentuk (**`luas_min = 20` px**, **`bulat_min = 0.5`**, dan **`rasio_maks = 1.8`**) menurunkan galat jumlah bercak ke titik terendah (`1.25` pada kelas berat, `0.90` pada kelas ringan, dan `1.20` pada kelas sehat).
- **Evaluasi Modul `src/bercak.py` pada 60 Citra:**
  - **Galat absolut rerata (MAE) persen bercak:** `0.575%`
  - **Korelasi persen prediksi vs acuan:** `0.957`
  - **Akurasi klasifikasi kelas mutu:** `0.867` (**86.7%** — 52/60 citra tepat; `Bercak Berat` 20/20 tepat, `Bercak Ringan` 16/20 tepat, `Sehat` 16/20 tepat).

---

## Cara Memakai `analisis_daun` (`src/bercak.py`)
```python
import sys, json
sys.path.append("src")
from utils_cv import baca
from praproses import praproses
from bercak import analisis_daun

# 1. Muat parameter praproses dan parameter bercak
param_pra = json.load(open("hasil/param_praproses.json"))
param_bercak = json.load(open("hasil/param_bercak.json"))

# 2. Baca citra, jalankan praproses, dan analisis bercak
img = baca("data/sintetis/citra/teh_041.png")
img_pra = praproses(img, param_pra)
hasil = analisis_daun(img_pra, param_bercak)

print("Jumlah bercak :", hasil["jumlah_bercak"])
print("Persen bercak :", hasil["persen_bercak"], "%")
print("Kelas mutu    :", hasil["kelas"])
```
