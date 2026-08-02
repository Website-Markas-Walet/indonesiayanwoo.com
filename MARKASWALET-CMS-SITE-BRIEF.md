# Potret Diri untuk Integrasi CMS — indonesiayanwoo.com

> Dokumen ini ditulis dari sudut pandang situs **indonesiayanwoo.com** sendiri, apa adanya,
> agar CMS terpusat **app.markaswalet.id** menyesuaikan diri ke kondisi nyataku — bukan sebaliknya.
> Semua angka di bawah adalah hasil pemindaian langsung atas isi repo, bukan asumsi.

---

## 1. Identitas Hosting — di mana & bagaimana aku hidup

| Hal | Kenyataan |
|---|---|
| Repo | `Website-Markas-Walet/indonesiayanwoo.com` |
| Hosting | **GitHub Pages** (static hosting) |
| Domain | `indonesiayanwoo.com` — diikat lewat file `CNAME` di root |
| Cara publish | **`git push` = langsung live.** Tidak ada build, tidak ada staging |
| `.nojekyll` | **TIDAK ADA** -> GitHub Pages menjalankan Jekyll. File/folder berawalan `_` bisa hilang diam-diam. Jebakan yang harus disadari CMS |
| CI/Action | **Tidak ada.** Tidak ada `.github/workflows`, tidak ada `package.json` |

**Konsekuensi:** satu-satunya "API" untuk mengubahku adalah **GitHub API / git commit**. Tidak ada endpoint dinamis.

---

## 2. Saya ini sebenarnya apa

Aku **bukan** WordPress hidup. Aku **hasil export statis (snapshot beku) dari WordPress**, file HTML-nya di-commit mentah ke GitHub Pages.

- Mesin asal: **WordPress 6.2.2**, tema **Astra**
- Digenerate plugin **Simply Static** (jejak di `wp-content/uploads/simply-static/`)
- SEO/sitemap dulu diurus **Rank Math**
- Folder `wp-json/`, `wp-content/`, `wp-includes/` **hanya cangkang statis** — bukan REST API WordPress.

Artinya: **CMS harus memperlakukanku sebagai kumpulan file HTML statis di git, bukan WordPress.**

---

## 3. Tipe konten yang BENAR-BENAR aku punya

| Tipe | Jumlah | Pola URL |
|---|---|---|
| **Post / artikel** | **194** | `/slug-artikel.html` |
| **Page statis** | **10** | `/tentang`, `/produk`, `/layanan/konsultasi` (folder + index.html) |
| **Halaman Kota** | **489** | `/kota/jual-sarang-walet-di-<kota>.html` |
| **Halaman Desain** | **5** | `/desain/desain-rumah-...` (folder, tanpa .html) |

- Total halaman bernilai SEO: **~698**. Total file .html di repo: **1.726** (sisanya arsip/paginasi/feed).
- Menu bar utama **hanya 3 item**: Home (/), Produk (/produk), Blog (/blog).
- Aset terbesar = **489 halaman kota** hasil generate massal.

---

## 4. Chrome bersama yang TERDUPLIKASI (masalah inti)

Header, menu, footer **ditempel penuh ke SETIAP file HTML**.

- Blok menu diulang **3x** dalam satu file (desktop + mobile + off-canvas).
- **~60% bobot tiap file = CSS inline (~115 KB) + JS (~10 KB)** identik di semua halaman.
- Tidak ada partial/layout. Tidak ada sumber tunggal.

**Keterbatasan:** ganti 1 item menu/footer hari ini = sunting ~698 file. "Edit sekali, berubah semua" **belum mungkin** sebelum refactor ke template.

---

## 5. Peta URL (WAJIB dijaga — nyawa SEO)

| Tipe | Ekstensi | Contoh |
|---|---|---|
| Artikel | **pakai .html** | `/manfaat-sarang-burung-walet-...html` |
| Kota | **pakai .html** | `/kota/jual-sarang-walet-di-sibolga-sumatra-utara.html` |
| Page | **tanpa ekstensi** | `/layanan/konsultasi` |
| Desain | **tanpa ekstensi** | `/desain/desain-rumah-burung-walet-ukuran-8x8-...` |

Aturan keras: **DILARANG ubah URL tanpa 301.** Ganti slug = hilang ranking.

---

## 6. Kondisi Media (paling rapuh)

**a) Lokal (aman):** `wp-content/uploads/` = **175 file, ~88 MB** (logo, favicon, featured).

**b) Gambar isi artikel (RAPUH — mayoritas hotlink eksternal):**

| Sumber | Ref | Status |
|---|---|---|
| `1.bp.blogspot.com` | 392 | eksternal |
| `cdn-ak.f.st-hatena.com` | 159 | eksternal (CDN Jepang) |
| lain-lain | ~24 | eksternal |
| milik sendiri | 11 | lokal |

Ratusan gambar bisa mati kapan saja. Tugas awal CMS: **rehome** hotlink -> R2/uploads -> perbarui src.

---

## 7. Intinya untuk app.markaswalet.id

1. **Situs statis GitHub Pages.** Menulis hanya via commit GitHub API. Bukan WordPress, bukan REST API.
2. **Belum ada template.** Header/menu/footer terduplikasi ~698 halaman.
3. **Konten = HTML blob**, bukan data terstruktur. 60% CSS inline.
4. **URL campur (.html vs folder) dan sakral.** Jangan diubah tanpa 301.
5. **Volume: ~698 halaman** (194 artikel + 489 kota + 10 page + 5 desain).
6. **Media setengah rapuh:** 88 MB lokal + ratusan hotlink eksternal.
7. **Jebakan teknis:** tidak ada .nojekyll, tidak ada CI, tidak ada package.json.
