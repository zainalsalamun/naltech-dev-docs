---
title: "AI Gateway Comparison"
description: "Perbandingan 9Router, LiteLLM, OpenRouter, Helicone, Portkey, Langfuse, Ollama, dan LM Studio untuk routing model, observability, cost control, dan local AI."
category: "AI Tools"
level: "Intermediate"
order: 110
tags: ["ai", "gateway", "router", "observability", "litellm", "openrouter", "helicone", "portkey", "langfuse"]
updated: "2026-05-23"
---

# AI Gateway Comparison

AI Gateway adalah lapisan tengah antara aplikasi/agent dengan provider model AI.

Tanpa gateway:

```text
App/Agent
  -> langsung ke OpenAI/Anthropic/Gemini/provider lain
```

Dengan gateway:

```text
App/Agent
  -> AI Gateway
  -> provider/model yang dipilih
```

Gateway membantu mengatur:

- routing model
- fallback provider
- API key management
- cost tracking
- quota
- observability
- caching
- guardrails
- rate limiting
- akses ke banyak model melalui satu endpoint

## Istilah Penting

### Gateway

Gateway adalah pintu tengah untuk request AI. Aplikasi cukup memakai satu endpoint, lalu gateway mengatur request ke provider yang sesuai.

### Router

Router memilih model/provider berdasarkan aturan tertentu.

Contoh:

```text
Task ringan -> model murah
Task berat -> model kuat
Provider error -> fallback provider lain
```

### Proxy

Proxy meneruskan request dari client ke provider. Proxy bisa sederhana, atau bisa punya fitur tambahan seperti logging, auth, dan transformasi request.

### Aggregator

Aggregator menyediakan akses ke banyak provider/model melalui satu API key atau satu endpoint.

Contoh: OpenRouter.

### Observability

Observability membantu melihat apa yang terjadi dalam sistem AI:

- prompt
- response
- token
- latency
- cost
- error
- trace agent
- tool calls
- evaluation

Contoh: Helicone dan Langfuse.

## Tools yang Dibandingkan

| Tool | Fokus Utama | Cocok Untuk |
|---|---|---|
| 9Router | local/private AI gateway dan routing dashboard | personal AI stack, OpenClaw/OpenCode/Codex, VPS gateway |
| LiteLLM | proxy server OpenAI-compatible untuk banyak provider | app production, unified API, enterprise gateway |
| OpenRouter | aggregator model cloud | akses banyak model lewat satu API key |
| Helicone | AI gateway + observability | monitoring LLM app, request logging, cost/latency analytics |
| Portkey | AI gateway + guardrails + observability | production gateway, routing, retries, policy, guardrails |
| Langfuse | LLM observability, tracing, evals, prompt management | agent/app tracing, debugging, prompt iteration |
| Ollama | local model runtime | menjalankan model lokal di laptop/server |
| LM Studio | local model desktop/server | eksperimen local model dengan UI dan endpoint lokal |

## 9Router

9Router adalah gateway/proxy untuk mengatur provider AI, routing model, combo, quota, usage analytics, dan request log.

Cocok untuk:

- personal AI gateway
- routing model untuk Codex/OpenCode/OpenClaw
- monitoring token dari banyak tool
- VPS gateway pribadi
- eksperimen provider/model
- fallback sederhana

Kelebihan:

- dashboard praktis
- cocok untuk personal stack
- bisa dipakai sebagai endpoint OpenAI-compatible
- ada usage analytics dan request log
- mudah dipahami untuk workflow developer pribadi

Kekurangan:

- ekosistem enterprise belum seluas LiteLLM/Portkey/Langfuse
- perlu hardening jika dipasang di VPS
- fitur observability/evaluation tidak sedalam Langfuse

Kapan dipakai:

```text
Kamu ingin satu endpoint AI pribadi untuk OpenCode, OpenClaw, Codex, dan automation.
```

## LiteLLM

LiteLLM adalah proxy/gateway OpenAI-compatible untuk banyak provider model.

