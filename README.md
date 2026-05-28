# Naltech Dev Docs

Project ini adalah dokumentasi pribadi berbasis Astro untuk menyimpan materi belajar, catatan kerja, snippet, dan dokumentasi teknis yang pernah dikerjakan.

Tujuan utamanya bukan hanya menyimpan materi Flutter, tetapi menjadi knowledge base pribadi yang mudah dibaca lagi saat dibutuhkan.

- Flutter
- Laravel
- React
- Database
- Deployment
- Troubleshooting
- Snippet kode
- Dokumentasi project

## Dokumentasi yang Sudah Ada

Saat ini dokumentasi dibagi menjadi beberapa kategori.

### Flutter

Materi Flutter sudah cukup lengkap dari dasar, state management, local storage, project, sampai Firebase.

| Urutan | Materi | Level |
| --- | --- | --- |
| 5 | Roadmap Belajar Flutter | Roadmap |
| 10 | Tutorial Flutter Dasar untuk Pemula | Beginner |
| 20 | Tutorial Flutter Lanjutan | Intermediate |
| 25 | Setup Project Flutter di Firebase Studio | Setup |
| 30 | Praktik Flutter per Bab | Practice |
| 35 | State Management Dasar | Foundation |
| 36 | CRUD Lokal, Filter, dan Search | Foundation |
| 37 | Provider untuk Pemula | State Management |
| 38 | Riverpod untuk Pemula | State Management |
| 39 | Cubit dan Bloc Dasar | State Management |
| 40 | Project 1: Aplikasi Catatan Belajar | Project |
| 50 | Project 2: Task Manager | Project |
| 55 | Local Storage Dasar | Storage |
| 56 | Shared Preferences untuk Pemula | Storage |
| 57 | Upgrade Task Manager dengan Local Storage | Project |
| 58 | Upgrade Task Manager dengan Provider dan Local Storage | Project |
| 59 | Upgrade Task Manager dengan Riverpod dan Local Storage | Project |
| 60 | Upgrade Task Manager dengan Cubit dan Local Storage | Project |
| 61 | Repository Pattern Sederhana | Architecture |
| 70 | Firebase Authentication untuk Pemula | Firebase |
| 71 | Cloud Firestore Dasar | Firebase |
| 72 | Firestore CRUD untuk Pemula | Firebase |
| 73 | Task Manager Online per User | Firebase |
| 74 | Firestore Security Rules Dasar | Firebase |

### AI Tools

Kategori AI Tools berisi catatan stack, workflow, automation, gateway, observability, evaluation, dan agent.

| Urutan | Materi | Level |
| --- | --- | --- |
| 60 | AI Tools Roadmap | Beginner |
| 70 | NalTech AI Stack | Intermediate |
| 80 | 9Router Proxy | Intermediate |
| 85 | OpenCode | Intermediate |
| 90 | OpenClaw | Intermediate |
| 95 | AI Agent Security | Intermediate |
| 100 | Cost Control AI | Intermediate |
| 105 | AI Automation | Intermediate |
| 110 | AI Gateway Comparison | Intermediate |
| 115 | Local AI Model Stack | Intermediate |
| 120 | Prompt Engineering untuk Agent | Intermediate |
| 125 | RAG dan Knowledge Base untuk AI Agent | Intermediate |
| 130 | AI Evaluation & Testing | Advanced |
| 135 | Langfuse Observability | Advanced |
| 140 | n8n + 9Router Workflow | Intermediate |
| 145 | Telegram dan Discord Automation | Intermediate |
| 150 | Hermes Agent | Intermediate |

## Struktur Utama

```text
src/
  content/
    docs/
      ai-tools/
        9router-proxy.md
        ai-tools-roadmap.md
        ...
      flutter/
        dasar.md
        lanjutan.md
        firestore-security-rules-dasar.md
        task-manager-online-per-user.md
        ...
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

Materi Flutter awal telah dipindahkan ke:

- `src/content/docs/flutter/dasar.md`
- `src/content/docs/flutter/lanjutan.md`

Dokumentasi sekarang sudah berkembang menjadi website docs berbasis Astro dengan kategori Flutter dan AI Tools. File HTML lama masih bisa dipakai sebagai arsip/versi statis bila masih tersedia di folder lama.
