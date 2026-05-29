---
title: "Cost Control AI"
description: "Panduan mengontrol biaya dan token AI dengan 9Router, model routing, quota, prompt discipline, caching, summarization, dan audit usage."
category: "AI Tools"
level: "Intermediate"
order: 100
tags: ["ai", "cost-control", "token", "9router", "llm", "monitoring", "budget"]
updated: "2026-05-23"
---

# Cost Control AI

Cost control adalah strategi untuk mengatur penggunaan token dan biaya saat memakai AI tools seperti Codex, OpenCode, OpenClaw, dan 9Router.

AI agent bisa sangat membantu, tetapi biaya bisa naik cepat jika:

- context terlalu panjang
- agent membaca terlalu banyak file
- task tidak dibatasi
- model mahal dipakai untuk tugas ringan
- agent melakukan retry/fallback tanpa kontrol
- output terlalu panjang
- request berulang tidak diaudit

Prinsip utama:

```text
Gunakan model yang cukup kuat untuk tugasnya,
tetapi jangan selalu memakai model paling mahal.
```

## Konsep Dasar Token

### Input token

Input token adalah token yang dikirim ke model.

Contoh sumber input token:

- instruksi user
- system prompt
- isi file yang dibaca agent
- riwayat percakapan
- output tool sebelumnya
- log server
- dokumentasi
- data dari browser/API

Input token bisa membengkak jika agent membaca banyak file atau membawa context terlalu panjang.

### Output token

Output token adalah token yang dihasilkan model.

Contoh:

- jawaban
- rencana kerja
- kode
- dokumentasi
- ringkasan
- analisis error

Output token bisa membengkak jika prompt meminta jawaban sangat detail tanpa batas.

### Context window

Context window adalah kapasitas total token yang bisa diproses model dalam satu request.

Model dengan context besar berguna untuk codebase besar, tetapi biasanya lebih mahal atau lebih lambat.

Prinsip:

```text
Context besar bukan berarti harus selalu dipakai penuh.
```

## Kenapa Biaya AI Bisa Membengkak

Penyebab umum:

1. Agent membaca seluruh repository.
2. Agent mengirim ulang context yang sama berkali-kali.
3. Model kuat dipakai untuk task sederhana.
4. Task terlalu umum, sehingga agent eksplorasi terlalu luas.
5. Log panjang dikirim mentah tanpa diringkas.
6. Output diminta terlalu panjang.
7. Retry otomatis tanpa batas.
8. Fallback provider tidak dipantau.
9. Tidak ada budget limit.
10. Tidak ada audit request mahal.

Contoh prompt boros:

```text
Baca seluruh project ini dan jelaskan semuanya secara detail.
```

Prompt lebih hemat:

```text
Baca README, package.json, dan struktur folder level 2.
Jelaskan ringkasan project maksimal 30 bullet.
Jangan baca seluruh file source dulu.
```

## Peran 9Router dalam Cost Control

9Router menjadi titik pusat untuk memantau dan mengatur penggunaan model.

Fitur yang penting:

- usage analytics
- total request
- input token
- output token
- estimasi cost
- request log
- provider routing
- quota tracking
- combo/model routing

Dengan 9Router, semua tool bisa diarahkan ke satu endpoint:

```text
Codex / OpenCode / OpenClaw
  -> 9Router
  -> Provider AI
```

Manfaatnya:

- pemakaian semua tool terlihat di satu dashboard
- model bisa diganti dari satu tempat
- provider bisa difallback
- request mahal bisa dilacak
- quota lebih mudah dipantau

## Strategi Model Selection

Jangan gunakan satu model untuk semua tugas. Buat kategori.

### Model ringan

Cocok untuk:

- ringkasan pendek
- klasifikasi
- membuat checklist
- menjawab pertanyaan sederhana
- format ulang teks
- membuat draft awal

Contoh:

```text
Task ringan
  -> model murah/cepat
```

### Model menengah

Cocok untuk:

- debugging sederhana
- dokumentasi project
- membaca beberapa file
- membuat test sederhana
- review ringan

Contoh:

```text
Task development biasa
  -> model menengah
```

### Model kuat

Cocok untuk:

- reasoning kompleks
- refactor besar
- debugging sulit
- arsitektur sistem
- membaca context besar
- security review

Contoh:

```text
Task berat
  -> model kuat
```

## Routing Rule

Routing rule membantu memilih model berdasarkan jenis task.

Contoh rule:

| Jenis Task | Model yang Disarankan | Catatan |
|---|---|---|
| Ringkasan meeting | model ringan | output dibatasi |
| Dokumentasi pendek | model ringan/menengah | baca file spesifik |
| Explain codebase | model menengah | jangan baca semua file |
| Debugging error | model menengah/kuat | tergantung kompleksitas |
| Refactor besar | model kuat | wajib plan dulu |
| Security review | model kuat | scope harus jelas |
| Monitoring log | model ringan/menengah | ringkas log dulu |
| Prompt rewriting | model ringan | tidak perlu context besar |

Di 9Router, rule ini bisa diterjemahkan menjadi combo atau profil model.

