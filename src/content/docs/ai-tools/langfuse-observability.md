---
title: "Langfuse Observability"
description: "Panduan memahami Langfuse untuk LLM observability, tracing, prompt management, datasets, experiments, evals, dan integrasi dengan RAG, agent, automation, serta 9Router."
category: "AI Tools"
level: "Advanced"
order: 135
tags: ["ai", "observability", "langfuse", "tracing", "evals", "prompt-management", "llmops"]
updated: "2026-05-23"
---

# Langfuse Observability

Langfuse adalah platform **LLM observability** dan **LLM engineering**. Tool ini membantu kita melihat, menganalisis, mengevaluasi, dan memperbaiki aplikasi atau agent berbasis AI.

Jika 9Router membantu routing model dan monitoring token, Langfuse membantu menjawab pertanyaan seperti:

- prompt apa yang dikirim?
- model apa yang dipakai?
- output apa yang dihasilkan?
- tool call apa yang terjadi?
- berapa latency?
- berapa cost?
- trace mana yang gagal?
- versi prompt mana yang lebih baik?
- apakah jawaban RAG sesuai sumber?

## Posisi Langfuse dalam AI Stack

Arsitektur sederhana:

```text
App / Agent / Automation
  -> 9Router
  -> Provider AI

App / Agent / Automation
  -> Langfuse
  -> traces, scores, datasets, experiments
```

Peran:

```text
9Router = routing model dan usage gateway
Langfuse = tracing, observability, evals, prompt management
```

## Kapan Perlu Langfuse?

Gunakan Langfuse jika:

- workflow AI mulai kompleks
- ada RAG/knowledge base
- ada agent dengan tool call
- perlu melihat trace request
- perlu membandingkan prompt/model
- perlu evaluasi kualitas
- perlu debugging production
- ingin menyimpan dataset dan experiment

Belum perlu jika:

- baru eksplorasi prompt sederhana
- hanya memakai AI secara manual
- belum punya automation atau app
- logging 9Router sudah cukup

Prinsip:

```text
Gunakan Langfuse saat kamu perlu melihat "apa yang terjadi di dalam sistem AI".
```

## Konsep Utama

### Trace

Trace adalah satu alur lengkap request.

Contoh:

```text
User bertanya
  -> retrieve dokumen
  -> panggil model
  -> model menjawab
  -> kirim output
```

Semua langkah itu bisa berada dalam satu trace.

### Span

Span adalah langkah dalam trace.

Contoh:

- retrieve docs
- call embedding model
- call chat model
- call tool
- format output
- send Telegram message

### Generation

Generation adalah panggilan ke model AI.

Data yang biasanya dicatat:

- model
- prompt/input
- completion/output
- token usage
- cost
- latency

### Event

Event adalah catatan kejadian penting.

Contoh:

- user clicked retry
- fallback provider used
- report sent to Telegram
- RAG source missing

### Score

Score adalah nilai evaluasi.

Contoh:

```text
correctness: 4/5
faithfulness: 5/5
safety: pass
source_citation: 3/5
```

## Observability vs Evaluation

Observability:

```text
Melihat apa yang terjadi.
```

Evaluation:

```text
Menilai apakah hasilnya baik.
```

Contoh:

```text
Observability:
Request memakai model X, latency 8 detik, output 900 token.

Evaluation:
Jawaban benar 4/5, sumber relevan 5/5, safety pass.
```

## Prompt Management

Langfuse bisa dipakai untuk menyimpan dan mengelola versi prompt.

Manfaat:

- prompt versioning
- testing prompt baru
- rollback prompt lama
- membandingkan performa prompt
- memisahkan prompt dari kode aplikasi

Contoh prompt yang cocok dikelola:

- RAG answer prompt
- Daily VPS report prompt
- Security review prompt
- Issue triage prompt
- Changelog prompt

Workflow:

```text
Prompt v1
  -> diuji dengan dataset
  -> hasil kurang bagus
  -> buat Prompt v2
  -> run experiment
  -> pilih versi terbaik
```

## Dataset dan Experiment

Dataset adalah kumpulan test case.

Contoh:

```text
Question:
Bagaimana cara install 9Router di VPS?

Expected:
Jawaban menyebut Docker, port 20128, volume persistent, Nginx, HTTPS.
```

Experiment adalah proses menjalankan prompt/model terhadap dataset.

Tujuan:

- membandingkan model
- membandingkan prompt
- menguji perubahan RAG
- mengecek regression

## LLM-as-a-Judge

LLM-as-a-Judge berarti memakai model AI untuk menilai output AI lain berdasarkan rubric.

Contoh rubric:

```text
Nilai 0-5:
- correctness
- faithfulness
- completeness
- source citation
- safety
```

Gunakan untuk:

- RAG answer quality
- ringkasan automation
- customer support draft
- documentation assistant
- issue triage

