---
title: "RAG dan Knowledge Base untuk AI Agent"
description: "Panduan membuat knowledge base AI agent dengan RAG, embedding, vector database, retrieval, dan mini project AI Docs Assistant untuk naltech-dev-docs."
category: "AI Tools"
level: "Intermediate"
order: 125
tags: ["ai", "rag", "knowledge-base", "embedding", "vector-database", "agent", "retrieval"]
updated: "2026-05-23"
---

# RAG dan Knowledge Base untuk AI Agent

RAG adalah singkatan dari **Retrieval-Augmented Generation**. RAG membuat AI bisa menjawab berdasarkan dokumen atau knowledge base yang kita miliki, bukan hanya dari pengetahuan umum model.

Tanpa RAG:

```text
User bertanya
  -> model menjawab dari pengetahuan internal dan context yang dikirim
```

Dengan RAG:

```text
User bertanya
  -> sistem mencari dokumen relevan
  -> dokumen relevan dikirim ke model
  -> model menjawab berdasarkan dokumen tersebut
```

RAG cocok untuk membuat agent yang bisa menjawab pertanyaan dari dokumentasi internal, catatan project, SOP, issue, changelog, atau knowledge base tim.

## Kenapa Agent Butuh Knowledge Base?

Agent punya context window terbatas. Jika semua dokumen selalu dikirim ke model, token akan boros dan lambat.

Knowledge base membantu agent:

- mencari informasi yang relevan saja
- mengurangi token
- menjawab berdasarkan sumber internal
- menghindari jawaban terlalu umum
- membuat dokumentasi lebih berguna
- mempercepat onboarding developer

Contoh:

```text
Pertanyaan:
"Bagaimana cara install 9Router di VPS?"

RAG:
  -> cari halaman 9Router Proxy
  -> ambil bagian install VPS
  -> kirim bagian relevan ke model
  -> model menjawab dengan sumber yang tepat
```

## Konsep Penting

### Document

Document adalah sumber pengetahuan.

Contoh:

- file Markdown
- PDF
- issue GitHub
- changelog
- README
- SOP
- catatan meeting
- halaman docs

### Chunk

Chunk adalah potongan kecil dari dokumen.

Dokumen panjang dipotong agar mudah dicari.

Contoh:

```text
openclaw.md
  -> chunk 1: pengertian OpenClaw
  -> chunk 2: instalasi lokal
  -> chunk 3: instalasi VPS
  -> chunk 4: security
```

### Embedding

Embedding adalah representasi angka dari teks.

Tujuannya agar sistem bisa mencari makna yang mirip, bukan hanya kata yang sama.

Contoh:

```text
"install 9Router di VPS"
```

bisa mirip dengan:

```text
"cara deploy 9Router pakai Docker di server"
```

### Vector Database

Vector database menyimpan embedding dan mencari chunk yang paling mirip dengan pertanyaan.

Contoh tools:

- Chroma
- Qdrant
- LanceDB
- pgvector
- Supabase Vector

### Retrieval

Retrieval adalah proses mencari chunk yang relevan.

Alur:

```text
query user
  -> embedding query
  -> search vector database
  -> ambil top-k chunk
  -> kirim chunk ke model
```

### Reranking

Reranking adalah menyusun ulang hasil retrieval agar chunk paling relevan naik ke atas.

Reranking berguna jika:

- dokumen banyak
- hasil retrieval sering meleset
- query ambigu
- top-k terlalu noisy

## Alur RAG

Alur indexing:

```text
Dokumen
  -> parsing
  -> cleaning
  -> chunking
  -> embedding
  -> simpan ke vector database
```

Alur query:

```text
Pertanyaan user
  -> embedding query
  -> retrieval dari vector database
  -> ambil chunk relevan
  -> masukkan ke prompt
  -> model menjawab
  -> tampilkan sumber
```

## Kapan Perlu RAG?

Gunakan RAG jika:

- dokumen banyak
- pertanyaan sering merujuk knowledge base internal
- agent perlu menjawab berdasarkan sumber tertentu
- context terlalu besar jika dikirim semua
- butuh pencarian semantik
- ingin membangun docs assistant

Tidak perlu RAG jika:

- dokumen sedikit
- cukup baca 1-3 file langsung
- pertanyaan sederhana
- data sering berubah setiap detik
- butuh perhitungan, bukan pencarian dokumen

Prinsip:

```text
Kalau sumbernya sedikit, baca langsung.
Kalau sumbernya banyak, gunakan RAG.
```

## Tools RAG

### Chroma

Chroma adalah vector database yang populer untuk eksperimen dan prototyping.

Cocok untuk:

- belajar RAG
- local development
- project kecil
- prototyping cepat

Kelebihan:

- mudah dipakai
- cocok untuk Python/TypeScript
- bisa local
- sederhana untuk pemula

Kekurangan:

- untuk production besar, perlu evaluasi lebih lanjut
- operasional tidak sekuat Qdrant/Postgres untuk beberapa use case

### Qdrant

Qdrant adalah vector database yang kuat untuk semantic search.

Cocok untuk:

- production vector search
- filtering metadata
- deployment Docker/VPS/cloud
- dokumen lebih banyak
- search performa tinggi

Kelebihan:

- fokus vector search
- metadata filtering
- performa bagus
- bisa self-host
- dokumentasi kuat

Kekurangan:

- setup lebih serius dibanding Chroma
- perlu memahami collection/vector config

### pgvector

pgvector adalah extension PostgreSQL untuk vector similarity search.

Cocok untuk:

- project yang sudah memakai PostgreSQL
- ingin data relasional dan vector dalam satu database
- aplikasi yang butuh query SQL + vector search

Kelebihan:

- tidak perlu database baru jika sudah pakai Postgres
- query SQL familiar
- bisa digabung dengan data bisnis

Kekurangan:

- tuning index perlu dipahami
- untuk vector search skala besar, dedicated vector DB bisa lebih cocok

### LanceDB

LanceDB adalah database untuk vector search yang cocok untuk local/embedded dan data AI.

Cocok untuk:

- local RAG
- prototype
- data science workflow
- file-based vector store

### Supabase Vector

Supabase Vector memakai PostgreSQL/pgvector.

Cocok untuk:

- aplikasi web
- project yang sudah memakai Supabase
- auth/database/storage dalam satu platform

### LangChain dan LlamaIndex

LangChain dan LlamaIndex bukan vector database, tetapi framework untuk membangun aplikasi RAG/agent.

Cocok untuk:

- document loader
- chunking
- retrieval pipeline
- agent dengan tool RAG
- evaluasi dan eksperimen pipeline

LlamaIndex sangat cocok untuk document-centric RAG, sedangkan LangChain cocok untuk workflow/tooling yang lebih luas.

## Embedding Model

Embedding model mengubah teks menjadi vector.

Pilihan:

- OpenAI embeddings
- Gemini embeddings
- Cohere embeddings
- Jina embeddings
- BGE / bge-m3
- Nomic embeddings
- Ollama embeddings
- Sentence Transformers

Kriteria memilih embedding:

- bahasa yang didukung
- kualitas retrieval
- biaya
- kecepatan
- ukuran vector
- bisa local atau cloud

Untuk bahasa Indonesia, pilih embedding multilingual jika memungkinkan.

## Chunking Strategy

Chunking sangat penting. Banyak RAG gagal bukan karena vector DB, tetapi karena chunking buruk.

Strategi umum:

```text
chunk size: 500-1200 token
overlap: 10-20%
```

Untuk Markdown:

- potong berdasarkan heading
- pertahankan judul section
- simpan metadata file dan heading
- jangan potong code block sembarangan

Contoh metadata:

```json
{
  "source": "src/content/docs/ai-tools/9router-proxy.md",
  "title": "9Router Proxy",
  "heading": "Cara Install 9Router di VPS",
  "category": "AI Tools",
  "updated": "2026-05-22"
}
```

## Prompt RAG

Prompt untuk RAG harus memaksa model menjawab berdasarkan context.

Template:

```text
Kamu adalah AI docs assistant.

Jawab pertanyaan user hanya berdasarkan context yang diberikan.
Jika context tidak cukup, jawab "informasi belum tersedia di dokumentasi".
Jangan mengarang.
Sertakan sumber file atau judul section jika tersedia.

Context:
[retrieved chunks]

Pertanyaan:
[user question]
```

Output:

```text
Jawaban:
...

Sumber:
- 9Router Proxy > Cara Install 9Router di VPS
- AI Automation > Step by Step Membuat AI Automation
```

## Mini Project: AI Docs Assistant untuk naltech-dev-docs

Tujuan:

```text
Membuat assistant yang bisa menjawab pertanyaan dari dokumentasi naltech-dev-docs.
```

Contoh pertanyaan:

```text
Bagaimana cara install 9Router di VPS?
Apa bedanya OpenClaw dan OpenCode?
Bagaimana membuat AI automation daily VPS report?
Kapan pakai local model?
Bagaimana membuat prompt agent yang aman?
```

### Arsitektur sederhana

```text
Markdown docs
  -> indexer script
  -> chunks + embeddings
  -> vector database
  -> query script/API
  -> 9Router
  -> answer with sources
```

### Struktur folder

```text
rag-docs-assistant/
  .env
  package.json
  scripts/
    index-docs.mjs
    ask-docs.mjs
  data/
    chunks.json
    vector-store/
```

### Tahap 1: Load Markdown

Ambil semua file:

```text
src/content/docs/**/*.md
```

Skip:

- `.env`
- file binary
- output build
- private notes

### Tahap 2: Chunking

Untuk setiap Markdown:

```text
1. baca frontmatter
2. ambil title, category, tags
3. split berdasarkan heading
4. pecah section panjang
5. simpan metadata
```

### Tahap 3: Embedding

Gunakan embedding model:

```text
Cloud embedding -> kualitas bagus, ada biaya
Local embedding -> lebih private, perlu setup
```

Jika lewat 9Router, pastikan provider embedding tersedia. Jika tidak, pakai embedding provider langsung atau local embedding.

### Tahap 4: Simpan vector

Pilihan pemula:

```text
Chroma atau LanceDB
```

