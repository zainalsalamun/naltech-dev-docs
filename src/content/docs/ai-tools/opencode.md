---
title: "OpenCode"
description: "Panduan memahami OpenCode sebagai open-source AI coding agent, instalasi, konfigurasi provider, integrasi 9Router, workflow coding, permission, dan troubleshooting."
category: "AI Tools"
level: "Intermediate"
order: 85
tags: ["ai", "coding-agent", "opencode", "terminal", "9router", "developer-tools"]
updated: "2026-05-23"
---

# OpenCode

OpenCode adalah **open-source AI coding agent** yang bisa berjalan di terminal, desktop app, atau IDE extension. Fokus utamanya adalah membantu developer bekerja di codebase: membaca file, memahami struktur project, membuat rencana, mengedit kode, menjalankan command, dan memvalidasi hasil.

Jika OpenClaw lebih luas sebagai personal AI agent dan automation runtime, OpenCode lebih spesifik untuk **coding workflow**.

```text
OpenCode = coding agent
OpenClaw = personal/automation agent
9Router = AI gateway/model router
```

## Fungsi OpenCode

OpenCode membantu developer melakukan pekerjaan seperti:

- memahami codebase
- menjelaskan file atau fungsi tertentu
- membuat fitur baru
- memperbaiki bug
- refactor kode
- membuat test
- menjalankan test/lint/build
- membuat dokumentasi project
- membuat rencana perubahan sebelum eksekusi
- bekerja dengan provider AI yang berbeda

OpenCode cocok untuk developer yang sering bekerja dari terminal dan ingin agent coding yang bisa dikontrol langsung dari project.

## Cara Kerja OpenCode

Alur kerja dasarnya:

```text
Developer membuka project
  -> menjalankan opencode
  -> memberi instruksi
  -> OpenCode membaca konteks project
  -> OpenCode meminta reasoning ke model AI
  -> OpenCode memakai tool: baca file, edit file, run command
  -> developer review hasil
```

Jika memakai 9Router:

```text
Developer
  -> OpenCode
  -> 9Router
  -> Provider AI
  -> 9Router
  -> OpenCode menjalankan aksi coding
```

## OpenCode vs Tool Lain

| Tool | Fokus | Cocok Untuk |
|---|---|---|
| OpenCode | coding agent open-source | coding terminal, project lokal, model custom |
| Codex | coding agent di workspace | edit repo, test, refactor, debugging |
| Claude Code | coding agent berbasis Claude | coding dengan Claude, reasoning code |
| OpenClaw | personal AI agent | automation, browser, chat app, workflow luas |
| 9Router | AI gateway | routing model, analytics, quota, fallback |
| n8n | automation visual | workflow trigger/API yang deterministik |

Gunakan OpenCode jika tujuan utamanya adalah bekerja di codebase. Gunakan OpenClaw jika tugasnya lintas aplikasi atau automation 24/7. Gunakan 9Router jika ingin mengatur model dan provider dari satu tempat.

## Instalasi OpenCode

### 1. Prasyarat

Untuk terminal, OpenCode lebih nyaman dipakai dengan terminal modern seperti WezTerm, Alacritty, Ghostty, atau Kitty.

Yang dibutuhkan:

- terminal modern
- akses shell
- API key provider AI, atau endpoint AI gateway seperti 9Router
- Node.js jika ingin install via npm/pnpm/yarn

### 2. Install dengan script resmi

Cara paling mudah:

```bash
curl -fsSL https://opencode.ai/install | bash
```

Cek hasil install:

```bash
opencode --version
```

### 3. Install via npm

Alternatif:

```bash
npm install -g opencode-ai
```

Via pnpm:

```bash
pnpm install -g opencode-ai
```

Via bun:

```bash
bun install -g opencode-ai
```

### 4. Install via Homebrew

Untuk macOS atau Linux:

```bash
brew install anomalyco/tap/opencode
```

### 5. Windows

Untuk Windows, jalur paling disarankan adalah WSL.

Alternatif:

```powershell
choco install opencode
```

Atau:

```powershell
scoop install opencode
```

## Menjalankan OpenCode Pertama Kali

Masuk ke folder project:

```bash
cd /path/to/project
```

Jalankan:

```bash
opencode
```

Di dalam TUI OpenCode, jalankan:

```text
/init
```

Command `/init` akan membuat OpenCode menganalisis project dan membuat file `AGENTS.md` di root project.

File `AGENTS.md` sebaiknya ikut dicommit ke Git karena berisi panduan agar agent memahami struktur, style, dan aturan project.

## Command Penting di TUI

| Command | Fungsi |
|---|---|
| `/connect` | menghubungkan provider/model |
| `/models` | memilih model |
| `/init` | membuat `AGENTS.md` untuk project |
| `/undo` | membatalkan perubahan dari session |
| `/redo` | menjalankan ulang perubahan yang dibatalkan |
| `/share` | membuat link session jika ingin dibagikan |

Catatan:

- Gunakan `/models` setelah provider tersambung.
- Gunakan `/undo` jika hasil perubahan tidak sesuai.
- Gunakan plan mode sebelum build mode untuk perubahan besar.

## Plan Mode dan Build Mode

OpenCode punya pola kerja yang bagus untuk mengurangi risiko:

```text
Plan mode
  -> OpenCode membaca konteks dan membuat rencana
  -> tidak langsung mengubah file

Build mode
  -> OpenCode mengeksekusi rencana
  -> bisa mengubah file dan menjalankan command
```

Workflow aman:

```text
1. Minta OpenCode membuat rencana.
2. Review rencana.
3. Beri koreksi jika perlu.
4. Baru izinkan OpenCode build.
5. Jalankan test.
6. Review diff.
```

Contoh prompt:

```text
Tolong buat rencana untuk menambahkan fitur search di halaman task.
Jangan edit file dulu.
Jelaskan file mana yang perlu diubah dan risiko perubahannya.
```

Jika rencana sudah oke:

```text
Rencananya sudah oke. Silakan implementasikan.
Setelah selesai, jalankan test yang relevan.
```

## Konfigurasi OpenCode

OpenCode memiliki beberapa level konfigurasi.

Urutan penting:

```text
Remote config organisasi
  -> global config
  -> custom config via env
  -> project config
  -> .opencode directories
  -> inline config via env
```

Lokasi global config:

```text
~/.config/opencode/opencode.json
```

Lokasi TUI config:

```text
~/.config/opencode/tui.json
```

Project config:

```text
opencode.json
```

Direktori project:

```text
.opencode/
  agents/
  commands/
  modes/
  plugins/
  skills/
  tools/
  themes/
```

## Konfigurasi Provider

OpenCode mendukung banyak provider melalui Models.dev dan AI SDK. Provider bisa dihubungkan lewat `/connect`, lalu model dipilih lewat `/models`.

Contoh memakai provider umum:

```text
/connect
-> pilih provider
-> masukkan API key
-> /models
-> pilih model
```

Provider yang umum:

- OpenAI
- Anthropic
- Gemini
- GitHub Copilot
- OpenRouter
- Ollama
- LM Studio
- provider OpenAI-compatible
- 9Router sebagai custom provider

## Integrasi OpenCode dengan 9Router

9Router bisa dipakai sebagai endpoint OpenAI-compatible untuk OpenCode.

Manfaat:

- satu endpoint untuk banyak provider
- routing model dari dashboard 9Router
- analytics token
- quota tracking
- fallback provider
- cost control

### 1. Siapkan 9Router

Pastikan 9Router berjalan.

Jika lokal:

```text
http://localhost:20128/v1
```

Jika di VPS:

```text
https://9router.domainkamu.com/v1
```

### 2. Simpan API key

Tambahkan ke shell profile:

```bash
export NINE_ROUTER_API_KEY="isi_api_key_9router"
```

Reload:

```bash
source ~/.zshrc
```

### 3. Tambahkan custom provider di `opencode.json`

Contoh global config:

```text
~/.config/opencode/opencode.json
```

