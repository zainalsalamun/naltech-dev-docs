---
title: "OpenClaw"
description: "Panduan memahami OpenClaw sebagai personal AI agent, cara kerja, use case, pilihan lokal vs VPS, dan integrasi dengan 9Router."
category: "AI Tools"
level: "Intermediate"
order: 90
tags: ["ai", "agent", "automation", "openclaw", "llm", "workflow"]
updated: "2026-05-22"
---

# OpenClaw

OpenClaw adalah **open-source personal AI agent**. Berbeda dari chatbot biasa yang hanya membalas teks, OpenClaw dirancang agar AI bisa menjalankan aksi nyata melalui tool yang tersedia di komputer, server, browser, terminal, file system, dan integrasi aplikasi.

Kalau chatbot biasa hanya menjawab:

```text
User bertanya
-> AI menjawab
```

OpenClaw bekerja seperti agent:

```text
User memberi instruksi
-> OpenClaw memahami tujuan
-> OpenClaw memilih tool yang dibutuhkan
-> OpenClaw menjalankan aksi
-> hasil aksi dikirim balik ke AI
-> AI melanjutkan sampai tugas selesai
-> user menerima hasil akhir
```

Dengan pola ini, OpenClaw bisa menjadi assistant yang bukan hanya memberi saran, tetapi juga membantu mengerjakan tugas.

## Posisi OpenClaw dalam Ekosistem AI

OpenClaw **bukan model AI**. Ia adalah runtime atau orchestrator yang menghubungkan model AI dengan tool yang bisa dipakai untuk bekerja.

Model AI bisa berasal dari:

- OpenAI
- Anthropic
- Google Gemini
- provider OpenAI-compatible
- local model seperti Ollama
- gateway seperti 9Router

Peran masing-masing:

```text
Model AI
  -> berpikir, membuat rencana, menulis jawaban

OpenClaw
  -> menjalankan tool, mengelola workflow, memberi akses ke komputer atau aplikasi

9Router
  -> merutekan request model AI ke provider yang sesuai
```

Jika digabung:

```text
User
  -> OpenClaw
  -> 9Router
  -> Provider AI / Model AI
  -> 9Router
  -> OpenClaw menjalankan tool
  -> hasil kembali ke User
```

## Cara Kerja OpenClaw

Secara umum, OpenClaw bekerja dalam beberapa tahap.

### 1. Menerima instruksi

User memberi instruksi melalui interface yang tersedia, misalnya:

- CLI atau terminal
- chat app seperti Telegram, Discord, Slack, WhatsApp, atau Signal
- companion app
- dashboard atau web UI
- automation trigger

Contoh instruksi:

```text
Cek folder project ini, baca README, lalu jelaskan struktur aplikasinya.
```

Atau:

```text
Baca email hari ini, cari yang berhubungan dengan invoice, lalu buat ringkasannya.
```

### 2. Mengirim konteks ke model AI

OpenClaw mengirim instruksi, konteks, daftar tool, dan aturan kerja ke model AI.

Model AI kemudian menentukan:

- tugas yang perlu dikerjakan
- tool apa yang perlu dipakai
- data apa yang perlu dibaca
- apakah perlu menjalankan command
- apakah perlu membuka browser
- apakah perlu membuat file, ringkasan, atau laporan

### 3. Menjalankan tool

Jika model AI meminta aksi, OpenClaw menjalankan tool yang sesuai.

Contoh tool:

- membaca file
- menulis file
- menjalankan command terminal
- membuka browser
- mengambil data website
- memanggil API
- membaca email
- membuat event calendar
- mengirim pesan ke chat app
- menjalankan plugin atau skill

### 4. Mengembalikan hasil tool ke model

Hasil eksekusi tool dikirim kembali ke model AI.

Contoh:

```text
Tool: baca file README.md
Hasil: isi README.md
```

Model AI membaca hasil tersebut, lalu memutuskan langkah berikutnya.

### 5. Menyelesaikan tugas

OpenClaw akan terus melakukan siklus:

```text
reasoning -> tool call -> hasil tool -> reasoning berikutnya
```

sampai tugas selesai atau butuh konfirmasi user.

## Contoh Alur Kerja

Contoh tugas:

```text
Rapikan inbox email saya dan buat ringkasan tagihan minggu ini.
```

Kemungkinan alurnya:

```text
1. OpenClaw membuka koneksi email.
2. OpenClaw mencari email yang berhubungan dengan invoice/tagihan.
3. OpenClaw membaca subject, pengirim, tanggal, dan nominal.
4. OpenClaw mengelompokkan tagihan.
5. OpenClaw membuat ringkasan.
6. OpenClaw bisa membuat reminder jika diminta.
7. OpenClaw mengirim laporan akhir ke user.
```

Contoh tugas coding:

```text
Baca project Laravel ini, cari route API user, lalu jelaskan alurnya.
```

Kemungkinan alurnya:

```text
1. OpenClaw membaca struktur folder.
2. OpenClaw mencari file route.
3. OpenClaw membaca controller terkait.
4. OpenClaw mencari model dan middleware.
5. OpenClaw membuat ringkasan alur request.
6. OpenClaw memberi rekomendasi perbaikan jika ada.
```

## Fitur Utama

### 1. Local-first

OpenClaw dapat berjalan di komputer sendiri. Ini penting karena data, file, konfigurasi, dan workflow bisa tetap berada di environment yang kita kontrol.

### 2. Cross-platform

OpenClaw mendukung macOS, Linux, dan Windows.

### 3. Model-agnostic

OpenClaw tidak terkunci ke satu model. Kita bisa memakai model dari berbagai provider atau local model.

### 4. Tool access

OpenClaw bisa diberi akses ke tool seperti file system, terminal, browser, API, dan integrasi aplikasi.

### 5. Persistent memory

OpenClaw dapat menyimpan konteks atau preferensi agar assistant lebih memahami cara kerja user dari waktu ke waktu.

### 6. Skills dan plugins

Kemampuan OpenClaw bisa diperluas menggunakan skill atau plugin. Ini membuat OpenClaw bisa disesuaikan untuk kebutuhan khusus.

### 7. Multi-channel

OpenClaw bisa dihubungkan ke banyak channel komunikasi. Ini membuatnya bisa dipakai bukan hanya dari terminal, tetapi juga dari chat app.

## OpenClaw Bisa Dipakai Untuk Apa Saja?

OpenClaw sering disebut personal AI assistant, tetapi kegunaannya bisa jauh lebih luas.

### 1. Coding agent

OpenClaw bisa membantu pekerjaan development:

- membaca codebase
- mencari bug
- menjelaskan arsitektur project
- membuat dokumentasi
- menjalankan test
- memperbaiki error sederhana
- membuat script automation
- review commit atau pull request

Contoh:

```text
Cek project ini, cari file konfigurasi database, lalu jelaskan cara setup development environment.
```

### 2. Automation kantor

OpenClaw bisa dipakai untuk workflow administrasi:

- merangkum email
- membuat draft balasan
- mengecek calendar
- membuat agenda meeting
- membuat reminder
- menyusun laporan mingguan
- mengelompokkan dokumen

Contoh:

```text
Buat ringkasan meeting minggu ini dari catatan yang ada di folder Notes.
```

### 3. Research assistant

OpenClaw bisa membantu riset:

