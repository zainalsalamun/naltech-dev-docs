# Fitaru Dashboard Design

Dokumen ini menjelaskan desain dashboard utama untuk MVP aplikasi Fitaru.

## Tujuan Dashboard

Dashboard adalah halaman utama yang user lihat setiap hari. Fungsinya bukan hanya menampilkan data, tetapi membantu user mengambil aksi cepat.

Tujuan utama:

- Menunjukkan kondisi hari ini dalam sekali lihat
- Membuat user mudah mencatat makan, olahraga, berat, dan air
- Memberi dorongan yang suportif
- Menampilkan progres tanpa membuat user merasa dihakimi
- Menjadi pusat aktivitas harian aplikasi

## Prinsip Dashboard

- Action-first: tombol catat harus mudah ditemukan
- Calm data: angka penting ditampilkan jelas, tapi tidak menekan
- Partial progress tetap dihargai
- Bahasa harus ramah dan realistis
- Dashboard tetap berguna meski user belum mencatat semua data

## Struktur Dashboard

Urutan konten dari atas ke bawah:

1. Header personal
2. Skor konsistensi hari ini
3. Aksi cepat
4. Ringkasan target harian
5. Timeline catatan hari ini
6. Insight atau pesan suportif
7. Bottom navigation

## 1. Header Personal

Fungsi:

- Menyapa user
- Menampilkan konteks hari ini
- Memberi akses ke notifikasi

Konten:

- Sapaan: "Hai, Raka"
- Subcopy: "Diet santai, progres tetap jalan."
- Icon notifikasi

Contoh:

```text
Hai, Raka
Diet santai, progres tetap jalan.       [Notifikasi]
```

## 2. Skor Konsistensi

Fungsi:

- Menjadi hero metric dashboard
- Mengukur kebiasaan, bukan kesempurnaan

Data yang dihitung:

- Makan tercatat
- Air tercatat
- Olahraga tercatat
- Berat tercatat sesuai jadwal

Contoh:

```text
Skor konsistensi
62%
2 dari 4 kebiasaan sudah tercatat
```

Copy alternatif:

- "Hari ini sudah 2 dari 4 kebiasaan tercatat."
- "Progres kecil tetap dihitung."
- "Belum lengkap tidak apa-apa, lanjut pelan-pelan."

## 3. Aksi Cepat

Fungsi:

- Memberi shortcut untuk pencatatan utama
- Mengurangi jumlah tap

Aksi:

- Makan
- Olahraga
- Berat
- Air

Layout:

- Grid 4 kolom
- Icon di atas
- Label pendek
- State selesai bila sudah tercatat

State:

- Default: soft mint surface
- Completed: teal tint atau check marker
- Pressed: teal background

## 4. Ringkasan Target Harian

Fungsi:

- Menampilkan progres target harian yang paling penting
- Memudahkan user melihat bagian yang belum lengkap

Komponen:

### Makan

Contoh:

```text
Makan
2/4 waktu makan tercatat
Sarapan, makan siang sudah masuk
```

### Air

Contoh:

```text
Air minum
5/8 gelas
```

### Olahraga

Contoh:

```text
Olahraga
Belum hari ini
Jalan 10 menit juga sudah progres
```

### Berat

Contoh:

```text
Berat terakhir
74.8 kg
Turun 0.4 kg minggu ini
```

## 5. Timeline Hari Ini

Fungsi:

- Menampilkan catatan yang sudah masuk hari ini
- Membuat user merasa progresnya nyata

Contoh item:

```text
08:10  Sarapan: Roti gandum, telur
12:35  Makan siang: Nasi ayam, sayur
15:20  Air: +1 gelas
```

Empty state:

```text
Belum ada catatan hari ini.
Mulai dari satu catatan kecil dulu.
```

## 6. Insight Harian

Fungsi:

- Memberi arahan lembut
- Tidak menghukum user

Contoh:

- "Makan enak tetap boleh, yang penting tercatat."
- "Hari ini air minummu sudah lumayan. Tambah 3 gelas lagi pelan-pelan."
- "Belum olahraga hari ini. Jalan 10 menit juga tetap progres."
- "Fokus ke tren, bukan satu angka hari ini."