Contoh combo:

```text
coding-light
  -> model murah/cepat

coding-heavy
  -> model kuat/context besar

summary
  -> model murah

security-review
  -> model kuat
```

## Prompt Discipline

Prompt yang baik bisa menghemat token.

### Batasi scope

Prompt boros:

```text
Cek semua file dan jelaskan semuanya.
```

Prompt hemat:

```text
Cek README, package.json, dan src/routes saja.
Jelaskan alur utama maksimal 20 bullet.
```

### Batasi output

Prompt boros:

```text
Jelaskan sedetail mungkin.
```

Prompt hemat:

```text
Jawab maksimal 30 bullet.
Prioritaskan hal yang penting untuk developer baru.
```

### Minta rencana dulu

Untuk task besar:

```text
Buat rencana dulu.
Jangan edit file.
Jangan baca seluruh repo.
Sebutkan file apa yang perlu dibaca dan alasannya.
```

### Gunakan file spesifik

Lebih hemat:

```text
Fokus pada file:
- src/routes/api.ts
- src/controllers/user.ts
- src/models/user.ts
```

Daripada:

```text
Baca seluruh folder src.
```

## Summarization Strategy

Untuk data panjang seperti log, issue, atau dokumen, jangan langsung kirim semuanya ke model kuat.

Gunakan tahap ringkas:

```text
Data panjang
  -> model ringan membuat ringkasan
  -> model kuat membaca ringkasan
  -> model kuat membuat keputusan
```

Contoh:

```text
1. Ambil 300 baris log terakhir.
2. Ringkas error unik.
3. Kirim hanya ringkasan ke model kuat.
4. Minta rekomendasi perbaikan.
```

Prompt:

```text
Ringkas log ini menjadi:
- error unik
- jumlah kemunculan
- endpoint terkait
- waktu kejadian
- contoh 1 baris log

Jangan analisis dulu.
```

Lalu:

```text
Berdasarkan ringkasan error ini, jelaskan kemungkinan penyebab dan prioritas perbaikan.
```

## Caching Response

Caching membantu menghindari request berulang.

Cocok untuk:

- dokumentasi dependency
- ringkasan struktur project
- daftar endpoint
- penjelasan arsitektur
- hasil audit awal

Strategi:

- simpan ringkasan project di `docs/`
- simpan mapping file penting
- simpan hasil research
- update cache hanya jika file terkait berubah

Contoh file cache:

```text
docs/ai-context/project-overview.md
docs/ai-context/api-routes.md
docs/ai-context/database-schema.md
```

Prompt:

```text
Sebelum membaca banyak file, cek apakah ada docs/ai-context/project-overview.md.
Jika ada, gunakan itu sebagai konteks awal.
```

## Audit Request Mahal

Di dashboard 9Router, perhatikan:

- request dengan input token tinggi
- request dengan output token tinggi
- model mahal yang sering dipakai
- retry berulang
- request gagal yang tetap memakan token
- client yang paling banyak memakai token

Pertanyaan audit:

```text
1. Task apa yang paling mahal?
2. Apakah task itu perlu model kuat?
3. Apakah context terlalu panjang?
4. Apakah output terlalu panjang?
5. Apakah agent membaca file terlalu banyak?
6. Apakah bisa dibuat ringkasan/cache?
7. Apakah perlu routing rule baru?
```

## Limit dan Quota

Atur limit agar biaya tidak lolos tanpa kontrol.

Rekomendasi:

- limit harian per provider
- limit mingguan per project
- limit output token untuk task ringan
- limit context untuk agent tertentu
- alert jika token naik tidak normal
- pause provider mahal jika melewati budget

Contoh policy:

```text
Task ringan:
  output maksimal 1500 token

Task dokumentasi:
  output maksimal 4000 token

Task refactor besar:
  wajib approval sebelum memakai model kuat

Security review:
  boleh model kuat, tetapi scope file harus jelas
```

## Cost Control untuk OpenCode

OpenCode sering membaca codebase dan menjalankan task coding. Ini bisa boros jika scope tidak jelas.

Praktik hemat:

- gunakan `/init` agar project punya `AGENTS.md`
- minta plan sebelum build
- sebutkan file/folder yang relevan
- jangan minta scan seluruh repo
- gunakan `small_model` untuk task ringan
- gunakan 9Router analytics untuk memantau request

Contoh prompt hemat:

```text
Fokus hanya pada src/pages/tasks dan src/lib/tasks.
Buat rencana fitur search.
Jangan baca folder lain kecuali perlu, dan jelaskan alasannya.
Jangan edit file dulu.
```

## Cost Control untuk OpenClaw

OpenClaw bisa mengakses banyak tool. Cost bisa naik jika agent eksplorasi terlalu luas.

Praktik hemat:

- batasi tool yang aktif
- batasi folder workspace
- ringkas data panjang sebelum reasoning
- jangan auto-retry tanpa batas
- gunakan model ringan untuk ringkasan
- gunakan model kuat hanya untuk keputusan
- simpan hasil research ke file