- mencari informasi
- membandingkan beberapa tools
- merangkum artikel
- membuat tabel perbandingan
- menyiapkan bahan presentasi
- membuat daftar referensi

Contoh:

```text
Bandingkan 9Router, OpenRouter, dan LiteLLM untuk kebutuhan AI gateway pribadi.
```

### 4. Browser automation

OpenClaw dapat membantu tugas yang biasanya dilakukan lewat browser:

- membuka dashboard
- mengecek status order
- mengisi form
- mengambil data dari website
- memantau harga
- mengambil screenshot

Contoh:

```text
Buka dashboard deployment, cek service yang gagal, lalu buat ringkasan penyebabnya.
```

### 5. DevOps helper

Untuk server dan deployment, OpenClaw bisa membantu:

- membaca log server
- mengecek status service
- menjalankan command diagnosis
- membuat issue dari error
- membantu deploy
- membuat checklist incident

Contoh:

```text
Cek log Nginx hari ini, cari error 500 terbanyak, lalu kelompokkan berdasarkan endpoint.
```

### 6. Data operations

OpenClaw bisa membantu pekerjaan data ringan:

- membersihkan CSV
- menggabungkan file
- membuat ringkasan spreadsheet
- mengecek data duplikat
- membuat laporan dari data mentah

Contoh:

```text
Baca file CSV penjualan minggu ini, cari produk paling laku, lalu buat ringkasan.
```

### 7. Content workflow

OpenClaw bisa membantu workflow konten:

- membuat outline artikel
- membuat draft post
- merangkum komentar
- menyiapkan caption
- membuat variasi copywriting
- menyusun kalender konten

Contoh:

```text
Buat draft artikel dari catatan meeting ini, lalu buat 5 ide judul.
```

### 8. Personal knowledge base

OpenClaw bisa dipakai untuk mengelola catatan pribadi:

- mencari catatan lama
- membuat ringkasan harian
- menghubungkan dokumen terkait
- menyusun ulang knowledge base
- membuat indeks topik

Contoh:

```text
Cari semua catatan tentang Flutter state management, lalu buat ringkasan belajar.
```

### 9. Customer support internal

Untuk tim kecil, OpenClaw bisa membantu:

- membaca knowledge base
- membuat draft jawaban support
- mengelompokkan tiket
- mencari akar masalah dari log
- membuat FAQ dari pertanyaan berulang

### 10. Multi-agent orchestration

OpenClaw juga bisa dipakai sebagai pusat koordinasi beberapa agent:

- agent riset
- agent coding
- agent review
- agent dokumentasi
- agent deployment

Konsepnya:

```text
OpenClaw sebagai orchestrator
  -> agent coding mengerjakan perubahan
  -> agent review mengecek hasil
  -> agent dokumentasi memperbarui catatan
  -> agent deploy menjalankan release
```

## Lokal atau VPS?

Salah satu keputusan penting adalah menentukan tempat menjalankan OpenClaw: di komputer lokal atau di server seperti VPS.

### Rekomendasi awal

Untuk belajar dan eksplorasi, mulai dari lokal dulu.

Alur yang disarankan:

```text
Tahap 1: Jalankan OpenClaw di lokal
Tahap 2: Hubungkan OpenClaw lokal ke 9Router di VPS
Tahap 3: Jalankan OpenClaw di VPS untuk automation 24/7
Tahap 4: Pisahkan agent lokal dan agent server sesuai kebutuhan
```

## Menjalankan OpenClaw di Lokal

Lokal berarti OpenClaw berjalan di laptop atau komputer pribadi.

### Cocok untuk

- coding di project lokal
- membaca dan menulis file project
- eksplorasi awal
- browser automation lokal
- task pribadi
- belajar permission dan cara kerja agent
- penggunaan yang tidak harus online 24 jam

### Kelebihan lokal

- Lebih aman untuk belajar.
- Tidak perlu membuka service ke internet.
- Data project tetap di komputer sendiri.
- Lebih mudah melihat aksi yang dilakukan agent.
- Cocok untuk coding dan file editing.
- Cocok untuk eksperimen dengan akses terbatas.

### Kekurangan lokal

- Hanya berjalan saat komputer menyala.
- Tidak cocok untuk automation 24/7.
- Jika laptop sleep atau mati, agent berhenti.
- Kurang ideal untuk webhook publik.

### Contoh arsitektur lokal

```text
Laptop
  -> OpenClaw
  -> 9Router di VPS atau local provider
  -> Model AI
```

Jika memakai 9Router di VPS:

```text
OpenClaw lokal
  -> https://9router.domainkamu.com/v1
  -> provider AI
```

Kelebihan pola ini:

- OpenClaw tetap aman di laptop.
- Routing model tetap terpusat di 9Router.
- Usage analytics dan quota tetap bisa dipantau.
- Tidak perlu expose OpenClaw ke internet.

## Menjalankan OpenClaw di VPS

VPS berarti OpenClaw berjalan di server yang selalu online.

### Cocok untuk

- automation 24/7
- Telegram bot
- Discord bot
- Slack assistant
- webhook GitHub
- monitoring server
- reminder rutin
- workflow tim
- agent yang harus aktif walaupun laptop mati

### Kelebihan VPS

- Online terus.
- Cocok untuk automation dan webhook.
- Bisa menjadi central agent untuk beberapa device.
- Lebih cocok untuk integrasi Telegram, Discord, Slack, GitHub, dan server monitoring.
- Bisa digabung dengan 9Router di server yang sama.

### Kekurangan VPS

- Risiko keamanan lebih tinggi.
- Perlu firewall dan HTTPS.
- Perlu backup dan monitoring.
- Jangan langsung diberi akses akun penting.
- Browser automation bisa lebih rumit jika butuh GUI.
- File lokal laptop tidak otomatis tersedia di VPS.

### Contoh arsitektur VPS

```text
VPS
  -> OpenClaw
  -> 9Router
  -> Provider AI
```

Atau dipisah:

```text
VPS Automation
  -> OpenClaw untuk Telegram/Discord/GitHub

VPS AI Gateway
  -> 9Router untuk routing provider

Laptop
  -> OpenClaw lokal untuk coding
```

## Perbandingan Lokal vs VPS

| Kebutuhan | Lokal | VPS |
|---|---|---|
| Belajar awal | Sangat cocok | Bisa, tapi lebih berisiko |
| Coding project lokal | Sangat cocok | Kurang cocok kecuali repo disinkronkan |
| Browser lokal | Cocok | Bisa, tapi setup lebih rumit |
| Automation 24/7 | Kurang cocok | Sangat cocok |
| Telegram/Discord bot | Bisa | Lebih cocok |
| Webhook publik | Kurang cocok | Sangat cocok |
| Keamanan awal | Lebih mudah dikontrol | Perlu hardening |
| Akses file pribadi | Cocok jika dibatasi | Harus sangat hati-hati |
| Integrasi server | Bisa | Sangat cocok |

## Rekomendasi Arsitektur untuk Belajar

Untuk tahap belajar, gunakan pola berikut:

```text
Laptop:
  OpenClaw untuk coding, file lokal, dan browser lokal

VPS:
  9Router untuk routing model/provider

Provider AI:
  OpenAI / Anthropic / Gemini / OpenAI-compatible provider / local model
```

