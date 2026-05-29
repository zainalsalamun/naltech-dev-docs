---
title: "NalTech AI Stack"
description: "Arsitektur AI stack untuk menggabungkan coding agent, OpenClaw, 9Router, VPS automation, provider AI, monitoring, keamanan, dan cost control."
category: "AI Tools"
level: "Intermediate"
order: 70
tags: ["ai", "architecture", "agent", "gateway", "9router", "openclaw", "vps"]
updated: "2026-05-23"
---

# NalTech AI Stack

NalTech AI Stack adalah rancangan arsitektur untuk memakai banyak tool AI secara rapi, aman, dan bisa dikembangkan.

Tujuannya bukan hanya memakai AI untuk chat, tetapi membuat ekosistem kerja:

- coding agent untuk membantu development
- AI gateway untuk mengatur provider/model
- agent automation untuk task 24/7
- dashboard untuk monitoring token dan biaya
- permission policy agar agent tidak terlalu bebas
- workflow belajar yang bisa naik ke produksi ringan

## Gambaran Besar

Arsitektur dasar:

```text
Developer
  -> Codex / OpenCode / OpenClaw lokal
  -> 9Router
  -> Provider AI
```

Arsitektur lengkap:

```text
Laptop Developer
  -> Codex untuk coding di repo
  -> OpenCode untuk coding terminal/open-source workflow
  -> OpenClaw lokal untuk file, browser, dan automation personal

VPS AI Gateway
  -> 9Router
  -> routing model
  -> fallback provider
  -> quota tracking
  -> usage analytics

VPS Automation
  -> OpenClaw server
  -> Telegram/Discord/GitHub webhook
  -> monitoring server
  -> laporan rutin

Provider AI
  -> OpenAI / Anthropic / Gemini / MiMo / local model / provider lain
```

## Komponen Utama

Materi detail:

- [AI Tools Roadmap](/docs/ai-tools/ai-tools-roadmap/)
- [9Router Proxy](/docs/ai-tools/9router-proxy/)
- [OpenClaw](/docs/ai-tools/openclaw/)
- [OpenCode](/docs/ai-tools/opencode/)
- [AI Agent Security](/docs/ai-tools/ai-agent-security/)
- [Cost Control AI](/docs/ai-tools/cost-control-ai/)
- [AI Automation](/docs/ai-tools/ai-automation/)
- [AI Gateway Comparison](/docs/ai-tools/ai-gateway-comparison/)
- [Local AI Model Stack](/docs/ai-tools/local-ai-model-stack/)
- [Prompt Engineering untuk Agent](/docs/ai-tools/prompt-engineering-agent/)
- [RAG dan Knowledge Base untuk AI Agent](/docs/ai-tools/rag-knowledge-base-agent/)
- [AI Evaluation & Testing](/docs/ai-tools/ai-evaluation-testing/)
- [Langfuse Observability](/docs/ai-tools/langfuse-observability/)
- [n8n + 9Router Workflow](/docs/ai-tools/n8n-9router-workflow/)
- [Telegram dan Discord Automation](/docs/ai-tools/telegram-discord-automation/)
- [Hermes Agent](/docs/ai-tools/hermes-agent/)

### 1. Codex

Codex dipakai sebagai coding agent di workspace/repository.

Cocok untuk:

- membaca codebase
- membuat perubahan file
- menjalankan test
- debugging
- membuat dokumentasi
- review perubahan
- bekerja langsung di repo

Peran dalam stack:

```text
Codex = agent coding utama untuk kerja di project
```

### 2. OpenCode

OpenCode bisa dipakai sebagai alternatif atau pelengkap coding agent.

Cocok untuk:

- workflow coding berbasis terminal
- eksperimen coding agent open-source
- memakai endpoint model custom
- integrasi dengan provider melalui 9Router

Peran dalam stack:

```text
OpenCode = coding agent alternatif yang bisa diarahkan ke 9Router
```

### 3. OpenClaw

OpenClaw dipakai sebagai agent yang lebih luas dari coding.

Cocok untuk:

- personal assistant lokal
- automation lintas aplikasi
- membaca file dan membuat laporan
- browser automation
- Telegram/Discord assistant
- workflow 24/7 di VPS
- research dan dokumentasi

Peran dalam stack:

```text
OpenClaw = agent automation dan personal workflow
```

### 4. 9Router

9Router adalah AI gateway atau router model.

Cocok untuk:

- satu endpoint untuk banyak provider
- routing model
- fallback provider
- quota tracking
- usage analytics
- monitoring token
- cost control

Peran dalam stack:

```text
9Router = pusat routing model AI dan monitoring penggunaan
```

### 5. Provider AI

Provider AI adalah sumber model yang dipakai agent.

Contoh:

- OpenAI
- Anthropic
- Google Gemini
- Xiaomi MiMo
- OpenAI-compatible provider lain
- local model melalui Ollama/LM Studio

