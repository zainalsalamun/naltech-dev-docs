---
title: "9Router Proxy"
description: "Catatan fungsi 9Router sebagai proxy, router, dan dashboard monitoring untuk penggunaan API model AI."
category: "AI Tools"
level: "Intermediate"
order: 80
tags: ["ai", "proxy", "router", "llm", "api", "monitoring"]
updated: "2026-05-22"
---

# 9Router Proxy

9Router adalah tool yang berfungsi sebagai **proxy dan router untuk API model AI**. Tool ini menjadi lapisan tengah antara aplikasi atau CLI yang kita pakai dengan provider AI yang menjadi tujuan request.

Dengan pola ini, aplikasi tidak harus langsung terhubung ke masing-masing provider. Aplikasi cukup mengirim request ke 9Router, lalu 9Router yang mengatur request tersebut akan diteruskan ke provider atau model yang sesuai.

## Fungsi Utama

### 1. Endpoint proxy

9Router menyediakan endpoint pusat yang bisa dipakai oleh aplikasi AI, coding agent, atau CLI tool. Endpoint ini menerima request dari client, lalu meneruskannya ke provider model AI yang sudah dikonfigurasi.

Contoh alur sederhana:

```text
OpenCode / CLI / Aplikasi
  -> 9Router Proxy
  -> Provider AI / Model AI
```

### 2. Provider manager

9Router dapat dipakai untuk mengelola banyak provider AI dari satu dashboard. Provider ini bisa berupa layanan berbayar, layanan gratis, endpoint OpenAI-compatible, atau provider custom.

Manfaatnya:

- API key dan endpoint lebih terpusat.
- Lebih mudah mengganti provider tanpa mengubah konfigurasi di banyak aplikasi.
- Bisa membandingkan performa beberapa model atau provider.

### 3. Model routing

9Router dapat mengarahkan request ke model atau provider tertentu. Misalnya satu client diarahkan ke model coding, sementara client lain diarahkan ke model yang lebih murah untuk chat ringan.

Contoh penggunaan:

- Coding agent memakai model yang kuat untuk reasoning.
- Chat ringan memakai model yang lebih hemat.
- Request tertentu diarahkan ke provider cadangan jika provider utama gagal.

### 4. Combo

Menu `Combos` kemungkinan dipakai untuk membuat kombinasi routing. Combo bisa berguna untuk menyimpan konfigurasi tertentu, misalnya gabungan client, provider, model, fallback, atau profil penggunaan.

Contoh ide combo:

- `Coding Hemat`: model murah untuk tugas ringan.
- `Coding Serius`: model lebih kuat untuk refactor atau debugging berat.
- `Fallback Chain`: provider utama lalu provider cadangan.

### 5. Usage analytics

9Router menyediakan halaman analytics untuk memantau penggunaan API. Dari dashboard, kita bisa melihat:

- Total request.
- Total input token.
- Total output token.
- Estimasi biaya.
- Riwayat request per model.

Fitur ini penting untuk membaca pola penggunaan dan menghindari pemakaian token yang tidak terkontrol.

### 6. Quota tracker

Quota tracker dipakai untuk memantau batas penggunaan provider atau model. Fitur ini membantu kita mengetahui apakah penggunaan sudah mendekati limit harian, bulanan, atau limit dari provider tertentu.

### 7. Proxy pools

Proxy pools kemungkinan dipakai untuk mengelola kumpulan proxy jaringan. Ini berguna ketika traffic perlu diarahkan melalui jalur jaringan tertentu, dibagi ke beberapa proxy, atau disesuaikan dengan kebutuhan provider.

### 8. MITM dan debugging

Menu `MITM` mengarah ke fitur inspeksi request dan response. Fitur ini berguna untuk debugging:

- Header request.
- Payload yang dikirim ke provider.
- Response dari model.
- Error format API.
- Masalah autentikasi.

### 9. Media providers

Menu `Media Providers` kemungkinan dipakai untuk provider yang tidak hanya berbasis chat teks, misalnya image generation, audio, video, atau layanan media lain.