Setelah paham:

```text
Laptop:
  OpenClaw lokal untuk pekerjaan development

VPS:
  9Router sebagai AI gateway
  OpenClaw server untuk automation 24/7

Chat app:
  Telegram / Discord / Slack sebagai interface agent server
```

## Integrasi OpenClaw dengan 9Router

9Router cocok dipakai sebagai endpoint model AI untuk OpenClaw.

Konfigurasi umum:

```text
Base URL / Endpoint: https://9router.domainkamu.com/v1
API Key: ambil dari dashboard 9Router
Model: pilih model atau combo dari 9Router
```

Jika 9Router berjalan lokal:

```text
Base URL / Endpoint: http://localhost:20128/v1
```

Jika 9Router berjalan di VPS tanpa domain:

```text
Base URL / Endpoint: http://IP_VPS:20128/v1
```

Namun untuk akses dari luar server, lebih aman memakai domain dan HTTPS.

Manfaat integrasi dengan 9Router:

- routing model lebih fleksibel
- bisa memakai banyak provider
- bisa fallback saat provider error
- usage analytics lebih mudah dipantau
- quota tracking lebih terpusat
- biaya dan token lebih mudah dikontrol

## Cara Menggunakan OpenClaw Secara Bertahap

### Tahap 1: Eksperimen lokal

Mulai dengan tugas sederhana:

```text
Cek folder ini dan jelaskan struktur file-nya.
```

Lalu naikkan level:

```text
Baca README dan buat ringkasan cara menjalankan project.
```

Kemudian:

```text
Cari file konfigurasi environment dan jelaskan variable yang dibutuhkan.
```

### Tahap 2: Coding ringan

Berikan tugas yang risikonya kecil:

```text
Buat dokumentasi setup development dari isi project ini.
```

Atau:

```text
Cari TODO comment di project ini dan kelompokkan berdasarkan folder.
```

### Tahap 3: Tool access lebih luas

Setelah percaya dengan workflow, aktifkan tool tambahan:

- terminal
- browser
- integrasi GitHub
- integrasi email testing
- plugin/skill tertentu

Tetap gunakan prinsip permission minimal.

### Tahap 4: Automation server

Jika sudah stabil, pindahkan workflow tertentu ke VPS:

- reminder harian
- monitoring deploy
- ringkasan issue GitHub
- Telegram bot internal
- Discord assistant tim

## Instalasi OpenClaw di Lokal

Bagian ini menjelaskan instalasi untuk laptop atau komputer pribadi. Ini adalah jalur paling aman untuk belajar karena OpenClaw tidak langsung terbuka ke internet.

### 1. Syarat sistem

Rekomendasi runtime dari OpenClaw:

- Node.js 24, atau minimal Node.js 22.19+
- npm, pnpm, atau bun
- terminal: zsh, bash, PowerShell, atau WSL2
- koneksi internet untuk install package dan akses model AI

Cek versi Node dan npm:

```bash
node --version
npm --version
```

Jika Node belum sesuai, gunakan `nvm` agar mudah mengganti versi:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Buka terminal baru, lalu install Node:

```bash
nvm install 24
nvm use 24
node --version
```

### 2. Install OpenClaw

Install OpenClaw global:

```bash
npm install -g openclaw@latest
```

Alternatif dengan pnpm:

```bash
pnpm add -g openclaw@latest
pnpm approve-builds -g
```

Alternatif dengan bun:

```bash
bun add -g openclaw@latest
```

Untuk pemula, npm biasanya paling mudah.

### 3. Jalankan onboarding

Jalankan:

```bash
openclaw onboard --install-daemon
```

Onboarding biasanya membantu menyiapkan:

- konfigurasi awal
- provider/model AI
- Gateway daemon
- permission dasar
- workspace agent
- channel komunikasi jika diperlukan

Opsi `--install-daemon` membuat OpenClaw Gateway berjalan sebagai service user, misalnya LaunchAgent di macOS atau systemd user service di Linux.

### 4. Verifikasi instalasi

Cek CLI:

```bash
openclaw --version
```

Cek konfigurasi:

```bash
openclaw doctor
```

Cek status Gateway:

```bash
openclaw gateway status
```

Jika ingin menjalankan Gateway manual:

```bash
openclaw gateway --port 18789 --verbose
```

Port default Gateway OpenClaw adalah `18789`.

### 5. Lokasi workspace dan konfigurasi

Secara umum, workspace OpenClaw berada di:

```text
~/.openclaw/workspace
```

File prompt yang penting:

```text
~/.openclaw/workspace/AGENTS.md
~/.openclaw/workspace/SOUL.md
~/.openclaw/workspace/TOOLS.md
```

Fungsinya:

- `AGENTS.md`: menjelaskan peran agent.
- `SOUL.md`: mengatur karakter, preferensi, dan prinsip agent.
- `TOOLS.md`: menjelaskan tool yang boleh dipakai dan batasannya.

Konfigurasi utama biasanya berada di:

```text
~/.openclaw/openclaw.json
```

File ini bisa dipakai untuk mengatur model, provider, default agent, dan konfigurasi runtime.

### 6. Test tugas sederhana

Mulai dengan task yang aman:

```text
Cek workspace ini dan jelaskan file penting yang tersedia.
```

Lalu coba:

```text
Buat ringkasan isi AGENTS.md, SOUL.md, dan TOOLS.md.
```

Untuk coding:

```text
Baca README project ini, lalu buat checklist cara menjalankan project.
```

## Konfigurasi OpenClaw dengan 9Router

9Router bisa menjadi OpenAI-compatible provider untuk OpenClaw. Ini berguna jika kita ingin routing model, fallback provider, quota tracking, dan analytics dikelola dari satu tempat.

### 1. Siapkan 9Router

Pastikan 9Router sudah berjalan.

Jika lokal:

```text
http://localhost:20128
```

Jika VPS dengan domain:

```text
https://9router.domainkamu.com
```

Endpoint OpenAI-compatible:

```text
https://9router.domainkamu.com/v1
```

### 2. Tambahkan provider custom di OpenClaw

Konfigurasi OpenClaw untuk provider custom biasanya memakai format `models.providers`.

Contoh konsep konfigurasi di `~/.openclaw/openclaw.json`:

```js
{
  agents: {
    defaults: {
      model: {
        primary: "nine-router/mimo-v2.5-pro",
      },
    },
  },
  models: {
    providers: {
      "nine-router": {
        baseUrl: "https://9router.domainkamu.com/v1",
        apiKey: "${NINE_ROUTER_API_KEY}",
        api: "openai-completions",
        timeoutSeconds: 300,
        models: [
          {
            id: "mimo-v2.5-pro",
            name: "MiMo via 9Router",
            reasoning: false,
            input: ["text"],
            contextWindow: 200000,
            maxTokens: 8192,
          },
        ],
      },
    },
  },
}
```

Catatan:

- `nine-router` adalah nama provider custom. Bisa diganti, misalnya `9router`, `naltech-router`, atau `ai-gateway`.
- `mimo-v2.5-pro` harus disesuaikan dengan model atau combo yang tersedia di 9Router.
- Gunakan environment variable untuk API key, jangan hardcode di file konfigurasi.
- `api: "openai-completions"` dipakai untuk endpoint OpenAI-compatible.
- `baseUrl` untuk 9Router menggunakan `/v1`.