Peran dalam stack:

```text
Provider AI = model yang melakukan reasoning dan menghasilkan jawaban
```

## Alur Request

### Alur coding lokal

```text
Developer memberi tugas coding
  -> Codex/OpenCode membaca repo
  -> request model dikirim ke 9Router
  -> 9Router memilih provider/model
  -> model memberi rencana/jawaban
  -> agent mengubah file atau menjalankan test
  -> hasil dikembalikan ke developer
```

### Alur OpenClaw lokal

```text
Developer memberi instruksi ke OpenClaw
  -> OpenClaw membaca file/browser/tool lokal
  -> OpenClaw meminta reasoning ke model via 9Router
  -> 9Router meneruskan ke provider
  -> OpenClaw menjalankan aksi
  -> hasil dikirim ke developer
```

### Alur automation VPS

```text
Trigger Telegram/Discord/GitHub/Cron
  -> OpenClaw server menerima task
  -> OpenClaw meminta model via 9Router
  -> OpenClaw membaca log/API/server
  -> OpenClaw membuat laporan
  -> hasil dikirim ke channel
```

## Tahap Implementasi

### Tahap 1: Belajar lokal

Mulai dari lokal agar aman.

Setup:

```text
Laptop
  -> Codex
  -> OpenClaw lokal
  -> 9Router lokal atau 9Router VPS
```

Target:

- paham cara kerja agent
- paham permission
- paham routing model
- coba task kecil
- belum expose service ke publik

Contoh task:

```text
Baca project ini, jelaskan struktur folder, dan buat draft dokumentasi setup.
```

### Tahap 2: 9Router di VPS

Pindahkan 9Router ke VPS agar endpoint model terpusat.

Setup:

```text
Laptop
  -> Codex/OpenCode/OpenClaw
  -> https://9router.domainkamu.com/v1
  -> Provider AI
```

Target:

- semua tool AI memakai satu endpoint
- usage analytics mulai terkumpul
- quota dan biaya mudah dipantau
- provider bisa diganti tanpa mengubah banyak tool

### Tahap 3: OpenClaw server untuk automation

Tambahkan OpenClaw di VPS untuk task yang harus online terus.

Setup:

```text
VPS
  -> OpenClaw server
  -> 9Router
  -> Provider AI
```

Target:

- Telegram/Discord bot
- monitoring server
- laporan harian
- GitHub issue summary
- reminder rutin

### Tahap 4: Workflow tim

Jika sudah stabil, atur workflow untuk tim.

Setup:

```text
Developer laptop
  -> agent lokal masing-masing

VPS
  -> 9Router shared
  -> OpenClaw automation shared

Channel tim
  -> Discord/Telegram/GitHub
```

Target:

- dokumentasi project otomatis
- issue triage
- changelog
- monitoring deploy
- ringkasan meeting
- audit penggunaan AI

## Rekomendasi Penempatan

| Komponen | Lokasi Awal | Lokasi Produksi Ringan | Catatan |
|---|---|---|---|
| Codex | Lokal | Lokal | Paling cocok untuk repo lokal |
| OpenCode | Lokal | Lokal/VPS | Bisa diarahkan ke 9Router |
| OpenClaw personal | Lokal | Lokal | Aman untuk file pribadi |
| OpenClaw automation | Tidak perlu dulu | VPS | Untuk bot/webhook/cron |
| 9Router | Lokal atau VPS | VPS | Lebih baik terpusat |
| Provider AI | Cloud/local | Cloud/local | Diakses lewat 9Router |
| Dashboard publik | Hindari | HTTPS + auth | Jangan expose port internal |

## Cost Control

9Router menjadi titik penting untuk mengontrol biaya dan token.

Strategi:

1. Pakai model murah untuk tugas ringan.
2. Pakai model kuat hanya untuk reasoning berat.
3. Buat combo/routing rule berdasarkan jenis task.
4. Pantau input/output token harian.
5. Tetapkan limit harian atau per project.
6. Gunakan fallback provider jika provider utama error.
7. Audit request yang tokennya besar.

Contoh routing:

```text
Task dokumentasi ringan
  -> model murah

Task debugging rumit
  -> model reasoning kuat

Task ringkasan log
  -> model cepat dan murah

Task coding besar
  -> model kuat dengan context besar
```

## Security Model

Prinsip keamanan:

```text
Agent boleh membantu, tetapi tidak boleh diberi akses tanpa batas.
```

Aturan utama:

- OpenClaw lokal hanya boleh akses folder yang diperlukan.
- OpenClaw VPS tidak berjalan sebagai root.
- 9Router tidak expose port internal langsung.
- Semua akses publik lewat HTTPS.
- API key tidak disimpan di dokumentasi.
- Command destruktif wajib konfirmasi.
- Deploy production wajib approval manusia.
- Backup config dan data dilakukan berkala.

