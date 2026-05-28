---
title: "Roadmap Belajar Flutter"
description: "Peta belajar Flutter dari dasar, praktik, state management, project, Firebase, local storage, sampai persiapan aplikasi production."
category: "Flutter"
level: "Roadmap"
order: 5
tags: ["flutter", "roadmap", "learning-path", "kurikulum"]
updated: "2026-05-23"
---

# Roadmap Belajar Flutter

Roadmap ini dibuat supaya proses belajar Flutter lebih terarah. Tujuannya bukan menyelesaikan semua materi secepat mungkin, tetapi memahami urutan belajar yang benar: mulai dari konsep dasar, latihan kecil, project, state management, penyimpanan data, Firebase, sampai aplikasi yang lebih siap produksi.

Gunakan roadmap ini sebagai peta. Kalau bingung harus belajar apa berikutnya, kembali ke halaman ini.

![Roadmap belajar Flutter](/assets/flutter-roadmap.svg)

---

## 1. Gambaran Besar

Alur belajar yang disarankan:

```text
Dasar Flutter
-> Praktik per Bab
-> Project 1: Catatan Belajar
-> CRUD Lokal, Filter, Search
-> State Management
-> Project 2: Task Manager
-> Local Storage
-> Firebase
-> API CRUD
-> Auth
-> Clean Architecture sederhana
```

Kenapa urutannya seperti ini?

Karena Flutter bukan hanya soal menghafal widget. Flutter perlu dipahami sebagai gabungan dari:

- UI
- data
- state
- navigasi
- form
- list
- storage
- API
- Firebase/backend
- struktur project

Jika langsung lompat ke Firebase atau architecture tanpa kuat di dasar, biasanya akan mudah bingung.

---

## 2. Level 1: Fondasi Flutter

Target level ini adalah bisa membuat aplikasi Flutter sederhana dan memahami cara Flutter membangun UI.

Materi yang dipelajari:

1. Tutorial Flutter Dasar untuk Pemula
2. Dasar Bahasa Dart
3. Widget dasar
4. Layout dasar
5. `StatelessWidget` dan `StatefulWidget`
6. State sederhana dengan `setState`
7. Navigasi
8. Form
9. List

Checklist selesai:

- [ ] Bisa membuat project Flutter baru.
- [ ] Bisa membaca struktur folder Flutter.
- [ ] Bisa menulis kode Dart dasar.
- [ ] Bisa membuat UI dengan widget.
- [ ] Bisa menyusun layout dengan `Column`, `Row`, `Container`, dan `Padding`.
- [ ] Bisa memakai `setState`.
- [ ] Bisa membuat navigasi antar halaman.
- [ ] Bisa membaca input dari form.
- [ ] Bisa menampilkan data dengan `ListView.builder`.

Materi terkait:

- [Tutorial Flutter Dasar untuk Pemula](/docs/flutter/dasar/)
- [Praktik Flutter per Bab](/docs/flutter/praktik-per-bab/)

---

## 3. Level 2: Praktik Dasar

Setelah paham teori dasar, lanjut ke latihan kecil. Jangan buru-buru masuk project besar.

Target:

- terbiasa mengetik kode Flutter
- memahami error umum
- bisa mengubah contoh kode
- bisa menghubungkan teori dengan UI nyata

Latihan yang perlu dikerjakan:

- variable dan function Dart
- List dan Map
- model class
- widget dasar
- counter state
- form input
- navigasi sederhana
- list sederhana

Checklist selesai:

- [ ] Bisa menyelesaikan latihan tanpa melihat contoh terus-menerus.
- [ ] Bisa menjelaskan alur data dari input ke tampilan.
- [ ] Bisa debug error sederhana.
- [ ] Bisa memecah widget menjadi komponen kecil.

Materi terkait:

- [Praktik Flutter per Bab](/docs/flutter/praktik-per-bab/)

---

## 4. Level 3: Project Pertama

Project pertama bertujuan menggabungkan dasar Flutter menjadi aplikasi kecil.

Project:

- Aplikasi Catatan Belajar

Fitur:

- menampilkan daftar catatan
- menambah catatan
- menghapus catatan
- empty state
- memisahkan file model, page, dan widget

Skill yang dilatih:

- `StatefulWidget`
- `TextEditingController`
- `Navigator`
- `ListView.builder`
- model class
- komponen widget

Checklist selesai:

- [ ] Bisa membuat model `Note`.
- [ ] Bisa membuat halaman list.
- [ ] Bisa membuat halaman form.
- [ ] Bisa mengirim data antar halaman.
- [ ] Bisa menambahkan data ke list.
- [ ] Bisa menghapus data dari list.
- [ ] Bisa menampilkan empty state.

Materi terkait:

- [Project 1: Aplikasi Catatan Belajar](/docs/flutter/project-catatan-belajar/)

---

## 5. Level 4: CRUD Lokal, Filter, dan Search

