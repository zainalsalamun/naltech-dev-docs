---
title: "Hermes Agent"
description: "Panduan memahami Hermes Agent dari Nous Research sebagai self-improving AI agent dengan persistent memory, skills, messaging gateway, automation, subagents, dan integrasi 9Router."
category: "AI Tools"
level: "Intermediate"
order: 150
tags: ["ai", "agent", "hermes", "nous-research", "automation", "memory", "skills", "9router"]
updated: "2026-05-23"
---

# Hermes Agent

Hermes Agent adalah **open-source self-improving AI agent** dari Nous Research. Hermes dirancang sebagai agent yang bisa berjalan terus, mengingat konteks lintas sesi, membuat skill dari pengalaman, dan diakses lewat terminal maupun messaging platform seperti Telegram, Discord, Slack, WhatsApp, Signal, dan lainnya.

Hermes bukan hanya chatbot. Hermes adalah agent yang bisa:

- memakai tool
- menjalankan terminal
- memakai memory
- membuat skill
- menjalankan automation terjadwal
- berjalan di laptop, VPS, cloud VM, atau backend lain
- menerima instruksi dari CLI atau messaging gateway

Ringkasnya:

```text
Hermes Agent = persistent personal agent + skills + memory + messaging gateway + automation
```

## Posisi Hermes dalam NalTech AI Stack

Hermes bisa menjadi alternatif atau pelengkap OpenClaw.

Arsitektur:

```text
Telegram / Discord / CLI
  -> Hermes Agent
  -> 9Router
  -> Provider AI / Local Model
```

Peran:

```text
Hermes Agent
  -> agent yang menjalankan workflow

9Router
  -> gateway model, routing, quota, usage analytics

Provider AI
  -> model reasoning
```

## Fitur Utama

### 1. Persistent memory

Hermes dirancang untuk mengingat konteks lintas sesi.

Contoh yang bisa diingat:

- preferensi user
- project yang sering dikerjakan
- environment kerja
- kebiasaan command
- hasil pekerjaan sebelumnya

Manfaat:

```text
Tidak perlu menjelaskan ulang konteks dari nol setiap sesi.
```

### 2. Self-improving learning loop

Hermes memiliki konsep learning loop: ketika menyelesaikan masalah, agent bisa menyimpan pengetahuan agar bisa dipakai lagi.

Contoh:

```text
Hermes pernah membantu deploy project.
Ia menyimpan langkah dan catatan sebagai skill.
Saat task serupa muncul, Hermes bisa memakai skill itu lagi.
```

### 3. Skills system

Hermes memakai sistem skill. Skill adalah instruksi reusable yang menjelaskan cara melakukan task tertentu.

Contoh skill:

- deploy project
- membuat diagram
- meringkas issue GitHub
- menjalankan backup
- membuat laporan harian
- setup server
- membuat dokumentasi

Skill membuat agent lebih konsisten karena tidak selalu mulai dari nol.

### 4. Messaging gateway

Hermes bisa diakses dari banyak channel.

Contoh:

- Telegram
- Discord
- Slack
- WhatsApp
- Signal
- CLI

Ini cocok untuk agent yang berjalan di VPS dan bisa dihubungi dari mana saja.

### 5. Scheduled automation

Hermes mendukung task terjadwal.

Contoh:

```text
Setiap pagi:
  -> cek status VPS
  -> cek issue GitHub
  -> buat laporan
  -> kirim ke Telegram/Discord
```

### 6. Subagents dan parallel work

Hermes mendukung pola kerja yang bisa mendelegasikan task ke subagent atau proses terpisah.

Contoh:

```text
Task utama:
  -> subagent 1: riset dokumentasi
  -> subagent 2: cek repo
  -> subagent 3: buat ringkasan
```

Ini berguna untuk task yang bisa dipecah.

### 7. Multi-provider model

Hermes bisa memakai banyak provider/model.

Contoh:

- Nous Portal
- OpenRouter
- OpenAI
- Hugging Face
- provider OpenAI-compatible
- local model
- 9Router sebagai gateway

## Hermes vs OpenClaw vs OpenCode vs Codex

| Tool | Fokus | Cocok Untuk |
|---|---|---|
| Hermes Agent | persistent self-improving agent | personal agent 24/7, messaging, skills, memory, automation |
| OpenClaw | personal AI agent/runtime | automation, browser, file, CLI, chat app |
| OpenCode | coding agent open-source | coding terminal, repo, model custom |
| Codex | coding agent di workspace | edit code, test, refactor, debugging |
| 9Router | AI gateway | routing model, quota, usage analytics |

