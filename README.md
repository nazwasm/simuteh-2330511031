# Praktikum SIMUTEH Computer Vision (P1 - P5)

**NAMA:** Nazwa Syafiya Mirzal
**NIM / SEED:** 2330511031 / 1031
**KELAS:** 7A

## Cara Menjalankan
1. Clone repositori ini ke Google Drive atau eksekusi langsung via Google Colab.
2. Hubungkan (mount) Google Drive di sel pertama setiap *notebook*.
3. Jalankan *notebook* secara berurutan mulai dari `notebook/B1_lingkungan.ipynb` hingga `notebook/B5_praproses.ipynb`.
4. Gunakan opsi **Runtime > Restart and run all** untuk memastikan hasil dapat direproduksi tanpa *error*.

## Ringkasan Hasil (v0.1-praproses)
* **Kanal Warna:** Kanal R (Merah) terbukti paling optimal memisahkan bercak dari daun sehat (KB tertinggi di berbagai kondisi).
* **Perbaikan Cahaya:** Metode CLAHE pada kanal V (dari ruang warna HSV) dengan `clipLimit=2.0` dan `tileGridSize=8x8` berhasil mengangkat detail pada kondisi gelap dan bayangan tanpa menimbulkan *false color*.
* **Penapisan Spasial:** Penapis Median dengan ukuran kernel 5x5 dipilih karena paling tangguh meredam derau *salt-and-pepper* (garam-merica) bawaan sensor sekaligus menjaga batas bercak kecil agar tidak ikut pudar.
* **Parameter Praproses Final:** 
  * Lebar citra: 640px
  * Koreksi Gamma: 1.0 (dinamis)
  * CLAHE: clip 2.0, tile 8
  * Penapis derau: Median, kernel 5
  * Penajaman (Unsharp Mask): Dimatikan (0.0)
