---
title: "AI Tools Roadmap"
description: "Roadmap belajar AI Tools NalTech dari fondasi, AI gateway, coding agent, automation, security, cost control, local model, sampai mini project."
category: "AI Tools"
level: "Beginner"
order: 60
tags: ["ai", "roadmap", "learning-path", "agent", "gateway", "automation", "naltech"]
updated: "2026-05-23"
---

# AI Tools Roadmap

AI Tools Roadmap adalah urutan belajar untuk memahami dan memakai tool AI secara bertahap.

Tujuan roadmap ini:

- memberi urutan belajar yang jelas
- menghubungkan semua materi AI Tools
- membantu pemula mulai dari konsep dasar
- memberi jalur praktik sampai automation
- menjaga pembelajaran tetap aman, hemat biaya, dan terstruktur

## Gambaran Besar

Urutan belajar:

```text
Fondasi
  -> AI Gateway
  -> Coding Agent
  -> Agent Automation
  -> Security
  -> Cost Control
  -> Local Model
  -> Advanced Workflow
```

Target akhirnya:

```text
Developer bisa memakai Codex/OpenCode/OpenClaw
  -> routing model lewat 9Router
  -> automation aman
  -> biaya terkendali
  -> local model sebagai opsi tambahan
```

## Level 1: Fondasi AI Stack

Tujuan:

- memahami peta besar tool AI
- tahu peran agent, gateway, provider, dan automation
- tahu kenapa butuh struktur sebelum praktik

Materi:

1. [NalTech AI Stack](/docs/ai-tools/naltech-ai-stack/)
2. [9Router Proxy](/docs/ai-tools/9router-proxy/)
3. [AI Gateway Comparison](/docs/ai-tools/ai-gateway-comparison/)

Yang harus dipahami:

- apa itu AI stack
- apa itu AI gateway
- bedanya agent dan model
- posisi 9Router
- kapan pakai cloud model vs local model

Praktik:

```text
1. Baca NalTech AI Stack.
2. Gambar ulang arsitektur sederhana:
   Codex/OpenCode/OpenClaw -> 9Router -> Provider AI
3. Buka dashboard 9Router.
4. Lihat menu Providers, Combos, Usage, dan Quota.
```

Checklist:

- [ ] Bisa menjelaskan fungsi 9Router.
- [ ] Bisa menjelaskan fungsi OpenClaw.
- [ ] Bisa menjelaskan fungsi OpenCode.
- [ ] Bisa menjelaskan kenapa perlu AI gateway.
- [ ] Bisa membaca alur request dari agent ke provider.

## Level 2: Coding Agent

Tujuan:

- memakai AI untuk coding dengan kontrol yang aman
- memahami plan mode dan build mode
- membuat prompt coding yang jelas
- menghindari perubahan file yang terlalu luas

Materi:

1. [OpenCode](/docs/ai-tools/opencode/)
2. [Prompt Engineering untuk Agent](/docs/ai-tools/prompt-engineering-agent/)
3. [AI Agent Security](/docs/ai-tools/ai-agent-security/)

Yang harus dipahami:

- coding agent berbeda dari chatbot
- agent bisa membaca dan mengubah file
- prompt harus punya scope dan output format
- perubahan besar harus dimulai dengan plan
- review diff tetap wajib

Praktik:

```text
1. Jalankan OpenCode di project kecil.
2. Jalankan /init untuk membuat AGENTS.md.
3. Minta OpenCode menjelaskan struktur project.
4. Minta rencana fitur kecil tanpa edit file.
5. Review rencana.
6. Izinkan implementasi kecil.
7. Jalankan test/build.
8. Review git diff.
```

Prompt latihan:

```text
Baca project ini dan jelaskan struktur folder, command development, dan file konfigurasi penting.
Jangan edit file.
Jawab maksimal 20 bullet.
```

Checklist:

