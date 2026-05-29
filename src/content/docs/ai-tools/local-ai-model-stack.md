---
title: "Local AI Model Stack"
description: "Panduan memakai model AI lokal dengan Ollama, LM Studio, llama.cpp, Open WebUI, dan integrasi ke 9Router, OpenCode, serta OpenClaw."
category: "AI Tools"
level: "Intermediate"
order: 115
tags: ["ai", "local-model", "ollama", "lm-studio", "llama.cpp", "open-webui", "9router"]
updated: "2026-05-23"
---

# Local AI Model Stack

Local AI Model Stack adalah setup untuk menjalankan model AI di komputer sendiri atau server sendiri, bukan selalu memakai cloud provider.

Contoh local stack:

```text
Laptop / mini PC / VPS GPU
  -> Ollama / LM Studio / llama.cpp
  -> endpoint OpenAI-compatible
  -> 9Router
  -> OpenCode / OpenClaw / automation
```

Tujuannya:

- mengurangi ketergantungan ke cloud
- menjaga data lebih private
- eksperimen model open-source
- mengurangi biaya token cloud untuk task ringan
- punya fallback saat provider cloud error

## Kapan Pakai Local Model?

Local model cocok jika:

- task tidak terlalu berat
- data lebih sensitif
- ingin eksperimen offline
- ingin menghemat biaya cloud
- ingin menjalankan model open-source
- ingin latency lokal untuk task kecil

Local model kurang cocok jika:

- butuh reasoning sangat kuat
- codebase sangat besar
- hardware terbatas
- butuh uptime production tinggi
- butuh kualitas model cloud premium
- butuh context sangat panjang

Prinsip:

```text
Local model untuk task ringan/privat.
Cloud model untuk reasoning berat dan kualitas tinggi.
```

## Komponen Utama

| Tool | Fungsi | Cocok Untuk |
|---|---|---|
| Ollama | menjalankan local model dengan CLI/API | local model sederhana, server lokal, integrasi tool |
| LM Studio | desktop app dan local server | eksplorasi model dengan UI |
| llama.cpp | runtime ringan berbasis GGUF | advanced user, server custom, performa CPU/GPU |
| Open WebUI | web UI untuk model lokal/remote | chat UI, team/local dashboard |
| 9Router | routing antara local dan cloud | gateway gabungan local + cloud |

## Ollama

Ollama adalah tool populer untuk menjalankan model lokal.

Kelebihan:

- mudah install
- CLI sederhana
- banyak model tersedia
- berjalan lokal
- punya API
- mendukung OpenAI-compatible endpoint sebagian

Endpoint default:

```text
http://localhost:11434
```

OpenAI-compatible endpoint:

```text
http://localhost:11434/v1
```

Install:

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

Download model:

```bash
ollama pull qwen3:8b
```

Jalankan chat:

```bash
ollama run qwen3:8b
```

List model:

```bash
ollama list
```

Test OpenAI-compatible endpoint:

```bash
curl http://localhost:11434/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "qwen3:8b",
    "messages": [
      { "role": "user", "content": "Jelaskan apa itu local AI model dalam 3 bullet." }
    ]
  }'
```

## LM Studio

LM Studio adalah aplikasi desktop untuk menjalankan local model dengan UI.

Cocok untuk:

- mencoba model lokal tanpa banyak command
- download model dari UI
- chat lokal
- menjalankan local server
- testing model sebelum dipakai di automation

Kelebihan:

- UI ramah pemula
- mudah load/unload model
- punya server OpenAI-compatible
- cocok untuk Mac/Windows

Kekurangan:

- lebih cocok untuk desktop
- automation server lebih sering memakai Ollama/llama.cpp
- tetap bergantung RAM/VRAM

Pola pemakaian:

```text
LM Studio
  -> start local server
  -> endpoint OpenAI-compatible
  -> OpenCode/OpenClaw/9Router
```

Endpoint biasanya:

```text
http://localhost:1234/v1
```

## llama.cpp

llama.cpp adalah runtime model lokal yang sangat populer untuk model GGUF.

Cocok untuk:

- advanced user
- optimasi performa
- server custom
- CPU inference
- GPU acceleration jika tersedia
- deployment ringan

Kelebihan:

- fleksibel
- performa bagus untuk banyak hardware
- format GGUF luas digunakan
- bisa menjalankan server

Kekurangan:

- setup lebih teknis
- pemula lebih mudah mulai dari Ollama/LM Studio
- perlu memahami quantization dan parameter runtime

Pola:

```text
llama.cpp server
  -> endpoint lokal
  -> 9Router atau client OpenAI-compatible
```