### 3. Simpan API key di environment variable

Tambahkan ke shell profile, misalnya `~/.zshrc`:

```bash
export NINE_ROUTER_API_KEY="isi_api_key_9router"
```

Reload shell:

```bash
source ~/.zshrc
```

Cek:

```bash
echo $NINE_ROUTER_API_KEY
```

Jangan commit file yang berisi API key.

### 4. Restart Gateway setelah config berubah

Setelah mengubah konfigurasi:

```bash
openclaw gateway restart
openclaw doctor
openclaw gateway status
```

Jika model tidak muncul atau masih memakai model lama, coba:

```bash
openclaw models list
openclaw models set nine-router/mimo-v2.5-pro
```

### 5. Test koneksi model

Kirim task sederhana:

```text
Jawab singkat: kamu sekarang memakai model dari provider apa?
```

Lalu cek di dashboard 9Router:

- apakah request masuk
- model apa yang dipakai
- token input/output
- apakah ada error provider

## Instalasi OpenClaw di VPS

OpenClaw di VPS cocok untuk automation yang harus online terus, seperti bot Telegram, Discord assistant, GitHub webhook, monitoring server, atau ringkasan rutin.

Untuk awal, jangan beri akses terlalu luas. Jalankan sebagai user biasa, bukan root.

### 1. Siapkan VPS

Rekomendasi:

- Ubuntu 22.04 atau 24.04
- RAM minimal 2 GB
- storage minimal 20 GB
- user non-root dengan akses sudo
- domain jika ingin akses dari luar

Update server:

```bash
sudo apt update
sudo apt upgrade -y
```

Install paket dasar:

```bash
sudo apt install -y curl git ca-certificates ufw
```

### 2. Buat user khusus

Buat user khusus agar OpenClaw tidak berjalan sebagai root:

```bash
sudo adduser openclaw
sudo usermod -aG sudo openclaw
```

Login sebagai user tersebut:

```bash
su - openclaw
```

### 3. Install Node dengan nvm

Install nvm:

```bash
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.40.3/install.sh | bash
```

Logout/login ulang atau jalankan:

```bash
source ~/.bashrc
```

Install Node:

```bash
nvm install 24
nvm use 24
node --version
npm --version
```

### 4. Install OpenClaw di VPS

```bash
npm install -g openclaw@latest
openclaw onboard --install-daemon
```

Cek:

```bash
openclaw --version
openclaw doctor
openclaw gateway status
```

### 5. Systemd user service

Jika `openclaw onboard --install-daemon` berhasil, Gateway akan dipasang sebagai service user.

Cek service user:

```bash
systemctl --user status openclaw
```

Jika service belum aktif:

```bash
systemctl --user enable --now openclaw
```

Agar service user tetap berjalan walaupun user tidak sedang login:

```bash
loginctl enable-linger openclaw
```

Perintah `loginctl enable-linger` dijalankan dari user yang punya sudo/root permission.

### 6. Firewall VPS

Untuk setup aman, jangan expose Gateway OpenClaw langsung ke publik.

Izinkan SSH:

```bash
sudo ufw allow OpenSSH
```

Jika memakai reverse proxy HTTPS:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

Jangan buka port `18789` ke publik kecuali benar-benar paham risikonya.

### 7. Reverse proxy untuk akses dashboard

Jika OpenClaw punya dashboard/control UI yang perlu diakses dari luar, gunakan Nginx atau Caddy dengan HTTPS.

Contoh Nginx:

```nginx
server {
    listen 80;
    server_name openclaw.example.com;

    location / {
        proxy_pass http://127.0.0.1:18789;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

Gunakan HTTPS dengan Certbot:

```bash
sudo apt install -y nginx certbot python3-certbot-nginx
sudo certbot --nginx -d openclaw.example.com
```

Untuk keamanan, lebih baik dashboard tidak dibuka publik tanpa autentikasi tambahan.

### 8. Integrasi OpenClaw VPS dengan 9Router VPS

Jika OpenClaw dan 9Router berada di VPS yang sama:

```text
OpenClaw -> http://127.0.0.1:20128/v1 -> 9Router -> Provider AI
```

Contoh `baseUrl`:

```js
baseUrl: "http://127.0.0.1:20128/v1"
```

Jika 9Router berada di server lain:

```text
OpenClaw VPS -> https://9router.domainkamu.com/v1 -> Provider AI
```

Gunakan HTTPS jika melewati internet publik.

### 9. Backup OpenClaw

Backup folder konfigurasi dan workspace:

```bash
tar -czf openclaw-backup-$(date +%F).tar.gz ~/.openclaw
```

Restore:

```bash
tar -xzf openclaw-backup-YYYY-MM-DD.tar.gz -C ~
openclaw gateway restart
```

Simpan backup di tempat lain, bukan hanya di VPS yang sama.

### 10. Update OpenClaw

Update package:

```bash
npm install -g openclaw@latest
openclaw gateway restart
openclaw doctor
```

OpenClaw juga menyediakan channel update:

```bash
openclaw update --channel stable
```

Gunakan channel `stable` untuk server produksi. Channel beta/dev lebih cocok untuk testing.

### 11. Troubleshooting VPS

Jika command `openclaw` tidak ditemukan:

```bash
node -v
npm prefix -g
echo $PATH
```

Tambahkan global npm bin ke PATH jika perlu:

```bash
export PATH="$(npm prefix -g)/bin:$PATH"
```

Jika Gateway tidak berjalan:

```bash
openclaw gateway status
openclaw doctor
systemctl --user status openclaw
```

Jika port bentrok:

```bash
sudo lsof -i :18789
```

Jika request model gagal:

- cek API key
- cek `baseUrl`
- cek nama model
- cek dashboard 9Router
- jalankan `openclaw doctor`
- restart Gateway

## Contoh Setup Produksi yang Aman

Untuk belajar banyak orang, arsitektur aman yang disarankan:

```text
Laptop developer:
  OpenClaw lokal untuk coding dan file project

VPS:
  9Router untuk model gateway
  OpenClaw server hanya untuk automation 24/7

Public internet:
  hanya expose HTTPS reverse proxy
  jangan expose port internal langsung