Prompt policy:

```text
Sebelum membaca banyak file atau data panjang, buat rencana.
Jika data terlalu panjang, ringkas dulu dengan model ringan.
Jangan mengirim seluruh log atau seluruh folder ke model jika tidak perlu.
```

## Cost Control untuk Codex

Untuk coding agent di repository:

- mulai dari file spesifik
- jelaskan scope perubahan
- minta rencana untuk perubahan besar
- hindari refactor tidak perlu
- jalankan test yang relevan, bukan seluruh suite jika tidak perlu
- simpan keputusan teknis di dokumentasi agar tidak diulang

Prompt:

```text
Perbaiki bug ini dengan scope minimal.
Fokus pada file yang relevan saja.
Jangan lakukan refactor unrelated.
Setelah selesai, jalankan test yang paling relevan.
```

## Fallback Provider

Fallback berguna saat provider error, tetapi bisa membuat biaya tidak terduga jika fallback memakai model lebih mahal.

Aturan:

- fallback harus punya urutan jelas
- fallback mahal butuh approval untuk task tertentu
- log fallback harus dipantau
- jangan fallback ke model kuat untuk task ringan tanpa alasan

Contoh:

```text
summary:
  provider murah A
  -> provider murah B
  -> stop

coding-heavy:
  provider kuat A
  -> provider kuat B
  -> minta approval jika gagal
```

## Template Policy Hemat Token

Masukkan ke `AGENTS.md`, `TOOLS.md`, atau instruksi agent:

```md
# Token and Cost Policy

Gunakan token secara hemat.

## Aturan

- Jangan membaca seluruh repository jika task hanya butuh beberapa file.
- Buat rencana sebelum membaca banyak file.
- Batasi output sesuai kebutuhan.
- Untuk data panjang, buat ringkasan dulu.
- Gunakan model ringan untuk ringkasan dan task sederhana.
- Gunakan model kuat hanya untuk reasoning berat.
- Jangan melakukan retry berulang tanpa alasan.
- Simpan ringkasan project agar bisa dipakai ulang.

## Wajib Konfirmasi

- memakai model kuat untuk task besar
- membaca folder besar
- menganalisis log sangat panjang
- menjalankan task multi-step yang lama
- melakukan retry lebih dari 2 kali
```

## Template Prompt Hemat Token

```text
Kerjakan dengan hemat token.
Fokus hanya pada file/folder yang relevan.
Jangan baca seluruh repo.
Jika butuh membaca file tambahan, jelaskan alasannya dulu.
Jawab maksimal 25 bullet.
Jangan menulis ulang isi file panjang kecuali diminta.
```

Untuk debugging:

```text
Analisis error ini.
Fokus pada stack trace dan file yang disebut.
Jangan scan seluruh project.
Buat 3 hipotesis paling mungkin dan langkah verifikasi.
```

Untuk dokumentasi:

```text
Buat dokumentasi ringkas.
Gunakan README dan file config utama.
Jika informasi belum jelas, beri label "perlu dikonfirmasi".
Jangan baca source code detail kecuali diperlukan.
```

## Dashboard Mingguan

Setiap minggu, cek:

- total request
- total input token
- total output token
- top 5 model paling sering dipakai
- top 5 request paling mahal
- provider yang sering error
- client yang paling boros
- task yang bisa dipindah ke model murah
- kebutuhan routing rule baru

Template laporan:

```text
AI Usage Weekly Report

Periode:

Total request:
Total input token:
Total output token:
Estimasi biaya:

Model paling sering dipakai:
1.
2.
3.

Request paling mahal:
1.
2.
3.

Masalah:
- provider error:
- token spike:
- retry berulang:

Rekomendasi:
- routing rule:
- model yang perlu diganti:
- prompt yang perlu diperbaiki:
```

## Checklist Cost Control

- [ ] Semua tool AI memakai 9Router jika memungkinkan.
- [ ] Dashboard usage dicek rutin.
- [ ] Model ringan tersedia untuk task sederhana.
- [ ] Model kuat hanya untuk task berat.
- [ ] Prompt agent membatasi scope.
- [ ] Output token dibatasi.
- [ ] Log panjang diringkas dulu.
- [ ] Request mahal diaudit.
- [ ] Fallback provider punya aturan jelas.
- [ ] Budget harian/mingguan ditentukan.
- [ ] Ringkasan project disimpan agar tidak dibaca ulang.
- [ ] Policy hemat token masuk ke `AGENTS.md` atau `TOOLS.md`.

## Kesimpulan

Cost control bukan berarti mengurangi kualitas kerja AI. Cost control berarti memilih model, context, dan workflow yang sesuai dengan tingkat kesulitan tugas.

Pola terbaik:

```text
Task ringan
  -> model ringan

Task panjang
  -> ringkas dulu

Task berat
  -> model kuat dengan scope jelas

Semua usage
  -> pantau lewat 9Router
```

Dengan 9Router sebagai pusat monitoring dan agent policy yang jelas, penggunaan AI bisa tetap produktif tanpa biaya yang liar.