### 10. Skills

Menu `Skills` bisa dikembangkan sebagai sistem kemampuan tambahan. Misalnya transformasi request, custom routing logic, preset prompt, filter keamanan, atau integrasi workflow tertentu.

### 11. CLI tools

CLI tools menunjukkan 9Router bisa diintegrasikan dengan terminal atau tool development. Ini cocok untuk coding agent, aplikasi command line, atau workflow lokal yang membutuhkan API AI.

### 12. Console log

Console log dipakai untuk melihat aktivitas runtime, error provider, request yang gagal, atau status service. Bagian ini penting saat melakukan troubleshooting.

## Kapan 9Router Berguna

9Router paling berguna ketika kita:

- Menggunakan banyak provider AI.
- Ingin satu endpoint pusat untuk semua tool AI.
- Perlu memantau token dan estimasi biaya.
- Ingin fallback otomatis saat provider error.
- Ingin debugging request dan response API.
- Ingin memisahkan model untuk kebutuhan berbeda.
- Ingin menjaga konfigurasi API key tetap rapi.

## Cara Install 9Router di VPS

Bagian ini menggunakan pendekatan yang cocok untuk server produksi kecil: 9Router dijalankan di VPS, data disimpan persistent, lalu akses dashboard diamankan lewat firewall atau reverse proxy.

Sumber resmi:

- Website: [https://9router.com](https://9router.com)
- GitHub: [https://github.com/decolua/9router](https://github.com/decolua/9router)
- Dokumentasi Docker: [https://github.com/decolua/9router/blob/master/DOCKER.md](https://github.com/decolua/9router/blob/master/DOCKER.md)

### 1. Siapkan VPS

Rekomendasi awal:

- Ubuntu 22.04 atau 24.04.
- RAM minimal 1 GB, lebih nyaman 2 GB.
- Storage minimal 10 GB.
- Domain atau subdomain jika ingin akses lewat HTTPS.
- Akses SSH dengan user yang punya izin `sudo`.

Update package server:

```bash
sudo apt update
sudo apt upgrade -y
```

Install utility dasar:

```bash
sudo apt install -y curl ca-certificates gnupg ufw
```

### 2. Install Docker

Install Docker menggunakan script resmi:

```bash
curl -fsSL https://get.docker.com | sudo sh
```

Aktifkan Docker saat boot:

```bash
sudo systemctl enable docker
sudo systemctl start docker
```

Opsional, agar user saat ini bisa menjalankan Docker tanpa `sudo`:

```bash
sudo usermod -aG docker $USER
```

Setelah menjalankan command di atas, logout dari SSH lalu login ulang.

Cek Docker:

```bash
docker --version
docker ps
```

### 3. Jalankan 9Router dengan Docker

Buat folder untuk data 9Router:

```bash
sudo mkdir -p /opt/9router/data
sudo chown -R $USER:$USER /opt/9router
```

Jalankan container:

```bash
docker run -d \
  --name 9router \
  --restart unless-stopped \
  -p 20128:20128 \
  -v /opt/9router/data:/app/data \
  -e DATA_DIR=/app/data \
  -e PORT=20128 \
  -e HOSTNAME=0.0.0.0 \
  decolua/9router:latest
```

Cek apakah container berjalan:

```bash
docker ps
docker logs -f 9router
```

Jika sukses, dashboard bisa dibuka dari browser:

```text
http://IP_VPS:20128
```

URL penting:

```text
Dashboard: http://IP_VPS:20128/dashboard
OpenAI-compatible API: http://IP_VPS:20128/v1
```

### 4. Alternatif rapi dengan Docker Compose

Untuk VPS, Docker Compose lebih nyaman karena konfigurasi container disimpan dalam file.

Buat folder project:

```bash
mkdir -p /opt/9router
cd /opt/9router
```

Buat file `docker-compose.yml`:

```bash
nano docker-compose.yml
```

Isi file:

```yaml
services:
  9router:
    image: decolua/9router:latest
    container_name: 9router
    restart: unless-stopped
    ports:
      - "20128:20128"
    environment:
      DATA_DIR: /app/data
      PORT: 20128
      HOSTNAME: 0.0.0.0
    volumes:
      - ./data:/app/data
```

Jalankan:

```bash
docker compose up -d
docker compose logs -f
```

Jika nanti ingin memakai reverse proxy Nginx dan tidak ingin port 9Router terbuka langsung ke publik, ubah bagian `ports` menjadi:

```yaml
ports:
  - "127.0.0.1:20128:20128"
```

Dengan cara ini, 9Router hanya bisa diakses dari dalam VPS melalui `127.0.0.1`.

### 5. Amankan akses dengan firewall

Jika dashboard hanya dipakai pribadi, jangan buka terlalu banyak port.

Izinkan SSH:

```bash
sudo ufw allow OpenSSH
```

Jika ingin akses langsung ke dashboard lewat port `20128`:

```bash
sudo ufw allow 20128/tcp
sudo ufw enable
sudo ufw status
```

Untuk setup yang lebih aman, jangan buka port `20128` ke publik. Gunakan reverse proxy seperti Nginx atau Caddy, lalu buka hanya port `80` dan `443`.

### 6. Setup reverse proxy dengan Nginx

Install Nginx:

```bash
sudo apt install -y nginx
```

Buat konfigurasi site:

```bash
sudo nano /etc/nginx/sites-available/9router
```

Isi konfigurasi:

```nginx
server {
    listen 80;
    server_name 9router.example.com;

    location / {
        proxy_pass http://127.0.0.1:20128;
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

Ganti `9router.example.com` dengan domain atau subdomain sendiri.

Aktifkan site:

```bash
sudo ln -s /etc/nginx/sites-available/9router /etc/nginx/sites-enabled/9router
sudo nginx -t
sudo systemctl reload nginx
```

Atur firewall untuk web:

```bash
sudo ufw allow 'Nginx Full'
sudo ufw status
```

### 7. Pasang HTTPS dengan Certbot

Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

Generate SSL:

```bash
sudo certbot --nginx -d 9router.example.com
```

Cek auto-renew:

```bash
sudo certbot renew --dry-run
```

Setelah ini dashboard bisa diakses melalui:

```text
https://9router.example.com
```

### 8. Hubungkan client ke 9Router

Setelah dashboard aktif, tambahkan provider di menu `Providers`, lalu ambil endpoint dan API key dari dashboard.

Konfigurasi umum untuk tool yang mendukung OpenAI-compatible API:

```text
Base URL / Endpoint: https://9router.example.com/v1
API Key: ambil dari dashboard 9Router
Model: pilih model atau combo yang sudah dibuat di 9Router
```

Jika akses langsung tanpa domain:

```text
Base URL / Endpoint: http://IP_VPS:20128/v1
API Key: ambil dari dashboard 9Router
```

Gunakan HTTPS jika endpoint dipakai dari luar VPS, terutama karena request bisa membawa API key dan isi prompt.

### 9. Backup data 9Router

Data 9Router disimpan di folder yang dipasang ke container. Dalam contoh ini:

```text
/opt/9router/data
```

Di dalam data tersebut biasanya terdapat database SQLite, backup, sertifikat, log, dan konfigurasi runtime.

Buat backup manual:

```bash
cd /opt/9router
tar -czf 9router-backup-$(date +%F).tar.gz data
```

Restore backup:

```bash
cd /opt/9router
docker stop 9router
tar -xzf 9router-backup-YYYY-MM-DD.tar.gz
docker start 9router
```

Simpan backup di tempat lain, misalnya object storage, server backup, atau local machine.

### 10. Update 9Router

Untuk update Docker image:

```bash
docker pull decolua/9router:latest
docker stop 9router
docker rm 9router
docker run -d \
  --name 9router \
  --restart unless-stopped \
  -p 20128:20128 \
  -v /opt/9router/data:/app/data \
  -e DATA_DIR=/app/data \
  -e PORT=20128 \
  -e HOSTNAME=0.0.0.0 \
  decolua/9router:latest
```

Karena data disimpan di `/opt/9router/data`, konfigurasi dan database tidak hilang saat container diganti.

Jika memakai Docker Compose:

```bash
cd /opt/9router
docker compose pull
docker compose up -d
docker compose logs -f
```

### 11. Alternatif install via npm

Jika tidak ingin memakai Docker, 9Router juga bisa dijalankan dari npm:

```bash
npm install -g 9router
9router
```

Untuk VPS produksi, jalankan dengan process manager seperti `systemd` atau `pm2` agar service tetap hidup setelah SSH ditutup atau server reboot.

Contoh dengan `pm2`:

```bash
npm install -g pm2
pm2 start 9router --name 9router
pm2 save
pm2 startup
```

Namun untuk server yang ingin mudah di-backup dan mudah di-update, Docker biasanya lebih rapi.

### 12. Checklist keamanan VPS

Sebelum dipakai rutin, pastikan:

- Jangan expose port `20128` langsung ke publik jika tidak perlu.
- Gunakan Nginx/Caddy + HTTPS untuk akses dari luar.
- Simpan API key dashboard dan provider dengan aman.
- Batasi akses dashboard hanya untuk user yang dipercaya.
- Aktifkan firewall dan hanya buka port yang diperlukan.
- Backup folder data secara berkala.
- Update image 9Router secara teratur.
- Jangan menaruh API key provider di dokumentasi publik.
- Jika memungkinkan, pakai domain khusus seperti `ai-gateway.example.com`.

### 13. Checklist setelah install

Setelah 9Router berjalan di VPS, lakukan pengecekan berikut:

- Dashboard bisa dibuka dari browser.
- Provider AI sudah ditambahkan.
- Endpoint proxy sudah dicatat.
- API key atau token dashboard tidak dibagikan publik.
- Firewall hanya membuka port yang diperlukan.
- Jika memakai domain, HTTPS sudah aktif.
- Data 9Router tersimpan di volume persistent.
- Log container tidak menunjukkan error berulang.

### 14. Troubleshooting

Jika dashboard tidak bisa dibuka, cek container:

```bash
docker ps
docker logs 9router
```

Jika port bentrok:

```bash
sudo lsof -i :20128
```

Jika Nginx error:

```bash
sudo nginx -t
sudo systemctl status nginx
```

Jika domain belum mengarah ke VPS, cek DNS record `A` domain sudah mengarah ke IP VPS.

## Arah Pengembangan yang Disarankan

Beberapa ide pengembangan yang paling bermanfaat:

1. **Fallback otomatis**

   Jika provider utama error, rate limit, atau lambat, request otomatis dialihkan ke provider cadangan.

2. **Cost control**

   Tambahkan limit harian, limit per provider, limit per project, dan notifikasi jika token melonjak.

3. **Routing rule**

   Buat aturan routing berdasarkan kebutuhan. Contoh: request coding diarahkan ke model kuat, chat ringan ke model hemat, dan request media ke provider media.

4. **Request replay**

   Dari log request, sediakan tombol untuk menjalankan ulang request yang sama. Ini akan sangat membantu saat debugging prompt atau payload API.

5. **Dashboard per client**

   Pisahkan analytics berdasarkan client seperti OpenCode, custom app, CLI tool, atau project tertentu.

6. **Privacy filter**

   Tambahkan filter sebelum request keluar ke provider. Contohnya menyamarkan API key, email, token rahasia, path file sensitif, atau data pribadi.

7. **Integrasi local model**

   Hubungkan 9Router dengan local model seperti Ollama atau LM Studio, sehingga routing bisa mencampur provider cloud dan model lokal.

8. **Export analytics**

   Sediakan export CSV atau JSON untuk audit penggunaan, laporan biaya, dan evaluasi performa model.

## Kesimpulan

9Router sebaiknya diposisikan sebagai **AI gateway pribadi**. Nilai utamanya bukan hanya meneruskan request, tetapi mengatur routing, memantau penggunaan, mengontrol biaya, membantu debugging, dan menyatukan banyak provider AI dalam satu tempat.