Cocok untuk:

- aplikasi production
- unified API untuk banyak provider
- rate limit
- budget
- key management
- model fallback
- logging
- enterprise gateway

Kelebihan:

- dukungan provider sangat luas
- OpenAI-compatible
- cocok untuk backend aplikasi
- banyak fitur production
- umum dipakai di stack LLM engineering

Kekurangan:

- setup bisa lebih teknis
- dashboard/operasional bisa lebih kompleks untuk pemula
- untuk personal use, bisa terasa terlalu besar

Kapan dipakai:

```text
Kamu membangun aplikasi AI production dan butuh gateway serius untuk banyak provider.
```

## OpenRouter

OpenRouter adalah aggregator model. Dengan satu API key dan endpoint, kita bisa mengakses banyak model dari berbagai provider.

Cocok untuk:

- mencoba banyak model cloud
- cepat berpindah model
- aplikasi yang butuh variasi model
- eksperimen benchmark
- developer yang tidak mau mengelola banyak provider key

Kelebihan:

- akses banyak model cepat
- API relatif OpenAI-compatible
- tidak perlu daftar ke banyak provider
- cocok untuk eksperimen model

Kekurangan:

- tetap bergantung pada platform pihak ketiga
- pricing dan availability mengikuti platform
- observability internal tidak sedalam Langfuse/Helicone
- beberapa fitur provider spesifik bisa berbeda

Kapan dipakai:

```text
Kamu ingin mencoba banyak model dari satu API tanpa mengelola banyak provider.
```

## Helicone

Helicone adalah AI Gateway dan LLM observability platform. Fokusnya membantu melihat request, token, cost, latency, error, dan analytics.

Cocok untuk:

- monitoring aplikasi AI
- observability request LLM
- cost tracking
- debugging latency/error
- gateway dengan logging otomatis

Kelebihan:

- observability kuat
- mudah melihat request dan cost
- gateway + analytics
- cocok untuk app yang sudah masuk tahap production

Kekurangan:

- fokusnya observability, bukan personal agent dashboard
- untuk self-host/production tetap butuh setup dan governance
- jika hanya butuh routing sederhana, bisa terasa berlebih

Kapan dipakai:

```text
Kamu punya aplikasi AI dan butuh monitoring request, latency, cost, dan debugging produksi.
```

## Portkey

Portkey adalah AI gateway dengan fokus production: routing, retries, guardrails, observability, caching, dan policy.

Cocok untuk:

- aplikasi AI production
- enterprise gateway
- guardrails
- routing dan retry kompleks
- policy enforcement
- observability

Kelebihan:

- fitur gateway production lengkap
- guardrails dan policy lebih kuat
- cocok untuk tim yang butuh kontrol serius
- mendukung banyak model/provider

Kekurangan:

- bisa terlalu besar untuk personal learning
- perlu memahami konfigurasi gateway
- kompleksitas lebih tinggi dibanding gateway sederhana

Kapan dipakai:

```text
Kamu membangun aplikasi AI untuk user nyata dan butuh guardrails, retries, policy, dan observability.
```

## Langfuse

Langfuse bukan sekadar gateway. Fokus utamanya adalah LLM observability, tracing, prompt management, evals, datasets, dan debugging agent/app AI.

Cocok untuk:

- tracing agent
- melihat tool call
- prompt management
- evaluation
- experiment tracking
- debugging aplikasi AI kompleks
- memahami chain/RAG/agent behavior

Kelebihan:

- tracing sangat berguna untuk agent
- prompt management dan evals
- cocok untuk LLM app engineering
- open source dan bisa self-host

Kekurangan:

- bukan pengganti gateway routing sederhana
- perlu instrumentasi aplikasi
- lebih cocok untuk app/agent yang sudah punya workflow kompleks

Kapan dipakai:

```text
Kamu ingin melihat detail alur agent: prompt, response, tool call, retrieval, latency, dan evaluasi kualitas.
```

## Ollama