Pilihan production:

```text
Qdrant atau pgvector
```

### Tahap 5: Query

Alur query:

```text
User question
  -> embed question
  -> retrieve top 5 chunks
  -> build prompt
  -> ask model via 9Router
  -> answer with sources
```

### Tahap 6: Evaluasi

Buat daftar pertanyaan test:

```text
1. Cara install 9Router di VPS?
2. Bagaimana OpenClaw dipakai di VPS?
3. Apa permission matrix untuk agent?
4. Bagaimana cost control AI?
5. Bagaimana local model dihubungkan ke 9Router?
```

Cek:

- apakah jawabannya benar?
- apakah sumbernya relevan?
- apakah model mengarang?
- apakah chunk yang diambil tepat?

## Security untuk RAG

Jangan index file sensitif.

Jangan index:

- `.env`
- private key
- API key
- token
- database dump
- credential
- log mentah yang berisi secret

Tambahkan filter:

```text
Skip file jika path mengandung:
.env
secret
private
credential
node_modules
dist
build
```

Masking:

```text
API key -> [MASKED_API_KEY]
token -> [MASKED_TOKEN]
password -> [MASKED_PASSWORD]
```

## Cost Control RAG

Biaya RAG muncul dari:

- embedding dokumen
- embedding query
- model answer
- re-index dokumen
- reranking

Cara hemat:

- index hanya dokumen penting
- chunk tidak terlalu kecil
- re-index hanya file yang berubah
- cache embedding
- batasi top-k retrieval
- batasi output
- gunakan model ringan untuk query sederhana

Aturan:

```text
top-k awal: 5
max context chunk: 5-8 chunk
output: maksimal 1000-1500 token untuk jawaban docs
```

## Common Problems

### Jawaban ngawur

Penyebab:

- chunk tidak relevan
- prompt tidak memaksa jawab dari context
- retrieval buruk
- model terlalu bebas

Solusi:

- tambahkan instruksi "jawab hanya berdasarkan context"
- tampilkan sumber
- perbaiki chunking
- gunakan reranking

### Dokumen relevan tidak muncul

Penyebab:

- embedding kurang cocok
- chunk terlalu besar/kecil
- metadata tidak dipakai
- query ambigu

Solusi:

- ubah chunk size
- tambah overlap
- gunakan embedding multilingual
- tambahkan keyword search/hybrid search

### Token terlalu besar

Penyebab:

- top-k terlalu banyak
- chunk terlalu besar
- context panjang
- output terlalu panjang

Solusi:

- kurangi top-k
- ringkas chunk
- batasi output
- gunakan reranking sebelum model final

### Informasi kadaluarsa

Penyebab:

- index tidak diperbarui
- dokumen berubah tapi vector lama

Solusi:

- simpan hash file
- re-index file yang berubah
- tampilkan `updated` dari frontmatter

## Rekomendasi untuk NalTech

Tahap belajar:

```text
Markdown docs
  -> script index sederhana
  -> Chroma/LanceDB local
  -> query via 9Router
```

Tahap lebih serius:

```text
naltech-dev-docs
  -> indexer incremental
  -> Qdrant or pgvector
  -> API docs assistant
  -> Telegram/Discord bot
  -> answer with sources
```

Gunakan RAG untuk:

- menjawab pertanyaan dari docs
- onboarding developer
- mencari tutorial internal
- menjelaskan setup project
- membuat FAQ otomatis

Jangan gunakan RAG untuk:

- membaca secret
- mengambil keputusan production tanpa review
- menggantikan dokumentasi yang belum ditulis

## Checklist RAG

- [ ] Sumber dokumen jelas.
- [ ] File sensitif dikecualikan.
- [ ] Chunking berdasarkan heading.
- [ ] Metadata disimpan.
- [ ] Embedding model dipilih.
- [ ] Vector store dipilih.
- [ ] Query mengambil top-k chunk.
- [ ] Prompt melarang model mengarang.
- [ ] Jawaban menyertakan sumber.
- [ ] Ada test question.
- [ ] Ada re-index strategy.
- [ ] Usage token dipantau.

## Kesimpulan

RAG membuat AI agent bisa memakai knowledge base internal tanpa mengirim semua dokumen ke model.

Pola terbaik:

```text
Dokumen rapi
  -> chunking bagus
  -> embedding cocok
  -> retrieval relevan
  -> prompt yang ketat
  -> jawaban dengan sumber
```

Untuk NalTech, mini project terbaik adalah **AI Docs Assistant** yang menjawab pertanyaan dari `naltech-dev-docs`. Ini akan membuat dokumentasi yang sudah dibuat menjadi benar-benar hidup dan bisa ditanya oleh agent.

## Referensi

- [Chroma Embedding Functions](https://docs.trychroma.com/docs/embeddings/embedding-functions)
- [Qdrant Documentation](https://qdrant.tech/documentation/)
- [Qdrant Vectors](https://qdrant.tech/documentation/manage-data/vectors/)
- [pgvector GitHub](https://github.com/pgvector/pgvector)
- [LlamaIndex Docs](https://docs.llamaindex.ai/)