### Kapan pakai Hermes?

Gunakan Hermes jika:

- ingin agent yang berjalan terus
- ingin memory lintas sesi
- ingin agent bisa membuat/memakai skill
- ingin akses dari Telegram/Discord/Slack
- ingin automation 24/7
- ingin agent berkembang dari pengalaman

### Kapan pakai OpenClaw?

Gunakan OpenClaw jika:

- ingin personal agent dengan tool luas
- ingin workflow lokal dan VPS
- ingin eksplorasi automation dengan agent runtime
- ingin integrasi browser/file/API

### Kapan pakai OpenCode atau Codex?

Gunakan OpenCode/Codex jika fokusnya coding di repository:

- edit file
- jalankan test
- debugging
- refactor
- dokumentasi codebase

## Install Hermes Agent

### Linux, macOS, WSL2, Termux

Install resmi:

```bash
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash
```

Reload shell:

```bash
source ~/.bashrc
```

Atau jika memakai zsh:

```bash
source ~/.zshrc
```

Jalankan:

```bash
hermes
```

### Windows

Native Windows masih lebih cocok dianggap early/beta. Untuk setup yang lebih stabil, gunakan WSL2.

PowerShell installer:

```powershell
iex (irm https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.ps1)
```

Rekomendasi:

```text
Windows user -> pakai WSL2 jika ingin lebih stabil.
```

## Command Dasar

Command penting:

```bash
hermes              # start interactive CLI
hermes model        # pilih provider/model
hermes tools        # konfigurasi tool
hermes config set   # set config individual
hermes gateway      # messaging gateway
hermes setup        # setup wizard
hermes update       # update Hermes
hermes doctor       # diagnosis masalah
```

Command migrasi:

```bash
hermes claw migrate
```

Dipakai jika datang dari OpenClaw dan ingin migrasi.

## Setup Model

Jalankan:

```bash
hermes model
```

Pilih provider/model yang ingin dipakai.

Untuk NalTech, opsi yang paling rapi:

```text
Hermes
  -> 9Router OpenAI-compatible endpoint
  -> provider AI
```

## Integrasi Hermes dengan 9Router

Karena Hermes mendukung custom/OpenAI-compatible endpoint, 9Router bisa menjadi gateway model.

Konfigurasi konsep:

```text
Base URL: https://9router.domainkamu.com/v1
API Key: API key 9Router
Model: model/combo dari 9Router
```

Jika lokal:

```text
Base URL: http://localhost:20128/v1
```

Manfaat:

- Hermes tidak perlu langsung ke banyak provider
- model bisa diganti dari 9Router
- usage token bisa dipantau
- fallback provider bisa diatur
- cost control lebih mudah

Arsitektur:

```text
Hermes Agent
  -> 9Router
  -> OpenAI / Anthropic / MiMo / Local Model
```

## Hermes di Lokal atau VPS?

### Lokal

Cocok untuk:

- belajar
- eksperimen
- coding/research pribadi
- akses file lokal
- testing skill

Kelebihan:

- lebih aman untuk awal
- tidak expose service publik
- mudah melihat aksi agent

Kekurangan:

- hanya jalan saat laptop hidup
- kurang cocok untuk automation 24/7

### VPS

Cocok untuk:

- agent 24/7
- Telegram/Discord agent
- scheduled reports
- monitoring server
- workflow tim

Kelebihan:

- online terus
- bisa diakses dari chat platform
- cocok untuk automation

Kekurangan:

- butuh hardening
- jangan berjalan sebagai root
- perlu firewall, HTTPS, backup, permission policy

Rekomendasi:

```text
Belajar -> lokal
Automation 24/7 -> VPS
Model routing -> 9Router
```

## Use Case Hermes

### 1. Personal assistant 24/7

Hermes berjalan di VPS dan bisa dihubungi dari Telegram.

Contoh:

```text
/status project
/ringkas issue hari ini
/buat draft changelog
```

### 2. Daily report

```text
Setiap pagi:
  -> cek server
  -> cek issue
  -> cek usage AI
  -> kirim report
```

### 3. Skill-based workflow

Hermes membuat skill setelah menyelesaikan task kompleks.