Catatan:

- judge model juga bisa salah
- gunakan rubric jelas
- sampling bisa menghemat biaya
- high-risk output tetap perlu human review

## Integrasi dengan RAG

Langfuse berguna untuk melihat RAG pipeline:

```text
User question
  -> embedding query
  -> retrieved chunks
  -> final answer
  -> score faithfulness
```

Yang dicatat:

- query user
- chunk yang diambil
- sumber dokumen
- prompt final
- jawaban model
- score jawaban

Pertanyaan debugging:

- apakah chunk yang benar terambil?
- apakah chunk terlalu banyak?
- apakah model mengarang?
- apakah sumber disebut?
- apakah embedding model perlu diganti?

## Integrasi dengan AI Automation

Contoh Daily VPS Report:

```text
cron trigger
  -> collect server data
  -> call model via 9Router
  -> generate report
  -> send Telegram/Discord
  -> log trace to Langfuse
```

Yang dicatat di Langfuse:

- waktu automation jalan
- data summary
- model yang dipakai
- report output
- latency
- error
- score safety

Manfaat:

- tahu automation gagal di mana
- tahu report terlalu panjang atau tidak
- tahu model mana yang boros
- bisa audit output lama

## Integrasi dengan 9Router

Ada dua pendekatan:

### 1. 9Router untuk routing, Langfuse untuk app trace

```text
App/Agent
  -> Langfuse trace
  -> 9Router /v1
  -> Provider AI
```

Cocok untuk custom app/script.

### 2. Gateway lain + Langfuse

Jika nanti memakai LiteLLM/Portkey/Helicone, Langfuse tetap bisa dipakai untuk trace dan eval.

Untuk NalTech saat ini:

```text
9Router tetap sebagai gateway utama.
Langfuse ditambahkan jika butuh observability lebih detail.
```

## Self-host vs Cloud

### Langfuse Cloud

Kelebihan:

- cepat mulai
- tidak perlu maintenance server
- cocok untuk eksperimen

Kekurangan:

- data trace masuk platform cloud
- perlu memperhatikan data sensitif

### Self-host

Kelebihan:

- kontrol data lebih besar
- cocok untuk internal/private workflow
- bisa deploy di VPS sendiri

Kekurangan:

- perlu maintenance
- butuh backup
- perlu update
- perlu hardening

Langfuse bisa self-host dengan Docker. Untuk production, ikuti dokumentasi resmi self-hosting karena komponennya bisa melibatkan database, cache, storage, dan worker.

## Security dan Privacy

Jangan sembarang log data sensitif.

Jangan log:

- API key
- token
- password
- private key
- data customer sensitif
- file `.env`
- raw database dump

Praktik aman:

- masking secret sebelum trace
- log metadata secukupnya
- sampling production traces
- batasi akses dashboard
- gunakan HTTPS
- batasi retention jika perlu
- role-based access untuk tim

## Mini Project: Observability AI Docs Assistant

Tujuan:

```text
Menambahkan trace untuk AI Docs Assistant.
```

Trace yang dicatat:

```text
Question
  -> retrieved chunks
  -> final prompt
  -> model response
  -> sources
  -> score
```

Dataset:

```text
10 pertanyaan dari naltech-dev-docs
```

Score:

- correctness
- source citation
- faithfulness
- safety

Output:

```text
Langfuse dashboard menampilkan trace dan score tiap pertanyaan.
```

## Checklist Implementasi

- [ ] Tentukan workflow yang ingin diobservasi.
- [ ] Tentukan data yang boleh dilog.
- [ ] Masking secret sebelum logging.
- [ ] Buat project Langfuse.
- [ ] Buat API key.
- [ ] Integrasikan SDK atau API.
- [ ] Log trace, span, generation.
- [ ] Tambahkan score sederhana.
- [ ] Buat dataset test.
- [ ] Jalankan experiment.
- [ ] Review cost dan latency.
- [ ] Batasi akses dashboard.

## Kesimpulan

Langfuse membantu melihat dan mengevaluasi sistem AI secara lebih serius.

Pola terbaik:

```text
9Router
  -> routing dan usage

Langfuse
  -> trace, eval, prompt management, experiments
```

Untuk NalTech, Langfuse paling berguna setelah:

- AI Docs Assistant mulai dibuat
- automation mulai rutin
- prompt sering berubah
- model routing perlu dibandingkan
- kualitas jawaban perlu diukur

## Referensi

- [Langfuse Docs](https://langfuse.com/docs/)
- [Langfuse Get Started](https://langfuse.com/docs/get-started)
- [Langfuse Integrations](https://langfuse.com/integrations)
- [Langfuse Self-hosting](https://langfuse.com/self-hosting)
- [Langfuse LLM-as-a-Judge](https://langfuse.com/docs/evaluation/evaluation-methods/llm-as-a-judge)