Isi:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "9router": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "9Router",
      "options": {
        "baseURL": "https://9router.domainkamu.com/v1",
        "apiKey": "{env:NINE_ROUTER_API_KEY}"
      },
      "models": {
        "mimo-v2.5-pro": {
          "name": "MiMo v2.5 Pro via 9Router",
          "limit": {
            "context": 200000,
            "output": 8192
          }
        }
      }
    }
  },
  "model": "9router/mimo-v2.5-pro",
  "small_model": "9router/mimo-v2.5-pro"
}
```

Sesuaikan:

- `baseURL` dengan endpoint 9Router kamu.
- `mimo-v2.5-pro` dengan model/combo yang tersedia di 9Router.
- `context` dan `output` dengan kemampuan model yang dipakai.

### 4. Pilih model di OpenCode

Jalankan:

```bash
opencode
```

Di TUI:

```text
/models
```

Pilih model dari provider `9Router`.

### 5. Verifikasi di dashboard 9Router

Setelah mengirim prompt dari OpenCode, cek dashboard 9Router:

- request masuk atau tidak
- model yang dipakai
- input token
- output token
- error provider jika ada

## Permission dan Keamanan

Secara default, OpenCode bisa melakukan banyak operasi. Untuk belajar dan project penting, atur permission agar edit dan command perlu approval.

Contoh `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "permission": {
    "edit": "ask",
    "bash": "ask"
  }
}
```

Aturan aman:

- Gunakan Plan mode untuk perubahan besar.
- Jangan izinkan command destruktif.
- Review diff sebelum commit.
- Jangan menyimpan API key di repo.
- Gunakan project config untuk aturan spesifik project.
- Batasi provider dengan `enabled_providers` jika perlu.
- Gunakan `small_model` untuk task ringan agar hemat biaya.

## AGENTS.md untuk OpenCode

`AGENTS.md` membantu OpenCode memahami project.

Template:

```md
# Project Agent Instructions

Kamu adalah coding agent untuk project ini.

## Prinsip

- Baca konteks sebelum mengubah file.
- Untuk perubahan besar, buat rencana dulu.
- Ikuti pola kode yang sudah ada.
- Jangan menambahkan dependency tanpa alasan.
- Jangan menulis secret/API key ke file.
- Jalankan test yang relevan setelah perubahan.

## Command

- Install: `npm install`
- Dev: `npm run dev`
- Build: `npm run build`
- Test: `npm test`

## Batasan

- Jangan deploy production.
- Jangan hapus file tanpa izin.
- Jangan commit atau push tanpa instruksi.
- Jangan mengubah konfigurasi environment tanpa konfirmasi.
```

Sesuaikan command dengan project masing-masing.

## Workflow Coding yang Disarankan

### 1. Memahami project

Prompt:

```text
Baca project ini dan jelaskan:
1. tujuan project
2. stack teknologi
3. struktur folder utama
4. command development
5. file konfigurasi penting

Jangan edit file.
```

### 2. Membuat rencana fitur

```text
Saya ingin menambahkan fitur search task.
Buat rencana implementasi dulu.
Jangan edit file.
Jelaskan file yang akan diubah dan potensi risiko.
```

### 3. Implementasi fitur

```text
Rencana sudah oke.
Silakan implementasikan fitur search task.
Setelah selesai, jalankan test/build yang relevan.
```

### 4. Review hasil

```text
Jelaskan perubahan yang kamu buat.
Tunjukkan file yang berubah, alasan perubahan, dan cara mengetesnya.
```

### 5. Dokumentasi

```text
Tambahkan catatan penggunaan fitur search ke dokumentasi.
Jangan ubah bagian lain yang tidak terkait.
```

## Prompt Siap Pakai

### Explain codebase

```text
Jelaskan codebase ini seperti onboarding developer baru.
Fokus pada struktur folder, alur utama aplikasi, dan command penting.
Jangan mengubah file.
```

### Cari bug

```text
Cari kemungkinan penyebab bug berikut:

[paste bug/error]

Baca file yang relevan, jelaskan hipotesis, dan buat rencana perbaikan.
Jangan edit file dulu.
```

### Refactor aman

```text
Refactor bagian ini agar lebih mudah dibaca tanpa mengubah behavior.
Buat rencana dulu, lalu tunggu konfirmasi sebelum edit.
```

### Tambah test

```text
Tambahkan test untuk behavior berikut:

[jelaskan behavior]