```

Port internal:

```text
9Router: 20128
OpenClaw Gateway: 18789
```

Yang boleh dibuka ke publik:

```text
80/tcp
443/tcp
22/tcp hanya untuk SSH, lebih baik dibatasi IP
```

Yang sebaiknya tidak dibuka langsung:

```text
20128/tcp
18789/tcp
```

## Checklist Setelah Instalasi

Checklist lokal:

- Node sudah versi 24 atau minimal 22.19+.
- `openclaw --version` berjalan.
- `openclaw doctor` tidak menunjukkan error serius.
- Gateway berjalan.
- Model provider sudah tersambung.
- Task sederhana berhasil dijalankan.
- Permission folder masih terbatas.

Checklist VPS:

- OpenClaw berjalan sebagai user biasa, bukan root.
- Firewall aktif.
- Port `18789` tidak terbuka langsung ke publik.
- Reverse proxy memakai HTTPS jika perlu akses luar.
- API key disimpan di environment variable.
- Backup `~/.openclaw` tersedia.
- Log dan status Gateway bisa dicek.
- 9Router menerima request jika dipakai sebagai provider.

## Studi Kasus 1: OpenClaw untuk Dokumentasi Project

Studi kasus ini cocok untuk belajar karena risikonya rendah, tetapi manfaatnya langsung terasa. OpenClaw diminta membaca project, memahami struktur, lalu membuat dokumentasi developer.

### Tujuan

Membuat dokumentasi project yang berisi:

- gambaran umum project
- cara install dependency
- cara menjalankan development server
- struktur folder
- file penting
- environment variable
- command build/test
- catatan troubleshooting

### Setup awal

Gunakan project dummy atau project yang tidak berisi data sensitif.

Contoh batasan:

```text
Kamu hanya boleh membaca folder project ini.
Jangan mengubah file sebelum meminta persetujuan.
Jangan menjalankan command yang menghapus file.
Jika perlu menjalankan command, jelaskan dulu tujuannya.
```

### Prompt awal

```text
Baca project ini sebagai developer baru.
Tolong jelaskan:
1. project ini dibuat untuk apa
2. teknologi utama yang dipakai
3. struktur folder penting
4. cara menjalankan project secara lokal
5. file konfigurasi yang perlu diperhatikan
6. risiko setup yang mungkin membingungkan developer baru

Jangan edit file dulu. Berikan laporan ringkas dan jelas.
```

### Prompt lanjutan

Jika laporan awal sudah benar:

```text
Buat draft dokumentasi README untuk project ini.
Strukturnya:
- Overview
- Requirements
- Installation
- Environment Variables
- Development
- Build
- Testing
- Troubleshooting

Jangan menulis API key atau secret.
Jika ada informasi yang belum pasti, beri label "perlu dicek".
```

### Prompt eksekusi

Jika ingin OpenClaw menulis file:

```text
Tulis draft dokumentasi tadi ke file docs/setup-development.md.
Jangan mengubah file lain.
Setelah selesai, tampilkan ringkasan perubahan.
```

### Verifikasi manual

Setelah file dibuat, cek:

- Apakah command install benar?
- Apakah nama package sesuai?
- Apakah environment variable tidak membocorkan secret?
- Apakah instruksi bisa dijalankan developer baru?
- Apakah ada asumsi yang perlu diperbaiki?

## Studi Kasus 2: OpenClaw untuk Monitoring Server

Studi kasus ini cocok jika OpenClaw dijalankan di VPS atau server internal.

### Tujuan

OpenClaw membantu mengecek kondisi server dan membuat ringkasan:

- status service
- pemakaian disk
- pemakaian memory
- error log terbaru
- rekomendasi tindakan

### Prompt aman

```text
Cek kondisi server ini dengan command non-destruktif.
Boleh menjalankan:
- uptime
- df -h
- free -h
- systemctl status untuk service yang relevan
- tail log maksimal 100 baris

Jangan restart service.
Jangan menghapus file.
Jangan mengubah konfigurasi.

Buat laporan ringkas: kondisi umum, masalah yang ditemukan, dan rekomendasi langkah berikutnya.
```

### Command yang biasanya aman

```bash
uptime
df -h
free -h
systemctl status nginx
systemctl status docker
journalctl -u nginx -n 100 --no-pager
```

### Output yang diharapkan

```text
Status server:
- CPU load normal
- Disk / hampir penuh 87%
- Nginx aktif
- Docker aktif
- Ada error 502 di log Nginx dalam 1 jam terakhir

Rekomendasi:
1. cek upstream app
2. cek container app
3. bersihkan log lama jika disk terus naik
```

## Studi Kasus 3: OpenClaw untuk Research Teknis

Studi kasus ini cocok untuk membandingkan tools atau membuat keputusan teknis.

### Tujuan

OpenClaw membantu membuat perbandingan beberapa opsi.

Contoh:

```text
Bandingkan 9Router, LiteLLM, OpenRouter, dan OpenClaw untuk kebutuhan AI workflow NalTech.
```

### Prompt research

```text
Tolong buat riset teknis tentang pilihan AI gateway dan AI agent untuk tim kecil.

Bandingkan:
- 9Router
- LiteLLM
- OpenRouter
- OpenClaw

Untuk setiap tool, jelaskan:
1. fungsi utama
2. kapan cocok dipakai
3. kelebihan
4. kekurangan
5. risiko keamanan
6. apakah cocok untuk NalTech

Buat kesimpulan arsitektur yang paling masuk akal untuk tahap belajar dan tahap produksi.
```

### Format hasil yang bagus

```text
Ringkasan keputusan:
- Untuk routing model: 9Router
- Untuk agent lokal: OpenClaw lokal
- Untuk coding: Codex/OpenCode/OpenClaw sesuai kebutuhan
- Untuk automation 24/7: OpenClaw VPS

Alasan:
...
```

## Prompt Siap Pakai

Bagian ini berisi prompt yang bisa langsung dipakai atau dimodifikasi.

### Prompt memahami project

```text
Baca project ini sebagai senior developer.
Jelaskan tujuan project, stack teknologi, struktur folder, alur utama aplikasi, dan command penting.
Jangan edit file.
Jika ada hal yang belum pasti, tulis sebagai asumsi.
```

### Prompt membuat dokumentasi

```text
Buat dokumentasi developer untuk project ini.
Fokus pada cara setup lokal, env variable, menjalankan project, build, test, dan troubleshooting.
Jangan tulis secret atau API key.
Simpan sebagai draft terlebih dahulu dan minta konfirmasi sebelum mengubah file.
```

### Prompt review keamanan

```text
Review project ini dari sisi keamanan dasar.
Cari potensi masalah seperti hardcoded secret, file env yang ikut commit, permission terlalu luas, dependency mencurigakan, dan endpoint tanpa proteksi.
Jangan ubah file.
Berikan findings dengan prioritas tinggi, sedang, rendah.
```

### Prompt debugging

```text
Saya mengalami error berikut:

[paste error di sini]

Tolong:
1. jelaskan arti error
2. cari kemungkinan penyebab
3. cek file yang relevan
4. berikan opsi perbaikan paling aman
5. jangan edit file sebelum saya setujui
```

### Prompt menjalankan test

```text
Jalankan test project ini dengan command yang sesuai.
Jika test gagal, jelaskan penyebabnya berdasarkan output.
Jangan mengubah source code dulu.
Berikan rekomendasi fix.
```

### Prompt membuat changelog

```text
Baca perubahan git saat ini.
Buat changelog singkat dalam bahasa Indonesia:
- fitur baru
- perbaikan
- perubahan teknis
- catatan migrasi jika ada

Jangan commit.
```

### Prompt membuat issue GitHub

```text
Berdasarkan error/log berikut, buat draft issue GitHub.
Format:
- Judul
- Ringkasan masalah
- Langkah reproduksi
- Expected behavior
- Actual behavior
- Log relevan
- Kemungkinan penyebab
```

### Prompt monitoring server

```text
Cek kondisi server dengan command non-destruktif.
Jangan restart, hapus, atau ubah konfigurasi.
Buat laporan status CPU, memory, disk, service penting, dan error log terbaru.
```

### Prompt ringkasan meeting

```text
Baca catatan meeting berikut.
Buat:
- ringkasan singkat
- keputusan penting
- action items
- siapa bertanggung jawab
- deadline jika disebutkan
- pertanyaan yang masih terbuka
```

### Prompt data CSV

```text
Baca file CSV ini.
Tolong jelaskan kolom yang tersedia, jumlah baris, data kosong, data duplikat, dan insight awal.
Jangan ubah file asli.
Jika perlu membuat output, buat file baru.
```

## Template AGENTS.md

`AGENTS.md` dipakai untuk menjelaskan peran agent dan cara agent bekerja di workspace.

Contoh template:

```md
# Agent Role