- [ ] Bisa menjalankan coding agent.
- [ ] Bisa membuat prompt plan mode.
- [ ] Bisa membatasi scope file.
- [ ] Bisa meminta agent menjalankan test.
- [ ] Bisa review diff sebelum commit.

## Level 3: Personal Agent dan Workflow

Tujuan:

- memahami OpenClaw sebagai agent yang lebih luas dari coding
- memakai agent untuk file, laporan, research, dan workflow personal
- membedakan agent lokal dan agent VPS

Materi:

1. [OpenClaw](/docs/ai-tools/openclaw/)
2. [Prompt Engineering untuk Agent](/docs/ai-tools/prompt-engineering-agent/)
3. [AI Agent Security](/docs/ai-tools/ai-agent-security/)

Yang harus dipahami:

- OpenClaw bisa memakai tool
- agent lokal lebih aman untuk belajar
- agent VPS cocok untuk automation 24/7
- permission matrix penting
- data eksternal bukan instruksi

Praktik:

```text
1. Jalankan OpenClaw lokal.
2. Hubungkan ke model atau 9Router.
3. Beri akses ke folder project dummy.
4. Minta OpenClaw membuat ringkasan project.
5. Minta OpenClaw membuat draft dokumentasi.
6. Jangan aktifkan akses luas dulu.
```

Checklist:

- [ ] Bisa menjelaskan beda OpenClaw dan OpenCode.
- [ ] Bisa menentukan kapan OpenClaw lokal atau VPS.
- [ ] Bisa membuat permission policy sederhana.
- [ ] Bisa membuat prompt automation aman.
- [ ] Bisa membatasi akses folder.

## Level 4: AI Automation

Tujuan:

- membuat automation AI yang aman
- memahami trigger, runner, model, output, dan log
- mulai dari workflow read-only
- menghubungkan automation ke 9Router

Materi:

1. [AI Automation](/docs/ai-tools/ai-automation/)
2. [Cost Control AI](/docs/ai-tools/cost-control-ai/)
3. [AI Agent Security](/docs/ai-tools/ai-agent-security/)

Yang harus dipahami:

- automation harus punya trigger jelas
- data yang dibaca harus dibatasi
- output harus diaudit
- aksi berisiko butuh approval
- log dan monitoring wajib ada

Praktik mini project:

```text
Daily VPS Status Report
```

Langkah:

```text
1. Buat folder /opt/ai-automation.
2. Buat script daily-vps-report.
3. Ambil data uptime, disk, memory, docker, dan log terbatas.
4. Kirim ke 9Router.
5. Simpan report ke Markdown.
6. Kirim ke Telegram/Discord.
7. Jadwalkan dengan cron.
8. Pantau usage di 9Router.
```

Checklist:

- [ ] Bisa membuat trigger cron.
- [ ] Bisa membatasi data log.
- [ ] Bisa kirim request ke 9Router.
- [ ] Bisa menyimpan report.
- [ ] Bisa mengirim output ke Telegram/Discord.
- [ ] Bisa membaca log automation.

## Level 5: Security dan Governance

Tujuan:

- memahami risiko agent
- membuat permission matrix
- mencegah prompt injection dan data leakage
- membuat approval workflow

Materi:

1. [AI Agent Security](/docs/ai-tools/ai-agent-security/)
2. [OpenClaw](/docs/ai-tools/openclaw/)
3. [Prompt Engineering untuk Agent](/docs/ai-tools/prompt-engineering-agent/)

Yang harus dipahami:

- prompt injection
- tool injection
- secret leakage
- command injection
- data eksternal bukan instruksi
- Allow / Ask / Deny
- incident response

Praktik:

```text
1. Buat permission matrix untuk agent lokal.
2. Buat permission matrix untuk agent VPS.
3. Tambahkan security policy ke AGENTS.md.
4. Tambahkan tool policy ke TOOLS.md.
5. Buat runbook incident response sederhana.
```

Checklist:

- [ ] Bisa menjelaskan prompt injection.
- [ ] Bisa menjelaskan data exfiltration.
- [ ] Bisa membuat policy Allow/Ask/Deny.
- [ ] Bisa menentukan aksi yang wajib approval.
- [ ] Bisa membuat checklist sebelum production.

## Level 6: Cost Control

Tujuan:

- memahami token dan biaya
- memilih model sesuai task
- membuat routing rule
- audit request mahal
- mengurangi pemborosan token

Materi:

1. [Cost Control AI](/docs/ai-tools/cost-control-ai/)
2. [9Router Proxy](/docs/ai-tools/9router-proxy/)
3. [Prompt Engineering untuk Agent](/docs/ai-tools/prompt-engineering-agent/)

Yang harus dipahami:

- input token
- output token
- context window
- model ringan vs model kuat
- summarization strategy
- caching context
- audit request di 9Router

Praktik:

```text
1. Buka dashboard Usage di 9Router.
2. Cari request paling besar.
3. Catat model yang paling sering dipakai.
4. Buat rule: task ringan -> model murah.
5. Buat prompt hemat token.
6. Buat laporan penggunaan mingguan.
```

Checklist:

- [ ] Bisa membaca usage token di 9Router.
- [ ] Bisa membedakan input/output token.
- [ ] Bisa memilih model sesuai task.
- [ ] Bisa membuat prompt hemat token.
- [ ] Bisa mengaudit request mahal.

## Level 7: Local AI Model

Tujuan:

- menjalankan model lokal
- memahami kapan local model cocok
- menghubungkan local model ke 9Router
- memakai local model untuk task ringan

Materi:

1. [Local AI Model Stack](/docs/ai-tools/local-ai-model-stack/)
2. [AI Gateway Comparison](/docs/ai-tools/ai-gateway-comparison/)
3. [Cost Control AI](/docs/ai-tools/cost-control-ai/)

Yang harus dipahami:

- Ollama
- LM Studio
- llama.cpp
- Open WebUI
- OpenAI-compatible endpoint
- hardware requirement
- local vs cloud trade-off

Praktik:

```text
1. Install Ollama.
2. Pull model kecil.
3. Test chat lokal.
4. Test endpoint /v1.
5. Hubungkan ke 9Router.
6. Pakai local model untuk ringkasan sederhana.
7. Buat fallback ke cloud model.
```

Checklist:

- [ ] Bisa menjalankan model lokal.
- [ ] Bisa test endpoint OpenAI-compatible.
- [ ] Bisa menjelaskan kebutuhan RAM/VRAM.
- [ ] Bisa menentukan task yang cocok untuk local model.
- [ ] Bisa menghubungkan local model ke gateway.

## Level 8: Advanced Workflow

Tujuan:

- menggabungkan agent, gateway, automation, dan local model
- membuat workflow tim
- mulai memikirkan observability dan evaluation

Materi:

1. [NalTech AI Stack](/docs/ai-tools/naltech-ai-stack/)
2. [AI Gateway Comparison](/docs/ai-tools/ai-gateway-comparison/)
3. [AI Automation](/docs/ai-tools/ai-automation/)
4. [AI Agent Security](/docs/ai-tools/ai-agent-security/)
5. [AI Evaluation & Testing](/docs/ai-tools/ai-evaluation-testing/)

Contoh advanced workflow:

```text
GitHub issue dibuat
  -> OpenClaw membaca issue
  -> 9Router memilih model
  -> AI membuat triage
  -> hasil dikirim ke Discord
  -> developer review
```

Contoh lain:

```text
Cron mingguan
  -> ambil usage 9Router
  -> AI membuat cost report
  -> rekomendasi routing model
  -> kirim ke channel tim
```

Checklist:

- [ ] Bisa membuat workflow multi-step.
- [ ] Bisa memilih trigger yang tepat.
- [ ] Bisa menentukan approval point.
- [ ] Bisa menghubungkan output ke channel tim.
- [ ] Bisa memantau biaya dan log.