Contoh:

```text
Skill: deploy Astro docs
Skill: backup 9Router data
Skill: audit AI cost
```

### 4. Research assistant

Hermes bisa membantu riset tool, membuat perbandingan, dan menyimpan hasil sebagai memory/skill.

### 5. Coding helper

Hermes bisa membantu coding/research, tetapi untuk coding mendalam di repo, Codex/OpenCode tetap lebih fokus.

### 6. Automation server

Hermes cocok untuk agent server yang menerima command dari chat dan menjalankan workflow read-only atau semi-automated.

## Security

Karena Hermes persistent dan bisa punya memory/tools/gateway, security sangat penting.

Aturan:

- jangan jalankan sebagai root
- mulai lokal dulu
- batasi tool
- gunakan user non-root di VPS
- API key simpan di env/secret manager
- jangan expose gateway tanpa auth
- whitelist user/channel
- command berisiko wajib approval
- jangan kirim secret ke chat
- backup `~/.hermes`

Command berisiko:

```text
restart service
deploy
update package
ubah firewall
hapus file
migration database
commit/push
```

Harus approval manusia.

## Permission Policy untuk Hermes

Contoh policy:

```text
Allow:
- membaca file workspace
- membuat laporan
- membaca log terbatas
- menjalankan command status

Ask:
- edit source code
- install dependency
- restart service
- deploy
- push git

Deny:
- hapus file/folder
- drop database
- membaca private key
- membagikan API key
- force push
```

## Hermes + NalTech AI Stack

Posisi ideal:

```text
Laptop:
  -> Codex/OpenCode untuk coding
  -> Hermes lokal untuk eksperimen personal

VPS:
  -> 9Router sebagai AI gateway
  -> Hermes untuk automation 24/7
  -> optional OpenClaw/n8n untuk workflow lain

Provider:
  -> cloud model
  -> local model via Ollama/LM Studio
```

Hermes bisa menjadi:

- personal AI agent
- automation runner
- chatops assistant
- skill-based workflow engine

9Router tetap menjadi:

- gateway model
- usage analytics
- quota tracking
- cost control

## Troubleshooting

### `hermes` command tidak ditemukan

Cek:

```bash
which hermes
echo $PATH
```

Reload shell:

```bash
source ~/.bashrc
```

atau:

```bash
source ~/.zshrc
```

### Model tidak tersambung

Cek:

```bash
hermes model
hermes doctor
```

Jika memakai 9Router:

- base URL harus memakai `/v1`
- API key benar
- model/combo tersedia
- 9Router aktif

### Gateway chat tidak jalan

Cek:

```bash
hermes gateway
hermes doctor
```

Cek juga token bot, chat ID, permission channel, dan firewall.

### Agent terlalu bebas

Solusi:

- batasi tools
- update permission policy
- gunakan approval untuk action berisiko
- jalankan dalam container/sandbox jika perlu

## Checklist Belajar Hermes

- [ ] Install Hermes.
- [ ] Jalankan `hermes`.
- [ ] Jalankan `hermes doctor`.
- [ ] Pilih model dengan `hermes model`.
- [ ] Coba task ringan.
- [ ] Coba konfigurasi tool.
- [ ] Pelajari memory dan skills.
- [ ] Coba gateway Telegram/Discord.
- [ ] Hubungkan ke 9Router.
- [ ] Buat permission policy.
- [ ] Baru deploy ke VPS jika sudah paham.

## Kesimpulan

Hermes Agent adalah agent yang cocok jika kita ingin AI assistant yang hidup lebih lama dari satu sesi, punya memory, bisa membuat skill, dan bisa dihubungi dari messaging platform.

Dalam NalTech AI Stack:

```text
Hermes
  -> persistent/self-improving agent

9Router
  -> model gateway dan usage control

OpenCode/Codex
  -> coding agent

OpenClaw/n8n
  -> automation alternatif/pelengkap
```

Gunakan Hermes secara bertahap:

```text
local experiment
  -> 9Router integration
  -> chat gateway
  -> VPS automation
  -> skill-based workflow
```

## Referensi

- [Hermes Agent GitHub](https://github.com/NousResearch/hermes-agent)
- [Hermes Agent Hugging Face Integration](https://huggingface.co/docs/inference-providers/en/integrations/hermes-agent)
- [Nous Research](https://nousresearch.com/)