Kamu adalah AI development assistant untuk project ini.
Tugas utama kamu adalah membantu membaca kode, menjelaskan alur, membuat dokumentasi, debugging, dan memberi saran perbaikan.

## Prinsip Kerja

- Baca konteks project sebelum memberi kesimpulan.
- Jangan mengubah file tanpa instruksi eksplisit.
- Jangan menjalankan command destruktif.
- Jika perlu menjalankan command, jelaskan tujuannya.
- Prioritaskan solusi sederhana dan sesuai struktur project.
- Jangan menulis API key, token, password, atau secret ke dokumentasi.

## Batasan

- Jangan akses folder di luar workspace kecuali diminta.
- Jangan melakukan deploy tanpa persetujuan.
- Jangan install dependency baru tanpa menjelaskan alasannya.
- Jangan commit perubahan tanpa instruksi.

## Output

Saat memberi laporan, gunakan format:

- Ringkasan
- Temuan penting
- Rekomendasi
- Langkah berikutnya
```

## Template SOUL.md

`SOUL.md` bisa dipakai untuk mengatur gaya komunikasi, preferensi, dan kebiasaan kerja agent.

Contoh template:

```md
# Agent Style

Gunakan bahasa Indonesia yang jelas, praktis, dan ramah.
Jelaskan hal teknis dengan contoh sederhana.
Jika ada risiko, sebutkan secara langsung.

## Preferensi

- Jawaban singkat untuk pertanyaan sederhana.
- Penjelasan bertahap untuk konsep baru.
- Gunakan checklist untuk tutorial.
- Gunakan tabel untuk perbandingan.
- Beri contoh command jika relevan.

## Cara Mengambil Keputusan

- Pilih pendekatan yang aman terlebih dahulu.
- Untuk project existing, ikuti pola yang sudah ada.
- Jika ada beberapa opsi, jelaskan trade-off.
- Jika informasi belum pasti, tulis sebagai asumsi.

## Hal yang Dihindari

- Jangan terlalu percaya diri jika belum memeriksa file.
- Jangan menyarankan command berbahaya tanpa alasan kuat.
- Jangan membocorkan secret.
- Jangan membuat perubahan besar tanpa rencana.
```

## Template TOOLS.md

`TOOLS.md` dipakai untuk mengatur tool yang boleh digunakan agent dan aturan penggunaannya.

Contoh template:

```md
# Tool Policy

Agent boleh memakai tool untuk membaca file, mencari teks, menjalankan command non-destruktif, dan membuat dokumentasi.

## Tool yang Diizinkan

- Membaca file di workspace.
- Mencari teks dengan ripgrep.
- Melihat status git.
- Menjalankan command build/test/lint.
- Membuat file dokumentasi baru jika diminta.

## Tool yang Perlu Konfirmasi

- Install dependency baru.
- Mengubah konfigurasi deployment.
- Menjalankan migration database.
- Restart service.
- Mengubah permission file.
- Mengakses folder di luar workspace.

## Tool yang Dilarang Tanpa Izin Eksplisit

- Menghapus file atau folder.
- Reset git history.
- Force push.
- Menghapus database.
- Mengirim email/message ke pihak luar.
- Deploy ke production.
- Membuka secret atau credential yang tidak diperlukan.

## Aturan Command

Sebelum menjalankan command, pastikan:

1. command sesuai tujuan
2. command tidak destruktif
3. output diperlukan untuk menyelesaikan tugas
4. user memahami risiko jika command berisiko
```

## Template Workflow Tim

Jika OpenClaw dipakai untuk tim kecil, buat aturan kerja yang jelas.

Contoh:

```md
# OpenClaw Team Workflow

## Tujuan

OpenClaw dipakai untuk membantu dokumentasi, debugging, research teknis, dan automation ringan.

## Channel

- Discord: diskusi dan request ringan.
- GitHub: issue, PR review, dan changelog.
- VPS: automation terjadwal dan monitoring.

## Agent

- Local Agent: dipakai developer di laptop masing-masing.
- Server Agent: dipakai untuk automation 24/7.
- Documentation Agent: fokus membuat dan merapikan dokumentasi.

## Aturan

- Perubahan kode harus direview manusia.
- Agent tidak boleh deploy production tanpa approval.
- Secret tidak boleh dikirim ke chat.
- Semua automation penting harus punya log.
- Semua workflow baru diuji di environment staging.
```

## Arsitektur NalTech AI Stack

Arsitektur yang disarankan untuk tahap belajar:

```text
Laptop developer
  -> OpenClaw lokal
  -> Codex / OpenCode untuk coding
  -> browser lokal

VPS
  -> 9Router sebagai AI gateway

Provider AI
  -> OpenAI / Anthropic / Gemini / MiMo / provider lain
```

Arsitektur untuk tahap produksi ringan:

```text
Developer laptop
  -> OpenClaw lokal untuk coding dan file project
  -> 9Router VPS untuk routing model

VPS automation
  -> OpenClaw server untuk workflow 24/7
  -> Telegram/Discord/GitHub webhook

VPS AI gateway
  -> 9Router
  -> quota tracking
  -> usage analytics
  -> fallback provider

Provider AI
  -> cloud model
  -> local model jika tersedia