Sebelum masuk project yang lebih kompleks, pahami dulu CRUD lokal.

Target:

- bisa tambah data
- bisa baca data
- bisa update data
- bisa hapus data
- bisa filter data
- bisa search data

Konsep penting:

- `enum`
- `id`
- `copyWith`
- `.where()`
- `.contains()`
- empty state

Checklist selesai:

- [ ] Bisa membuat model `Task`.
- [ ] Bisa memakai `enum`.
- [ ] Bisa menambah data ke `List`.
- [ ] Bisa update data berdasarkan `id`.
- [ ] Bisa hapus data berdasarkan `id`.
- [ ] Bisa filter berdasarkan status.
- [ ] Bisa search berdasarkan keyword.
- [ ] Bisa membuat empty state sesuai kondisi.

Materi terkait:

- [CRUD Lokal, Filter, dan Search](/docs/flutter/crud-lokal-filter-search/)

---

## 6. Level 5: State Management

State management dipelajari setelah kamu merasakan bahwa `setState` mulai kurang nyaman untuk fitur yang lebih besar.

Urutan belajar:

```text
State Management Dasar
-> Provider
-> Riverpod
-> Cubit
-> Bloc
```

### State Management Dasar

Pelajari dulu:

- apa itu state
- local state
- shared state
- kapan `setState` cukup
- kapan state perlu dipisah
- loading, empty, error, success state

Materi:

- [State Management Dasar](/docs/flutter/state-management-dasar/)

### Provider

Provider cocok sebagai state management pertama.

Pelajari:

- `ChangeNotifier`
- `notifyListeners`
- `ChangeNotifierProvider`
- `Consumer`
- `context.watch`
- `context.read`
- `Selector`
- `MultiProvider`

Materi:

- [Provider untuk Pemula](/docs/flutter/provider-untuk-pemula/)

### Riverpod

Riverpod cocok jika ingin state lebih modern, testable, dan rapi untuk async.

Pelajari:

- `ProviderScope`
- `ConsumerWidget`
- `WidgetRef`
- `StateProvider`
- `Provider`
- `NotifierProvider`
- `FutureProvider`
- `AsyncValue`

Materi:

- [Riverpod untuk Pemula](/docs/flutter/riverpod-untuk-pemula/)

### Cubit dan Bloc

Cubit/Bloc cocok untuk flow yang lebih eksplisit dan project besar.

Pelajari:

- Cubit
- `emit`
- `BlocProvider`
- `BlocBuilder`
- `BlocListener`
- `BlocConsumer`
- event-state di Bloc

Materi:

- [Cubit dan Bloc Dasar](/docs/flutter/cubit-bloc-dasar/)

Checklist selesai:

- [ ] Bisa menjelaskan perbedaan `setState`, Provider, Riverpod, dan Cubit/Bloc.
- [ ] Bisa membuat provider/cubit sederhana.
- [ ] Bisa memindahkan logic dari UI ke state class.
- [ ] Bisa memilih state management sesuai kebutuhan.
- [ ] Bisa memahami loading, empty, error, success state.

---

## 7. Level 6: Project Kedua

Setelah paham CRUD dan state management, lanjut ke project yang lebih realistis.

Project:

- Task Manager

Fitur:

- tambah task
- edit task
- hapus task dengan konfirmasi
- ubah status task
- filter task
- search task
- empty state

Skill yang dilatih:

- model `Task`
- `enum TaskStatus`
- `copyWith`
- CRUD lokal
- form edit
- filter dan search
- state yang mulai kompleks

Checklist selesai:

- [ ] Bisa membuat aplikasi Task Manager dengan `setState`.
- [ ] Bisa memahami alur tambah/edit/hapus.
- [ ] Bisa membuat filter dan search.
- [ ] Bisa menampilkan pesan kosong yang tepat.
- [ ] Bisa menjelaskan bagian mana yang nanti cocok dipindahkan ke Provider/Riverpod/Cubit.

Materi terkait:

- [Project 2: Task Manager](/docs/flutter/project-task-manager/)

---

## 8. Level 7: Setup Cloud Workspace dan Firebase

Setelah project dasar aman, kamu bisa mulai belajar tools cloud dan Firebase.

Target:

- bisa setup Flutter di Firebase Studio
- bisa import project dari GitHub
- bisa menjalankan project di cloud workspace
- bisa menghubungkan Flutter ke Firebase

Materi:

- [Setup Project Flutter di Firebase Studio](/docs/flutter/setup-flutter-firebase-studio/)

Checklist selesai:

- [ ] Bisa membuka Firebase Studio.
- [ ] Bisa membuat/import project Flutter.
- [ ] Bisa menjalankan `flutter pub get`.
- [ ] Bisa menjalankan preview Flutter.
- [ ] Bisa install FlutterFire CLI.
- [ ] Bisa menjalankan `flutterfire configure`.
- [ ] Bisa inisialisasi Firebase di `main.dart`.