Ollama adalah runtime untuk menjalankan model lokal. Ollama juga menyediakan endpoint yang kompatibel dengan sebagian OpenAI API.

Cocok untuk:

- local model
- eksperimen offline
- privacy
- model kecil/menengah di laptop/server
- integrasi local AI ke tool yang mendukung OpenAI-compatible endpoint

Kelebihan:

- berjalan lokal
- data tidak harus keluar ke cloud
- mudah mencoba model open-source
- bisa dipakai untuk task ringan

Kekurangan:

- kualitas tergantung model dan hardware
- model lokal bisa lebih lambat
- context dan reasoning bisa kalah dari cloud model kuat
- perlu RAM/VRAM cukup

Kapan dipakai:

```text
Kamu ingin menjalankan model lokal untuk privacy, eksperimen, atau task ringan tanpa biaya token cloud.
```

## LM Studio

LM Studio adalah tool desktop/server untuk menjalankan local model dengan UI dan endpoint lokal OpenAI-compatible.

Cocok untuk:

- eksplorasi model lokal
- developer yang ingin UI sederhana
- local inference
- testing model sebelum dipakai di automation

Kelebihan:

- UI ramah pemula
- mudah load model lokal
- menyediakan server lokal
- cocok untuk eksperimen

Kekurangan:

- lebih desktop-oriented
- untuk server production, Ollama/llama.cpp kadang lebih fleksibel
- tetap bergantung hardware

Kapan dipakai:

```text
Kamu ingin mencoba local model dengan UI dan endpoint lokal tanpa setup rumit.
```

## Perbandingan Fitur

| Fitur | 9Router | LiteLLM | OpenRouter | Helicone | Portkey | Langfuse | Ollama/LM Studio |
|---|---|---|---|---|---|---|---|
| OpenAI-compatible endpoint | Ya | Ya | Ya | Ya | Ya | Bukan fokus utama | Ya/sebagian |
| Routing model | Ya | Ya | Ya | Ya | Ya | Tidak utama | Lokal saja |
| Banyak provider | Ya | Sangat kuat | Sangat kuat | Ya | Sangat kuat | Integrasi observability | Local model |
| Usage analytics | Ya | Ya | Ya | Kuat | Kuat | Kuat untuk traces | Terbatas |
| Cost tracking | Ya | Ya | Ya | Kuat | Kuat | Bisa melalui traces | Tidak utama |
| Fallback/retry | Bisa | Kuat | Tergantung platform | Ada gateway | Kuat | Tidak utama | Tidak utama |
| Guardrails | Terbatas | Ada/tergantung setup | Terbatas | Terbatas | Kuat | Eval/tracing | Tidak utama |
| Agent tracing | Terbatas | Integrasi | Terbatas | Observability | Observability | Kuat | Tidak |
| Prompt management | Tidak utama | Tidak utama | Tidak utama | Terbatas | Ada fitur terkait | Kuat | Tidak |
| Local model | Via provider/local endpoint | Bisa | Cloud aggregator | Tidak utama | Bisa integrasi | Observability | Fokus utama |
| Cocok untuk personal stack | Sangat cocok | Bisa | Bisa | Bisa | Bisa, tapi berat | Bisa, jika butuh tracing | Cocok untuk lokal |
| Cocok untuk production app | Bisa, perlu hardening | Sangat cocok | Bisa | Sangat cocok | Sangat cocok | Sangat cocok untuk observability | Terbatas/tergantung setup |

## Kriteria Memilih AI Gateway

Pertanyaan yang harus dijawab:

1. Apakah butuh banyak provider?
2. Apakah butuh satu API key atau tetap BYOK?
3. Apakah butuh self-host?
4. Apakah butuh observability detail?
5. Apakah butuh guardrails?
6. Apakah butuh fallback/retry kompleks?
7. Apakah dipakai personal, tim kecil, atau production app?
8. Apakah butuh local model?
9. Apakah budget harus dipantau ketat?
10. Apakah agent perlu tracing tool call?

