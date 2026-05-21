# Personal Developer Docs

Project ini adalah migrasi awal dari tutorial HTML statis menjadi dokumentasi berbasis Astro.

Tujuan utamanya bukan hanya menyimpan materi Flutter, tetapi menjadi knowledge base pribadi untuk semua hal yang pernah dikerjakan:

- Flutter
- Laravel
- React
- Database
- Deployment
- Troubleshooting
- Snippet kode
- Dokumentasi project

## Struktur Utama

```text
src/
  content/
    docs/
      flutter/
        dasar.md
        lanjutan.md
  components/
    Sidebar.astro
  layouts/
    BaseLayout.astro
    DocsLayout.astro
  pages/
    index.astro
    docs/[...slug].astro
```

## Cara Menjalankan

Install dependency:

```bash
npm install
```

Jalankan development server:

```bash
npm run dev
```

Build static site:

```bash
npm run build
```

Preview hasil build:

```bash
npm run preview
```

## Menambah Materi Baru

Buat file Markdown baru di dalam `src/content/docs`.

Contoh:

```text
src/content/docs/laravel/auth-login.md
src/content/docs/database/mysql-join.md
src/content/docs/troubleshooting/flutter-build-error.md
```

Format frontmatter:

```md
---
title: "Laravel Auth Login"
description: "Catatan membuat login Laravel dengan role user dan admin."
category: "Laravel"
level: "Beginner"
order: 30
tags: ["laravel", "auth", "login"]
updated: "2026-05-20"
---

# Laravel Auth Login

Isi dokumentasi ditulis di sini.
```

## Rekomendasi Agar Mudah Dibaca User

Gunakan pola ini saat materi makin banyak:

1. Satu topik kecil menjadi satu file Markdown.
   Contoh: jangan gabungkan semua Laravel dalam satu file besar. Pisahkan menjadi `auth-login.md`, `middleware-role.md`, dan `api-resource.md`.

2. Pakai kategori yang konsisten.
   Contoh kategori awal:
   - `Flutter`
   - `Laravel`
   - `React`
   - `Database`
   - `Deployment`
   - `Troubleshooting`
   - `Snippet`
   - `Project Notes`

3. Pakai `order` untuk mengatur urutan baca.
   Materi dasar bisa `10`, lanjutan `20`, project `30`, dan seterusnya.

4. Isi `tags` dengan kata yang mungkin dicari lagi nanti.
   Contoh: `["flutter", "state", "provider", "error"]`.

5. Tulis setiap materi dengan format yang konsisten:
   - Masalah / tujuan
   - Penjelasan singkat
   - Langkah praktik
   - Contoh kode
   - Error umum
   - Checklist

6. Untuk dokumentasi pekerjaan nyata, simpan juga konteksnya:
   - Nama project
   - Tanggal
   - Masalah yang diselesaikan
   - Solusi
   - File yang diubah
   - Pelajaran yang bisa dipakai ulang

## Fitur UI yang Sudah Disiapkan

- Sidebar kategori dan materi.
- Submateri aktif muncul sebagai turunan di sidebar, mirip dokumentasi/course.
- Search dokumentasi di sidebar.
- Progress bar membaca.
- Mobile sidebar drawer.
- Tombol copy pada code block.
- Tombol next/previous materi.
- Tombol kembali ke atas.

## Catatan Migrasi

Materi Flutter yang sudah ada telah dipindahkan ke:

- `src/content/docs/flutter/dasar.md`
- `src/content/docs/flutter/lanjutan.md`

File HTML lama masih ada di folder `web/` sebagai arsip/versi statis.