Port internal:

```text
9Router: 20128
OpenClaw Gateway: 18789
```

Port publik yang boleh dibuka:

```text
80/tcp
443/tcp
22/tcp untuk SSH, lebih baik dibatasi IP
```

## Permission Policy Ringkas

| Aksi | Status |
|---|---|
| Membaca file workspace | Boleh |
| Membuat draft dokumentasi | Boleh jika diminta |
| Menjalankan test/lint | Boleh jika non-destruktif |
| Mengedit source code | Harus konfirmasi |
| Install dependency | Harus konfirmasi |
| Restart service | Harus konfirmasi |
| Migration database | Harus konfirmasi |
| Commit/push git | Harus konfirmasi |
| Deploy production | Wajib approval manusia |
| Hapus file/database | Dilarang tanpa izin eksplisit |
| Membagikan API key | Dilarang |

## Workflow Harian

### Pagi

```text
OpenClaw VPS:
- cek status server
- cek issue GitHub baru
- buat ringkasan error log
- kirim laporan ke Telegram/Discord
```

### Siang

```text
Codex/OpenCode:
- bantu coding
- debugging
- refactor
- jalankan test

OpenClaw lokal:
- bantu riset
- buat dokumentasi
- baca catatan project
```

### Sore

```text
OpenClaw/Codex:
- buat changelog
- ringkas pekerjaan hari ini
- buat daftar next action
- update dokumentasi
```

### Mingguan

```text
9Router:
- audit token
- cek provider yang paling sering dipakai
- cek request paling mahal
- update routing rule

VPS:
- backup config
- update package
- cek security log
```

## Contoh Use Case End-to-End

### Use case: membuat dokumentasi otomatis

```text
Developer:
  "Buat dokumentasi setup project ini."

Codex/OpenClaw lokal:
  -> membaca README/package/config
  -> membuat draft docs/setup.md
  -> menjalankan command non-destruktif jika perlu
  -> meminta review manusia

9Router:
  -> routing ke model yang cocok
  -> mencatat token dan biaya
```

### Use case: monitoring deploy

```text
GitHub webhook / cron
  -> OpenClaw VPS
  -> cek status service
  -> baca log terbatas
  -> ringkas masalah
  -> kirim laporan ke Discord

9Router:
  -> pilih model ringkasan cepat
  -> log usage
```

### Use case: riset tool baru

```text
Developer:
  "Bandingkan tool AI gateway untuk project kita."

OpenClaw lokal:
  -> research
  -> buat tabel perbandingan
  -> tulis rekomendasi

Codex:
  -> memasukkan hasil ke dokumentasi repo
```

## Roadmap Belajar

Urutan belajar yang disarankan:

1. Pahami konsep AI agent.
2. Pahami 9Router sebagai AI gateway.
3. Jalankan OpenClaw lokal.
4. Hubungkan OpenClaw ke 9Router.
5. Coba coding agent untuk dokumentasi project.
6. Buat permission policy.
7. Deploy 9Router di VPS.
8. Tambahkan OpenClaw VPS untuk automation kecil.
9. Hubungkan Telegram/Discord.
10. Buat monitoring token dan laporan mingguan.

## Checklist Implementasi

Checklist lokal:

- Codex/OpenCode bisa dipakai di project.
- OpenClaw lokal bisa menjalankan task sederhana.
- Model provider sudah tersambung.
- Permission folder dibatasi.
- Dokumentasi workflow dibuat.

Checklist 9Router:

- 9Router berjalan di VPS.
- Endpoint `/v1` bisa dipakai.
- Provider sudah dikonfigurasi.
- Usage analytics aktif.
- Quota/cost dipantau.
- HTTPS aktif jika diakses dari luar.

Checklist OpenClaw VPS:

- Berjalan sebagai user non-root.
- Firewall aktif.
- Port internal tidak dibuka publik.
- Service auto-start.
- Backup tersedia.
- Bot/webhook diuji dengan task kecil.

Checklist tim:

- Ada aturan approval.
- Ada permission matrix.
- Ada channel khusus agent.
- Ada dokumentasi prompt.
- Ada audit token mingguan.
- Ada human review untuk perubahan penting.

## Kesimpulan

NalTech AI Stack sebaiknya dibangun bertahap:

```text
Mulai lokal
  -> pusatkan model lewat 9Router
  -> tambah automation VPS
  -> baru masuk workflow tim
```

Kunci utamanya:

- jangan langsung memberi agent akses besar
- pisahkan agent lokal dan agent server
- gunakan 9Router untuk kontrol model dan biaya
- semua akses publik harus aman
- manusia tetap menjadi approval terakhir untuk aksi penting

Dengan stack ini, AI tidak hanya menjadi chatbot, tetapi menjadi sistem kerja yang bisa membantu coding, dokumentasi, monitoring, research, dan automation secara terukur.