## Rekomendasi Berdasarkan Kebutuhan

### Personal AI stack

Rekomendasi:

```text
9Router
  -> routing model
  -> analytics
  -> endpoint untuk OpenCode/OpenClaw/Codex
```

Tambahkan Ollama/LM Studio jika ingin local model.

### Tim kecil

Rekomendasi:

```text
9Router atau LiteLLM
  -> gateway

Langfuse atau Helicone
  -> observability jika workflow mulai kompleks
```

### Aplikasi production

Rekomendasi:

```text
LiteLLM / Portkey / Helicone
  -> gateway production

Langfuse
  -> tracing, prompt management, evals
```

### Eksperimen banyak model

Rekomendasi:

```text
OpenRouter
  -> akses banyak model cepat
```

### Local/private AI

Rekomendasi:

```text
Ollama atau LM Studio
  -> local model endpoint

9Router
  -> routing antara local dan cloud
```

## Arsitektur Kombinasi

### NalTech personal stack

```text
OpenCode / OpenClaw / Codex
  -> 9Router
  -> Provider cloud / local model
```

### NalTech dengan local model

```text
OpenCode / OpenClaw
  -> 9Router
  -> Ollama / LM Studio
  -> Cloud provider fallback
```

### Production app dengan observability

```text
App backend
  -> LiteLLM / Portkey / Helicone Gateway
  -> Provider AI
  -> Langfuse traces/evals
```

### Agent workflow dengan tracing

```text
OpenClaw / custom agent
  -> 9Router or LiteLLM
  -> Provider AI
  -> Langfuse tracing
```

## Rekomendasi untuk NalTech

Untuk tahap sekarang:

```text
9Router sebagai gateway utama.
OpenClaw untuk automation.
OpenCode/Codex untuk coding.
Ollama/LM Studio untuk eksperimen local model.
```

Alasan:

- setup lebih mudah
- cocok untuk personal developer stack
- dashboard 9Router sudah cukup untuk usage/token
- bisa naik bertahap ke local model dan automation

Jika nanti workflow makin serius:

```text
Tambah Langfuse untuk tracing agent.
Pertimbangkan LiteLLM/Portkey jika butuh gateway production lebih kompleks.
Gunakan Helicone jika observability request dan cost jadi prioritas utama.
```

## Checklist Memilih Gateway

- [ ] Butuh self-host atau boleh SaaS?
- [ ] Butuh banyak provider?
- [ ] Butuh local model?
- [ ] Butuh fallback otomatis?
- [ ] Butuh quota/budget?
- [ ] Butuh tracing agent?
- [ ] Butuh guardrails?
- [ ] Butuh prompt management?
- [ ] Targetnya personal, tim kecil, atau production?
- [ ] Siapa yang akan mengelola API key?
- [ ] Bagaimana backup dan security-nya?

## Kesimpulan

Tidak ada satu gateway yang paling benar untuk semua kebutuhan.

Ringkasan keputusan:

```text
Personal AI gateway:
  -> 9Router

Production gateway:
  -> LiteLLM / Portkey / Helicone

Model aggregator:
  -> OpenRouter

Tracing dan evals:
  -> Langfuse

Local model:
  -> Ollama / LM Studio
```

Untuk NalTech, jalur paling realistis:

```text
Mulai dengan 9Router
  -> hubungkan OpenCode/OpenClaw/Codex
  -> pantau token dan biaya
  -> tambah local model
  -> tambah observability jika workflow makin besar
```

## Referensi

- [LiteLLM Docs](https://docs.litellm.ai/)
- [OpenRouter Docs](https://openrouter.ai/docs/api-reference/overview)
- [Helicone Docs](https://docs.helicone.ai/getting-started/platform-overview)
- [Portkey AI Gateway Docs](https://portkey.ai/docs/product/ai-gateway)
- [Langfuse Observability Docs](https://langfuse.com/docs/observability/overview/)
- [Ollama OpenAI Compatibility](https://docs.ollama.com/api/openai-compatibility)