Ikuti pola test yang sudah ada.
Jalankan test yang relevan setelah selesai.
```

### Buat dokumentasi

```text
Buat dokumentasi setup project untuk developer baru.
Jangan menulis secret.
Jika ada env variable yang belum jelas, beri label "perlu dikonfirmasi".
```

## Use Case OpenCode di NalTech AI Stack

### Coding lokal

```text
Developer
  -> OpenCode lokal
  -> 9Router VPS
  -> provider AI
```

Use case:

- membuat fitur Flutter
- memperbaiki bug Laravel
- refactor React component
- membuat dokumentasi project
- menjalankan test/build

### Pairing dengan Codex

OpenCode bisa dipakai bersama Codex:

```text
Codex
  -> perubahan utama di repo

OpenCode
  -> eksplorasi alternatif
  -> review ringan
  -> eksperimen prompt/model
```

Aturan:

- jangan menjalankan dua agent untuk mengedit file yang sama secara bersamaan
- selalu cek `git diff`
- pisahkan branch jika eksperimen besar

### Pairing dengan OpenClaw

```text
OpenCode
  -> coding di project

OpenClaw
  -> dokumentasi, research, automation, browser
```

Contoh:

```text
OpenCode membuat fitur.
OpenClaw membuat ringkasan perubahan dan draft changelog.
9Router memantau token keduanya.
```

## Troubleshooting

### `opencode` tidak ditemukan

Cek install:

```bash
which opencode
opencode --version
```

Jika install via npm:

```bash
npm prefix -g
echo $PATH
```

### Provider tidak muncul

Cek:

- API key sudah ditambahkan lewat `/connect`
- `opencode.json` valid JSON
- provider ID di `/connect` sama dengan config
- model tersedia di bagian `models`
- jalankan ulang OpenCode

### 9Router tidak menerima request

Cek:

- `baseURL` harus memakai `/v1`
- API key benar
- model/combo ada di 9Router
- 9Router berjalan
- dashboard 9Router tidak menunjukkan provider error

Test endpoint:

```bash
curl https://9router.domainkamu.com/v1/models \
  -H "Authorization: Bearer $NINE_ROUTER_API_KEY"
```

### OpenCode mengubah terlalu banyak file

Langkah aman:

```text
/undo
```

Lalu ulang dengan prompt lebih spesifik:

```text
Ubah hanya file X dan Y.
Jangan refactor bagian lain.
Jangan format seluruh project.
```

### Token terlalu boros

Solusi:

- pakai `small_model` untuk task ringan
- minta OpenCode membaca file spesifik dengan `@file`
- jangan minta scan seluruh repo jika tidak perlu
- gunakan 9Router analytics untuk melihat request besar
- pecah task besar menjadi beberapa langkah

## Checklist Belajar OpenCode

- Install OpenCode.
- Jalankan `opencode --version`.
- Buka project kecil.
- Jalankan `/init`.
- Baca `AGENTS.md`.
- Hubungkan provider dengan `/connect`.
- Pilih model dengan `/models`.
- Coba prompt explain project.
- Coba plan mode untuk fitur kecil.
- Coba build mode setelah review rencana.
- Jalankan test/build.
- Cek diff.
- Cek usage di 9Router jika memakai 9Router.

## Kesimpulan

OpenCode adalah pilihan yang bagus untuk coding agent open-source yang berjalan dekat dengan workflow developer. Ia cocok untuk terminal, project lokal, dan eksperimen dengan berbagai model/provider.

Dalam NalTech AI Stack:

```text
OpenCode
  -> membantu coding

9Router
  -> mengatur model dan biaya

OpenClaw
  -> automation dan workflow non-coding

Codex
  -> coding agent utama di workspace
```

Pola paling aman:

```text
Mulai dari explain project
  -> minta rencana
  -> review rencana
  -> izinkan build
  -> jalankan test
  -> review diff
```

Dengan pola ini, OpenCode bisa dipakai produktif tanpa kehilangan kontrol terhadap codebase.

## Referensi

- [OpenCode official site](https://opencode.ai/)
- [OpenCode docs](https://dev.opencode.ai/docs/)
- [OpenCode providers](https://dev.opencode.ai/docs/providers/)
- [OpenCode config](https://dev.opencode.ai/docs/config/)
- [OpenCode GitHub](https://github.com/sst/opencode)