---

## 9. Level 8: Local Storage

Local storage dipelajari ketika data lokal tidak boleh hilang saat aplikasi ditutup.

Target materi berikutnya:

- memahami kenapa data hilang saat hanya memakai `List`
- mengenal pilihan storage
- memakai `shared_preferences`
- menyimpan object ke JSON
- load data saat aplikasi dibuka

Pilihan storage:

| Storage | Cocok Untuk |
| --- | --- |
| `shared_preferences` | setting kecil, token sederhana, cache ringan |
| Hive/Isar | data lokal lebih banyak dan cepat |
| SQLite/sqflite | data relational dan query |
| Firestore | database online realtime/cloud |

Checklist sebelum belajar local storage:

- [ ] Sudah paham model class.
- [ ] Sudah paham `toJson` dan `fromJson` secara konsep.
- [ ] Sudah paham CRUD lokal.
- [ ] Sudah punya project Task Manager lokal.

---

## 10. Level 9: API dan Firebase

Setelah local storage, lanjut ke data online.

Jalur API:

```text
HTTP request
-> JSON
-> model
-> repository
-> UI
```

Jalur Firebase:

```text
Firebase Auth
-> Firestore
-> Storage
-> user-specific data
```

Materi yang cocok dibuat berikutnya:

1. API CRUD App
2. Firebase Authentication
3. Cloud Firestore
4. Upload gambar ke Firebase Storage
5. Task Manager sync ke Firestore

Checklist siap masuk API/Firebase:

- [ ] Bisa parsing JSON.
- [ ] Bisa membuat model dari Map.
- [ ] Bisa memahami async/await.
- [ ] Bisa menampilkan loading/error/data.
- [ ] Bisa memakai state management dasar.

---

## 11. Level 10: Struktur Project Lebih Rapi

Saat aplikasi mulai besar, struktur folder perlu dirapikan.

Target:

- memisahkan feature
- memisahkan model, service, repository, state, dan UI
- membuat kode mudah dirawat

Contoh struktur:

```text
lib/
  core/
    theme/
    utils/
  features/
    tasks/
      data/
      domain/
      presentation/
```

Untuk pemula, jangan langsung mulai dari struktur besar. Gunakan struktur besar ketika fitur sudah mulai banyak.

Tanda perlu struktur lebih rapi:

- file page terlalu panjang
- service bercampur dengan UI
- logic API ditulis langsung di widget
- banyak kode berulang
- sulit menambah fitur tanpa takut merusak fitur lama

---

## 12. Jalur Belajar Cepat

Jika ingin belajar cepat untuk membuat aplikasi sederhana:

```text
Dasar Flutter
-> Praktik per Bab
-> Project Catatan Belajar
-> CRUD Lokal
-> Project Task Manager
-> Local Storage
```

Cocok untuk:

- pemula
- belajar mandiri
- membuat aplikasi kecil

---

## 13. Jalur Belajar State Management

Jika ingin fokus state management:

```text
State Management Dasar
-> Provider
-> Riverpod
-> Cubit
-> Bloc
-> Upgrade Task Manager dengan masing-masing pendekatan
```

Catatan:

- Jangan hafalkan semua sekaligus.
- Pilih satu untuk dipakai dalam project.
- Pahami konsep data-flow, bukan hanya syntax.

Rekomendasi:

```text
Pemula -> Provider
Modern/scalable -> Riverpod
Enterprise/team besar -> Cubit/Bloc
```

---

## 14. Jalur Belajar Firebase

Jika ingin membangun aplikasi online:

```text
Setup Firebase Studio
-> FlutterFire CLI
-> Firebase Auth
-> Firestore CRUD
-> Storage
-> Security Rules
-> Hosting
```

Project yang cocok:

- Task Manager online
- Notes app online
- habit tracker
- simple chat app
- expense tracker

---

## 15. Checklist Akhir Roadmap

Kamu berada di jalur yang bagus jika sudah bisa:

- [ ] Membuat aplikasi Flutter sederhana dari nol.
- [ ] Membuat UI dari widget kecil.
- [ ] Membuat model data.
- [ ] Mengelola form.
- [ ] Menampilkan list.
- [ ] Membuat CRUD lokal.
- [ ] Memahami state management.
- [ ] Membuat minimal dua project.
- [ ] Menghubungkan project ke Firebase.
- [ ] Menyimpan data lokal atau online.
- [ ] Merapikan struktur folder project.

Roadmap ini tidak harus diselesaikan sekali jalan. Belajar Flutter paling bagus dilakukan dengan siklus:

```text
Baca konsep
-> ketik contoh
-> ubah contoh
-> buat project kecil
-> temukan error
-> catat solusi
-> ulangi
```

Semakin sering membuat project kecil, semakin cepat pola Flutter terasa natural.