```

Prinsip arsitektur:

- Agent lokal untuk pekerjaan yang butuh akses file pribadi.
- Agent VPS untuk automation yang harus online terus.
- 9Router untuk routing model dan monitoring token.
- Jangan expose port internal langsung ke publik.
- Semua akses publik lewat HTTPS.
- Human review tetap wajib untuk perubahan penting.

## OpenClaw vs Tools Lain

OpenClaw sering terlihat mirip dengan beberapa tool AI lain, tetapi perannya berbeda. Bagian ini membantu menentukan kapan memakai OpenClaw dan kapan memakai tool lain.

| Tool | Fungsi Utama | Cocok Untuk | Kurang Cocok Untuk |
|---|---|---|---|
| OpenClaw | Personal AI agent dan automation runtime | assistant lokal, workflow automation, integrasi chat app, tool orchestration | routing provider AI murni |
| Codex | Coding agent di workspace/repository | membaca codebase, edit file, menjalankan test, refactor, debugging | automation 24/7 lintas aplikasi |
| Claude Code | Coding agent berbasis Claude | coding, refactor, reasoning code, task terminal | workflow personal assistant non-coding |
| OpenCode | Coding agent/open-source terminal assistant | coding lokal, eksperimen agent coding, integrasi model custom | automation server jangka panjang |
| 9Router | AI gateway/router untuk provider model | routing model, fallback provider, quota tracking, usage analytics | menjalankan aksi file/browser/terminal |
| n8n | Workflow automation visual | integrasi API, trigger, webhook, automation bisnis | reasoning agent kompleks tanpa custom logic |
| LangChain/LangGraph | Framework membangun aplikasi agent | membangun agent custom, multi-step graph, product AI | pengguna non-developer yang ingin langsung pakai |
| Ollama | Menjalankan local model | eksperimen model lokal, privacy, offline/local inference | orchestration agent lengkap |

### Kapan memakai OpenClaw

Gunakan OpenClaw jika kebutuhan utamanya:

- agent yang bisa memakai tool
- menjalankan workflow dari chat/CLI
- automation yang butuh reasoning
- akses file, browser, terminal, API, atau aplikasi
- personal assistant yang bisa dikustomisasi
- workflow yang bisa berkembang menjadi multi-agent

Contoh:

```text
Saya ingin agent yang bisa membaca project, menjalankan test, membuat ringkasan, lalu mengirim laporan ke Discord.
```

### Kapan memakai Codex atau Claude Code

Gunakan Codex atau Claude Code jika fokusnya coding dalam repository:

- memahami codebase
- memperbaiki bug
- menulis test
- refactor
- review perubahan
- menjalankan command development

Contoh:

```text
Saya ingin agent memperbaiki bug di repo ini dan menjalankan test sampai lulus.
```

### Kapan memakai 9Router

Gunakan 9Router jika masalah utamanya ada di model/provider:

- ingin satu endpoint untuk banyak provider
- ingin fallback model
- ingin analytics token
- ingin quota tracking
- ingin memakai model berbeda untuk task berbeda

Contoh:

```text
Saya ingin semua tool AI memakai endpoint yang sama, tetapi routing model dan biaya dipantau dari dashboard.
```

### Kapan memakai n8n

Gunakan n8n jika workflow lebih deterministik dan berbasis trigger:

- saat form masuk, kirim email
- saat webhook GitHub masuk, buat tiket
- setiap pagi ambil data spreadsheet dan kirim laporan

OpenClaw lebih cocok jika workflow butuh reasoning fleksibel, sedangkan n8n lebih cocok jika workflow sudah jelas dan berulang.

### Kapan memakai LangChain atau LangGraph

Gunakan LangChain/LangGraph jika ingin membangun aplikasi agent sendiri sebagai produk atau sistem custom.

Contoh:

```text
Saya ingin membuat aplikasi customer support AI dengan state machine, memory, retrieval, dan workflow approval.
```

OpenClaw lebih cocok untuk langsung dipakai sebagai agent, sedangkan LangChain/LangGraph lebih cocok sebagai framework development.

## Security Hardening VPS

Jika OpenClaw dijalankan di VPS, keamanan harus disiapkan sejak awal. Agent yang punya akses terminal, file, browser, API, atau chat app bisa berbahaya jika server terbuka tanpa proteksi.

### 1. Gunakan user non-root

Jangan jalankan OpenClaw sebagai root.

```bash
sudo adduser openclaw
sudo usermod -aG sudo openclaw
```

Login sebagai user tersebut:

```bash
su - openclaw
```

### 2. Gunakan SSH key-only

Di laptop lokal, buat SSH key jika belum ada:

```bash
ssh-keygen -t ed25519 -C "openclaw-vps"
```

Copy public key ke VPS:

```bash
ssh-copy-id openclaw@IP_VPS
```

Test login:

```bash
ssh openclaw@IP_VPS
```

### 3. Disable root login dan password login

Edit konfigurasi SSH:

```bash
sudo nano /etc/ssh/sshd_config
```

Pastikan konfigurasi berikut:

```text
PermitRootLogin no
PasswordAuthentication no
PubkeyAuthentication yes
```

Restart SSH:

```bash
sudo systemctl restart ssh
```

Sebelum menutup terminal lama, buka terminal baru dan pastikan login SSH key berhasil.

### 4. Aktifkan firewall UFW

Izinkan SSH:

```bash
sudo ufw allow OpenSSH
```

Jika memakai reverse proxy:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Aktifkan:

```bash
sudo ufw enable
sudo ufw status verbose
```

Jangan expose port internal:

```text
18789/tcp untuk OpenClaw Gateway
20128/tcp untuk 9Router
```

Kedua port itu sebaiknya hanya bind ke `127.0.0.1` jika dipakai bersama reverse proxy.

### 5. Pasang fail2ban

Fail2ban membantu memblokir percobaan login yang mencurigakan.

```bash
sudo apt install -y fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
sudo fail2ban-client status
```

### 6. Gunakan reverse proxy dengan HTTPS

Jika dashboard atau endpoint harus diakses dari luar, gunakan domain dan HTTPS.

Contoh:

```text
https://openclaw.example.com
https://9router.example.com
```

Jangan akses dashboard melalui HTTP publik.

### 7. Tambahkan basic auth untuk dashboard internal

Jika dashboard belum punya proteksi yang cukup, tambahkan basic auth di Nginx.

Install tool:

```bash
sudo apt install -y apache2-utils
```

Buat user password:

```bash
sudo htpasswd -c /etc/nginx/.htpasswd-openclaw admin
```

Tambahkan ke blok `location /` Nginx:

```nginx
auth_basic "Restricted";
auth_basic_user_file /etc/nginx/.htpasswd-openclaw;
```

Reload Nginx:

```bash
sudo nginx -t
sudo systemctl reload nginx
```

### 8. Batasi akses berdasarkan IP jika memungkinkan

Jika hanya dipakai dari IP tertentu, batasi akses di Nginx:

```nginx
allow 203.0.113.10;
deny all;
```

Ini lebih aman daripada membuka dashboard ke seluruh internet.

### 9. Simpan secret di environment variable

Jangan simpan API key di file dokumentasi atau repository.

Contoh:

```bash
export NINE_ROUTER_API_KEY="isi_api_key"
export OPENAI_API_KEY="isi_api_key"
```

Untuk service systemd, secret bisa disimpan di environment file dengan permission ketat:

```bash
sudo nano /etc/openclaw.env
sudo chmod 600 /etc/openclaw.env
```

### 10. Backup otomatis

Buat folder backup:

```bash
mkdir -p ~/backups
```

Script backup sederhana:

```bash
nano ~/backup-openclaw.sh
```

Isi:

```bash
#!/usr/bin/env bash
set -euo pipefail

BACKUP_DIR="$HOME/backups"
DATE="$(date +%F)"

