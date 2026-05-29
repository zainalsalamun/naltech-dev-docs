# Fitaru Admin CMS Design

Dokumen ini menjelaskan konsep dashboard web admin untuk mengelola aplikasi Fitaru.

## Tujuan Admin CMS

Admin CMS Fitaru digunakan oleh tim internal untuk mengelola konten, memantau aktivitas user, dan mengatur data pendukung aplikasi.

CMS ini bukan untuk user umum. CMS dipakai oleh:

- Founder atau owner produk
- Admin operasional
- Content manager
- Nutrition/health content reviewer
- Customer support

## Fungsi Utama

Admin CMS harus membantu tim untuk:

- Melihat ringkasan performa aplikasi
- Mengelola konten tips
- Mengelola database makanan
- Mengelola daftar olahraga
- Memantau user
- Mengirim notifikasi
- Melihat feedback user
- Mengatur konfigurasi aplikasi

## Modul MVP Admin CMS

### 1. Overview Dashboard

Ringkasan utama:

- Total user
- Active user hari ini
- Makanan tercatat hari ini
- Olahraga tercatat hari ini
- Konten tips aktif
- Feedback baru

Widget:

- User growth chart
- Daily activity chart
- Top logged foods
- Recent user feedback
- Quick actions

### 2. User Management

Fitur:

- Melihat daftar user
- Search user
- Filter berdasarkan status
- Melihat detail user
- Melihat aktivitas ringkas user
- Suspend atau reactivate user bila diperlukan

Data user:

- Nama
- Email atau nomor HP
- Tanggal daftar
- Tujuan diet
- Status akun
- Aktivitas terakhir

### 3. Content Management

Digunakan untuk mengelola artikel tips.

Fitur:

- Buat artikel
- Edit artikel
- Draft / publish / archive
- Kategori artikel
- Upload thumbnail
- Preview artikel

Kategori:

- Makan santai
- Olahraga pemula
- Kurangi gula
- Meal prep
- Tidur dan recovery

Data artikel:

- Judul
- Slug
- Kategori
- Ringkasan
- Konten
- Thumbnail
- Status
- Author
- Publish date

### 4. Food Database

Digunakan untuk mengelola referensi makanan.

Fitur:

- Tambah makanan
- Edit makanan
- Kategori makanan
- Estimasi kalori
- Porsi default
- Status aktif/nonaktif

Data makanan:

- Nama makanan
- Kategori
- Estimasi kalori per porsi
- Porsi
- Protein opsional
- Karbo opsional
- Lemak opsional
- Catatan

Untuk MVP, macro detail bisa opsional.

### 5. Exercise Database

Digunakan untuk mengelola referensi olahraga.

Fitur:

- Tambah olahraga
- Edit olahraga
- Kategori olahraga
- Estimasi kalori per durasi
- Intensitas
- Status aktif/nonaktif

Data olahraga:

- Nama olahraga
- Kategori
- Intensitas
- Estimasi kalori
- Durasi default
- Catatan

### 6. Notification Center

Digunakan untuk mengirim notifikasi ke user.

Fitur:

- Buat push notification
- Pilih target user
- Jadwalkan notifikasi
- Kirim langsung
- Lihat riwayat campaign

Target:

- Semua user
- User aktif
- User tidak aktif 7 hari
- User dengan target turun berat badan
- User yang belum mencatat makan hari ini

Data notifikasi:

- Judul
- Pesan
- Target segment
- Jadwal kirim
- Status
- Statistik terkirim/dibuka

### 7. Feedback & Support

Digunakan untuk melihat masukan user.

Fitur:

- Daftar feedback
- Filter status
- Tandai sebagai open, reviewed, resolved
- Catatan admin

Data feedback:

- User
- Tipe feedback
- Pesan
- Tanggal
- Status
- Admin note

### 8. App Settings

Digunakan untuk konfigurasi dasar aplikasi.

Fitur:

- Target default air minum
- Target default olahraga
- Jadwal reminder default
- Kategori tips
- Kategori makanan
- Kategori olahraga
- Maintenance banner

## Navigasi Admin CMS

Sidebar navigation:

- Overview
- Users
- Content
- Food Database
- Exercise Database
- Notifications
- Feedback
- Settings

## Role Admin

Untuk MVP, role bisa sederhana:

### Super Admin

Bisa mengakses semua fitur.

### Content Admin

Bisa mengelola artikel tips.

### Support Admin

Bisa melihat user dan feedback, tapi tidak bisa mengubah konfigurasi aplikasi.

## Overview Dashboard Layout

```text
┌──────────────────────────────────────────────────────┐
│ Sidebar        Header: Search, Admin Profile         │
├───────────────┬──────────────────────────────────────┤
│ Overview      │ Stat Cards                           │
│ Users         │ [Users] [Active] [Meals] [Exercise]  │
│ Content       │                                      │
│ Food DB       │ User Growth Chart   Activity Chart   │
│ Exercise DB   │                                      │
│ Notifications │ Top Foods          Recent Feedback   │
│ Feedback      │                                      │
│ Settings      │ Quick Actions                        │
└───────────────┴──────────────────────────────────────┘
```

## Prioritas MVP Admin CMS

Urutan modul yang sebaiknya dibuat:

1. Login admin
2. Overview dashboard
3. Content management
4. Food database
5. Exercise database
6. User list
7. Notification center
8. Feedback
9. Settings

## Data Penting untuk Overview

Metric awal:

- `totalUsers`
- `activeUsersToday`
- `newUsersThisWeek`
- `mealsLoggedToday`
- `exerciseLoggedToday`
- `publishedTips`
- `pendingFeedback`

Chart awal:

- User growth 7 hari
- Activity logs 7 hari
- Top foods minggu ini
- Top exercises minggu ini

## Tone UI Admin

Berbeda dari aplikasi mobile yang lebih emosional dan suportif, CMS harus terasa:

- Rapi
- Efisien
- Mudah dipindai
- Profesional
- Tidak terlalu dekoratif
- Tetap memakai identitas warna Fitaru

## Design Direction

Warna:

- Primary: Fitaru Teal
- Sidebar: deep teal atau white
- Background: off-white atau light gray
- Card: white
- Accent: coral dan amber untuk status ringan

Komponen:

- Sidebar
- Topbar
- Stat card
- Data table
- Filter bar
- Search input
- Status badge
- Chart card
- Modal form
- Drawer detail

## Success Criteria

CMS MVP dianggap berhasil bila admin bisa:

- Melihat kondisi aplikasi dalam satu layar
- Membuat dan publish artikel tips
- Menambah makanan dan olahraga referensi
- Melihat user aktif
- Mengirim notifikasi sederhana
- Membaca feedback user

## Tahap Berikutnya

Tahap berikutnya:

1. Membuat mockup UI admin dashboard web
2. Membuat wireframe halaman content management
3. Membuat struktur database admin
4. Menentukan role dan permission
5. Menentukan tech stack admin panel