## Open WebUI

Open WebUI adalah web UI untuk memakai model lokal atau remote.

Cocok untuk:

- UI chat lokal
- UI untuk Ollama
- team internal chat
- eksperimen prompt
- akses model dari browser

Arsitektur umum:

```text
Browser
  -> Open WebUI
  -> Ollama / OpenAI-compatible endpoint
```

Kapan dipakai:

```text
Jika ingin chat UI untuk model lokal tanpa membuat aplikasi sendiri.
```

## Integrasi Local Model ke 9Router

9Router bisa dipakai sebagai gateway yang menggabungkan local model dan cloud provider.

Arsitektur:

```text
OpenCode / OpenClaw / Codex
  -> 9Router
  -> Ollama local model
  -> Cloud provider fallback
```

Manfaat:

- satu endpoint untuk local dan cloud
- local model untuk task ringan
- cloud fallback untuk task berat
- usage analytics tetap terpusat
- routing bisa diatur dari dashboard

Contoh endpoint local model:

```text
Ollama: http://localhost:11434/v1
LM Studio: http://localhost:1234/v1
```

Jika 9Router berada di VPS dan Ollama berada di laptop, jangan expose Ollama langsung ke publik. Gunakan VPN, tunnel aman, atau jalankan Ollama di server yang sama.

## Integrasi dengan OpenCode

OpenCode bisa memakai provider OpenAI-compatible.

Contoh konsep provider Ollama di `opencode.json`:

```json
{
  "$schema": "https://opencode.ai/config.json",
  "provider": {
    "ollama": {
      "npm": "@ai-sdk/openai-compatible",
      "name": "Ollama",
      "options": {
        "baseURL": "http://localhost:11434/v1",
        "apiKey": "ollama"
      },
      "models": {
        "qwen3:8b": {
          "name": "Qwen3 8B Local",
          "limit": {
            "context": 32768,
            "output": 4096
          }
        }
      }
    }
  },
  "model": "ollama/qwen3:8b",
  "small_model": "ollama/qwen3:8b"
}
```

Untuk workflow NalTech, lebih rapi jika OpenCode tetap mengarah ke 9Router:

```text
OpenCode
  -> 9Router
  -> Ollama or cloud model
```

## Integrasi dengan OpenClaw

OpenClaw juga bisa memakai provider OpenAI-compatible.

Pola:

```text
OpenClaw lokal
  -> http://localhost:11434/v1
```

Atau:

```text
OpenClaw
  -> 9Router
  -> local/cloud model
```

Rekomendasi:

- untuk belajar local model: langsung ke Ollama
- untuk stack rapi: lewat 9Router
- untuk automation 24/7: jalankan local model di server yang sama atau jaringan privat

## Kebutuhan Hardware

Kebutuhan hardware tergantung ukuran model dan quantization.

Panduan kasar:

| Model | RAM/VRAM Minimum | Cocok Untuk |
|---|---|---|
| 1B-3B | 4-8 GB | chat ringan, klasifikasi, ringkasan sederhana |
| 7B-8B | 8-16 GB | chat umum, coding ringan, summarization |
| 13B-14B | 16-32 GB | reasoning lebih baik, coding menengah |
| 30B+ | 32 GB+ | task berat, butuh hardware kuat |
| 70B+ | 64 GB+ | kualitas tinggi, butuh GPU/RAM besar |

Untuk Mac Apple Silicon:

- RAM 16 GB: nyaman untuk 7B/8B quantized
- RAM 32 GB: lebih nyaman untuk 14B/30B kecil
- RAM 64 GB+: bisa eksperimen model besar

Untuk VPS CPU:

- bisa jalan, tetapi sering lambat
- cocok untuk model kecil
- kurang cocok untuk coding berat

Untuk VPS GPU:

- lebih cepat
- biaya server lebih tinggi
- cocok jika automation local model harus 24/7

## Memilih Model

Kategori task:

| Task | Model Lokal yang Cocok | Catatan |
|---|---|---|
| ringkasan pendek | 3B-8B | hemat dan cepat |
| klasifikasi | 1B-8B | cocok lokal |
| chat umum | 7B-14B | tergantung kualitas model |
| coding ringan | 7B-14B coding model | masih perlu review |
| refactor besar | cloud model kuat | local sering kurang stabil |
| security review | cloud model kuat | butuh reasoning tinggi |
| embedding | embedding model lokal | bisa untuk RAG lokal |

Prinsip:

```text
Local model untuk task murah, repeatable, dan low-risk.
Cloud model untuk reasoning mahal, kritis, dan kompleks.
```