mkdir -p "$BACKUP_DIR"
tar -czf "$BACKUP_DIR/openclaw-$DATE.tar.gz" "$HOME/.openclaw"
```

Aktifkan:

```bash
chmod +x ~/backup-openclaw.sh
```

Jalankan manual:

```bash
~/backup-openclaw.sh
```

Tambahkan cron harian:

```bash
crontab -e
```

Isi:

```text
0 2 * * * /home/openclaw/backup-openclaw.sh
```

Simpan backup ke storage eksternal jika memungkinkan.

### 11. Rotasi API key

Rotasi API key secara berkala:

- buat key baru di provider
- update environment variable
- restart OpenClaw Gateway
- cek request berjalan
- revoke key lama

Contoh:

```bash
openclaw gateway restart
openclaw doctor
```

### 12. Update rutin

Update package server:

```bash
sudo apt update
sudo apt upgrade -y
```

Update OpenClaw:

```bash
npm install -g openclaw@latest
openclaw gateway restart
openclaw doctor
```

Update 9Router jika memakai Docker:

```bash
cd /opt/9router
docker compose pull
docker compose up -d
```

## Permission Matrix

Permission matrix membantu menentukan aksi mana yang boleh otomatis, harus konfirmasi, atau dilarang. Ini penting agar OpenClaw tidak diberi akses terlalu luas.

### Prinsip dasar

Gunakan prinsip **least privilege**:

```text
Berikan akses terkecil yang cukup untuk menyelesaikan tugas.
```

Jika sebuah tool tidak dibutuhkan, jangan aktifkan.

### Matrix umum

| Area | Boleh Otomatis | Harus Konfirmasi | Dilarang Tanpa Izin Eksplisit |
|---|---|---|---|
| File lokal | baca file workspace, buat draft dokumen | edit source code, pindah file | hapus folder, ubah file di luar workspace |
| Terminal | `ls`, `pwd`, `rg`, `git status`, test/lint | install dependency, migration, restart service | `rm -rf`, reset git, force push |
| Git | lihat diff/status/log | commit, push, buat branch | force push, rewrite history |
| Browser | buka halaman, ambil data publik | login, isi form, submit data | transaksi, payment, ubah akun |
| Email | baca email testing, buat draft | kirim email, arsip massal | hapus email, kirim ke banyak orang |
| GitHub | baca issue/PR, buat draft issue | komentar PR, label issue, buka PR | merge PR, delete branch, release production |
| Server VPS | cek status, baca log terbatas | restart service, update package | hapus data, ubah firewall tanpa review |
| Database | baca schema, query read-only | migration, update data | drop table, truncate, delete massal |
| 9Router | baca analytics, cek provider | ubah provider, ubah routing | hapus provider, expose key |
| OpenClaw config | baca config, validasi config | ubah model/default agent | membagikan secret, membuka akses global |

### Permission untuk lokal

Untuk OpenClaw lokal tahap belajar:

| Aksi | Status |
|---|---|
| Membaca folder project dummy | Boleh otomatis |
| Membuat dokumentasi baru | Boleh jika diminta |
| Mengedit source code | Harus konfirmasi |
| Menjalankan test/lint | Boleh otomatis jika non-destruktif |
| Install dependency | Harus konfirmasi |
| Membaca home directory penuh | Hindari |
| Menghapus file | Dilarang tanpa izin eksplisit |

### Permission untuk VPS

Untuk OpenClaw di VPS:

| Aksi | Status |
|---|---|
| Cek uptime/disk/memory | Boleh otomatis |
| Baca log maksimal 100-300 baris | Boleh otomatis |
| Restart service | Harus konfirmasi |
| Update package | Harus konfirmasi |
| Ubah firewall | Harus konfirmasi |
| Buka port publik | Harus konfirmasi kuat |
| Hapus data/log/database | Dilarang tanpa izin eksplisit |
| Deploy production | Harus approval manusia |

### Permission untuk chat app

Jika OpenClaw terhubung ke Telegram, Discord, atau Slack:

| Aksi | Status |
|---|---|
| Membaca pesan channel khusus bot | Boleh otomatis |
| Menjawab di thread internal | Boleh jika channel memang untuk bot |
| Mengirim DM ke user | Harus konfirmasi |
| Mention banyak orang | Harus konfirmasi |
| Mengirim file/log sensitif | Dilarang tanpa izin eksplisit |
| Mengirim secret/API key | Dilarang |

### Permission untuk email

Email adalah area sensitif.

| Aksi | Status |
|---|---|
| Membaca email testing | Boleh otomatis |
| Membuat draft email | Boleh otomatis |
| Mengirim email | Harus konfirmasi |
| Forward email | Harus konfirmasi |
| Menghapus email | Dilarang tanpa izin eksplisit |
| Membaca email pribadi penuh | Hindari |

### Prompt permission policy

Masukkan aturan ini ke `TOOLS.md` atau prompt agent:

```text
Sebelum menjalankan aksi yang mengubah sistem, kamu harus meminta konfirmasi.

Aksi yang wajib konfirmasi:
- mengedit source code
- install dependency
- restart service
- migration database
- commit atau push git
- mengirim email/pesan
- mengubah firewall
- membuka port publik
- deploy

Aksi yang dilarang tanpa izin eksplisit:
- menghapus file/folder
- reset git history
- force push
- drop/truncate database
- membagikan API key/secret
- melakukan transaksi/payment
```

## Checklist Keamanan

Karena OpenClaw bisa menjalankan aksi nyata, keamanan harus dianggap serius.

Checklist awal:

- Jalankan lokal dulu untuk belajar.
- Jangan langsung hubungkan akun utama.
- Gunakan folder project khusus untuk eksperimen.
- Jangan beri akses seluruh home directory jika tidak perlu.
- Review command sebelum dieksekusi otomatis.
- Jangan izinkan command destruktif tanpa konfirmasi.
- Pisahkan environment testing dan production.
- Simpan API key di secret manager atau environment variable.
- Jangan commit API key ke repository.
- Gunakan firewall jika berjalan di VPS.
- Gunakan HTTPS untuk akses dari luar.
- Backup konfigurasi dan data penting.
- Audit plugin dan skill sebelum dipakai.

## Contoh Workflow Belajar

Gunakan urutan ini agar aman dan bertahap:

```text
1. Install OpenClaw di lokal.
2. Hubungkan ke model AI atau 9Router.
3. Beri akses ke satu folder project dummy.
4. Minta OpenClaw membaca struktur folder.
5. Minta OpenClaw membuat dokumentasi sederhana.
6. Izinkan command non-destruktif seperti test atau lint.
7. Review hasil perubahan.
8. Baru coba integrasi browser atau GitHub.
9. Setelah stabil, buat workflow automation kecil.
10. Jika butuh 24/7, deploy workflow tertentu ke VPS.
```

## Kesalahan Umum

Beberapa kesalahan yang perlu dihindari:

- Langsung memberi akses terlalu luas.
- Menjalankan agent di VPS tanpa firewall.
- Menaruh API key di file yang ikut commit.
- Mengaktifkan automation tanpa log dan monitoring.
- Membiarkan agent menjalankan command berisiko tanpa konfirmasi.
- Menghubungkan email utama sebelum memahami permission.
- Tidak punya backup data atau konfigurasi.

## Kesimpulan

OpenClaw adalah tool yang cocok untuk membangun AI agent yang bisa bekerja secara nyata. Ia bisa menjadi coding worker, automation assistant, research helper, browser operator, support helper, atau orchestrator untuk beberapa agent.

Untuk belajar, pilihan paling aman adalah menjalankan OpenClaw di lokal terlebih dahulu. Setelah workflow jelas dan permission sudah dipahami, OpenClaw bisa dipindahkan ke VPS untuk kebutuhan automation 24/7.

Kombinasi yang paling masuk akal:

```text
OpenClaw lokal
  -> untuk coding, file lokal, browser lokal

9Router di VPS
  -> untuk routing model, fallback, analytics, quota

OpenClaw di VPS
  -> hanya untuk automation yang memang harus online terus
```

Dengan pendekatan bertahap, OpenClaw bisa dipelajari dengan aman sekaligus tetap berguna untuk workflow nyata.

## Referensi

- [OpenClaw official site](https://openclaw.ai/)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [OpenClaw About](https://openclawlab.com/en/about/)
- [9Router GitHub](https://github.com/decolua/9router)