## Mini Project Roadmap

### Mini Project 1: Project Documentation Assistant

Goal:

```text
Agent membaca project kecil dan membuat draft dokumentasi setup.
```

Materi pendukung:

- OpenCode
- Prompt Engineering
- AI Agent Security

Output:

```text
docs/setup-development.md
```

### Mini Project 2: Daily VPS Status Report

Goal:

```text
Automation membuat laporan status VPS harian.
```

Materi pendukung:

- AI Automation
- Cost Control AI
- 9Router Proxy

Output:

```text
reports/server-report-YYYY-MM-DD.md
Telegram/Discord message
```

### Mini Project 3: AI Cost Weekly Report

Goal:

```text
AI membuat laporan penggunaan token mingguan dari 9Router.
```

Materi pendukung:

- Cost Control AI
- 9Router Proxy
- Prompt Engineering

Output:

```text
AI Usage Weekly Report
```

### Mini Project 4: Local Model Experiment

Goal:

```text
Menjalankan Ollama dan menghubungkannya ke 9Router.
```

Materi pendukung:

- Local AI Model Stack
- AI Gateway Comparison
- Cost Control AI

Output:

```text
Local model bisa dipakai untuk task ringkasan ringan.
```

### Mini Project 5: Agent Security Policy

Goal:

```text
Membuat AGENTS.md dan TOOLS.md untuk workflow agent aman.
```

Materi pendukung:

- AI Agent Security
- Prompt Engineering untuk Agent
- OpenClaw

Output:

```text
AGENTS.md
TOOLS.md
Permission Matrix
```

## Rekomendasi Urutan Baca

Untuk pemula:

```text
1. NalTech AI Stack
2. 9Router Proxy
3. OpenCode
4. Prompt Engineering untuk Agent
5. AI Agent Security
6. AI Automation
7. Cost Control AI
8. Local AI Model Stack
9. AI Gateway Comparison
10. OpenClaw
```

Untuk fokus automation:

```text
1. NalTech AI Stack
2. OpenClaw
3. AI Automation
4. Prompt Engineering untuk Agent
5. AI Agent Security
6. Cost Control AI
7. 9Router Proxy
```

Untuk fokus coding:

```text
1. OpenCode
2. Prompt Engineering untuk Agent
3. AI Agent Security
4. 9Router Proxy
5. Cost Control AI
6. Local AI Model Stack
```

Untuk fokus infrastructure:

```text
1. 9Router Proxy
2. AI Gateway Comparison
3. Cost Control AI
4. AI Agent Security
5. AI Automation
6. Local AI Model Stack
```

## Checklist Kompetensi Akhir

Setelah menyelesaikan roadmap ini, targetnya kamu bisa:

- [ ] Menjelaskan arsitektur AI stack.
- [ ] Menjalankan AI gateway.
- [ ] Menghubungkan agent ke 9Router.
- [ ] Memakai coding agent dengan aman.
- [ ] Menulis prompt agent yang jelas.
- [ ] Membuat automation read-only.
- [ ] Mengirim report ke Telegram/Discord.
- [ ] Membuat permission matrix.
- [ ] Mengontrol token dan biaya.
- [ ] Menjalankan local model sederhana.
- [ ] Menentukan kapan pakai local vs cloud.
- [ ] Membuat mini project AI automation.

## Kesimpulan

Roadmap ini dibuat agar belajar AI Tools tidak lompat-lompat.

Urutan terbaik:

```text
Pahami stack
  -> pakai gateway
  -> pakai coding agent
  -> belajar prompt
  -> amankan agent
  -> buat automation
  -> kontrol biaya
  -> tambah local model
```

Dengan urutan ini, AI Tools bisa dipelajari sebagai sistem kerja yang utuh: bukan hanya chat, tetapi coding, automation, monitoring, security, dan cost control.