## Dashboard States

### State 1: Baru Mulai Hari

Kondisi:

- Belum ada catatan

Prioritas UI:

- Tampilkan empty state ramah
- Tombol "Catat makan" paling menonjol

Copy:

```text
Hari baru, mulai ringan dulu.
Catat makanan pertamamu hari ini.
```

### State 2: Sebagian Tercatat

Kondisi:

- Ada 1 sampai 3 kebiasaan tercatat

Prioritas UI:

- Tampilkan skor konsistensi
- Tampilkan next best action

Copy:

```text
Sudah mulai jalan. Lanjut satu kebiasaan lagi.
```

### State 3: Hampir Lengkap

Kondisi:

- Hampir semua target tercatat

Prioritas UI:

- Rayakan progres dengan lembut
- Hindari gamification yang terlalu ramai

Copy:

```text
Hari ini rapi. Pertahankan ritmenya.
```

## Layout Mobile

Rekomendasi mobile:

```text
┌─────────────────────────────┐
│ Hai, Raka             Bell  │
│ Diet santai, progres...     │
│                             │
│ [Consistency Hero Card]     │
│                             │
│ Aksi cepat                  │
│ [Makan] [Gerak] [Berat] [Air]
│                             │
│ Target hari ini             │
│ [Makan 2/4]                 │
│ [Air 5/8]                   │
│ [Olahraga belum]            │
│                             │
│ Timeline hari ini           │
│ [Sarapan]                   │
│ [Makan siang]               │
│                             │
│ [Insight]                   │
│                             │
│ Bottom nav                  │
└─────────────────────────────┘
```

## Layout Tablet / Desktop

Untuk fase berikutnya bila Fitaru punya dashboard web:

```text
┌───────────────────────────────────────────────┐
│ Header                                        │
├───────────────────────┬───────────────────────┤
│ Consistency + Actions │ Daily target summary  │
├───────────────────────┼───────────────────────┤
│ Timeline today        │ Insight + Tips        │
└───────────────────────┴───────────────────────┘
```

## Komponen Dashboard

### Consistency Hero Card

Isi:

- Label: Skor konsistensi
- Angka besar: 62%
- Progress bar
- Subcopy

Style:

- Background gradient teal
- Text putih
- Rounded 18
- Tidak terlalu tinggi

### Quick Action Tile

Isi:

- Icon
- Label
- Optional check marker

Style:

- Surface soft mint
- Active teal
- Radius 16

### Daily Target Card

Isi:

- Icon
- Nama target
- Angka progres
- Progress bar kecil
- Subcopy pendek

Style:

- White card
- Border soft
- Compact

### Timeline Item

Isi:

- Jam
- Jenis catatan
- Detail pendek

Style:

- Icon kecil
- Line vertical lembut opsional
- Tidak perlu card besar untuk setiap item

## Prioritas Data MVP

Untuk MVP, dashboard cukup memakai data:

- `todayMealsCount`
- `todayWaterGlasses`
- `todayExerciseMinutes`
- `lastWeight`
- `weeklyWeightChange`
- `consistencyScore`
- `todayLogs`

Belum perlu:

- Analisis nutrisi detail
- Macro protein/karbo/lemak
- AI recommendation kompleks
- Integrasi wearable

## Success Criteria

Dashboard MVP dianggap berhasil bila:

- User bisa memahami status hari ini kurang dari 5 detik
- User bisa mencatat makan dalam 1 tap dari dashboard
- User tidak merasa bersalah saat data belum lengkap
- User tahu aksi berikutnya yang paling masuk akal
- Dashboard tetap terlihat berguna walau data masih sedikit

## Next Iteration

Iterasi berikutnya:

1. Membuat prototype dashboard interaktif
2. Membuat state kosong, sebagian, dan lengkap
3. Membuat versi dark mode opsional
4. Membuat desain setup target harian
5. Menentukan struktur data untuk dashboard