## Cost dan Privacy

Kelebihan local:

- tidak bayar per token
- data tidak harus keluar ke cloud
- bisa offline
- cocok untuk eksperimen

Biaya local:

- listrik
- hardware
- waktu setup
- maintenance
- performa bisa lebih lambat

Kelebihan cloud:

- kualitas model tinggi
- tidak perlu hardware
- mudah scale
- model selalu update

Kekurangan cloud:

- bayar per token
- data keluar ke provider
- bergantung internet/provider
- perlu cost control

## Security

Jangan expose local model server langsung ke publik.

Risiko:

- orang lain memakai resource kamu
- prompt/data masuk tanpa kontrol
- local endpoint disalahgunakan
- tidak ada auth default di beberapa setup

Aturan:

```text
Bind local model ke localhost jika hanya dipakai lokal.
Gunakan VPN/tunnel aman jika perlu akses remote.
Gunakan reverse proxy auth jika benar-benar perlu expose.
Jangan expose Ollama/LM Studio ke internet publik tanpa proteksi.
```

## Troubleshooting

### Model lambat

Solusi:

- gunakan model lebih kecil
- gunakan quantization lebih rendah
- kurangi context
- tutup aplikasi berat
- gunakan GPU jika tersedia

### Out of memory

Solusi:

- pilih model lebih kecil
- gunakan quantized model
- kurangi context window
- restart runtime
- cek RAM/VRAM

### Endpoint tidak bisa diakses

Cek:

```bash
curl http://localhost:11434/api/tags
curl http://localhost:11434/v1/models
```

Jika dari Docker/container, `localhost` di container bukan host machine. Gunakan host networking atau alamat host yang sesuai.

### OpenCode/OpenClaw tidak cocok dengan model

Kemungkinan:

- model tidak cukup kuat untuk tool/coding
- endpoint tidak sepenuhnya kompatibel
- context terlalu kecil
- output format tidak stabil

Solusi:

- pakai model coding
- gunakan model lebih kuat
- lewatkan melalui 9Router
- gunakan cloud model untuk task sulit

### Response kosong atau error format

Cek:

- nama model benar
- endpoint memakai `/v1`
- model sudah di-pull/load
- server local model berjalan
- client memakai format OpenAI-compatible yang didukung

## Rekomendasi untuk NalTech

Tahap belajar:

```text
Laptop
  -> Ollama
  -> OpenCode/OpenClaw test langsung
```

Tahap stack rapi:

```text
OpenCode/OpenClaw/Codex
  -> 9Router
  -> Ollama local
  -> cloud provider fallback
```

Tahap automation:

```text
VPS automation
  -> OpenClaw
  -> 9Router
  -> local model kecil untuk report
  -> cloud model untuk task berat
```

Model lokal cocok untuk:

- daily report
- ringkasan pendek
- klasifikasi issue
- draft dokumentasi ringan
- eksperimen prompt

Cloud model tetap disarankan untuk:

- coding kompleks
- refactor besar
- security review
- debugging rumit
- arsitektur sistem

## Checklist Setup Local AI

- [ ] Pilih runtime: Ollama, LM Studio, atau llama.cpp.
- [ ] Install runtime.
- [ ] Pull/load model.
- [ ] Test chat lokal.
- [ ] Test endpoint OpenAI-compatible.
- [ ] Hubungkan ke OpenCode/OpenClaw.
- [ ] Hubungkan ke 9Router jika ingin routing.
- [ ] Jangan expose endpoint publik.
- [ ] Pilih model sesuai task.
- [ ] Pantau performa dan memory.
- [ ] Buat fallback ke cloud model untuk task berat.

## Kesimpulan

Local AI model melengkapi cloud AI. Bukan pengganti penuh, tetapi sangat berguna untuk task ringan, private, dan repeatable.

Pola terbaik:

```text
Local model
  -> task ringan, privat, murah

Cloud model
  -> task berat, reasoning kompleks

9Router
  -> routing antara local dan cloud
```

Dengan local AI model stack, NalTech bisa punya setup AI yang lebih fleksibel: hemat biaya, lebih privat, dan tetap bisa memakai cloud model saat benar-benar dibutuhkan.

## Referensi

- [Ollama OpenAI Compatibility](https://docs.ollama.com/api/openai-compatibility)
- [LM Studio OpenAI Compatibility](https://lmstudio.ai/docs/developer/openai-compat)
- [llama.cpp Server](https://github.com/ggml-org/llama.cpp/tree/master/tools/server)
- [Open WebUI Docs](https://docs.openwebui.com/)

