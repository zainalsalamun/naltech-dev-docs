---
title: "Local Storage Dasar"
description: "Pengenalan local storage di Flutter: memory, shared_preferences, Hive/Isar, SQLite, file storage, Firestore, kapan dipakai, alur penyimpanan, dan checklist belajar."
category: "Flutter"
level: "Storage"
order: 55
tags: ["flutter", "local-storage", "shared-preferences", "database", "offline"]
updated: "2026-05-23"
---

# Local Storage Dasar

Local storage adalah cara menyimpan data di device user agar data tidak hilang saat aplikasi ditutup. Ini adalah langkah penting setelah belajar CRUD lokal dengan `List`, karena data yang hanya disimpan di memory akan hilang ketika aplikasi restart.

Materi ini adalah pengantar sebelum praktik memakai `shared_preferences`, Hive/Isar, SQLite, atau Firebase.

---

## 1. Kenapa Perlu Local Storage

Saat belajar CRUD lokal, kita biasanya menyimpan data seperti ini:

```dart
final List<Task> tasks = [];
```

Masalahnya:

```text
Aplikasi dibuka
-> tasks dibuat kosong
-> user menambah task
-> task muncul di UI
-> aplikasi ditutup
-> memory dibersihkan
-> aplikasi dibuka lagi
-> tasks kosong lagi
```

Data hilang karena `List` hanya hidup selama aplikasi berjalan. Begitu aplikasi ditutup, data di memory ikut hilang.

Local storage menyelesaikan masalah ini:

```text
User menambah task
-> task masuk ke List
-> task disimpan ke storage device
-> aplikasi ditutup
-> aplikasi dibuka lagi
-> task dibaca dari storage
-> task tampil kembali
```

Jadi, local storage membuat aplikasi terasa lebih nyata karena data user tetap ada.

---

## 2. Memory vs Local Storage vs Cloud

Sebelum memilih teknologi, pahami dulu perbedaannya.

| Tempat Data | Bertahan Setelah App Ditutup | Butuh Internet | Cocok Untuk |
| --- | --- | --- | --- |
| Memory/List | Tidak | Tidak | latihan, state sementara |
| Local Storage | Ya | Tidak | data offline di device |
| Cloud Database | Ya | Ya | sinkron antar device/user |

Contoh:

- `List<Task>`: data hilang saat app ditutup.
- `shared_preferences`: data tetap ada di device.
- SQLite/Hive/Isar: data lokal yang lebih besar dan terstruktur.
- Firestore: data online yang bisa sinkron antar device.

Untuk pemula, urutannya:

```text
List di memory
-> shared_preferences
-> Hive/Isar atau SQLite
-> Firestore/cloud database
```

---

## 3. Jenis Local Storage di Flutter

Ada beberapa pilihan storage. Tidak semua harus dipakai sekaligus.

### shared_preferences

Cocok untuk:

- setting kecil
- status onboarding sudah selesai
- theme mode
- token sederhana
- cache ringan
- list kecil yang disimpan sebagai JSON string

Contoh data:

```text
isDarkMode = true
userName = "Budi"
lastOpenedPage = 2
```

Kelebihan:

- mudah dipelajari
- cocok untuk pemula
- setup ringan

Kekurangan:

- tidak cocok untuk data besar
- tidak ideal untuk query kompleks
- object/list harus diubah ke string JSON terlebih dahulu

### Hive atau Isar

Cocok untuk:

- data lokal lebih banyak
- aplikasi offline-first
- list task/note yang cukup banyak
- performa cepat
- data object

Contoh:

```text
daftar task
daftar catatan
riwayat transaksi lokal
cache produk
```

Kelebihan:

- cepat
- cocok untuk data lokal
- lebih nyaman untuk object/list

Kekurangan:

- perlu belajar konsep box/schema/adapter sesuai package
- setup lebih banyak daripada `shared_preferences`

### SQLite atau sqflite

Cocok untuk:

- data relational
- butuh query SQL
- tabel saling berhubungan
- data lokal yang butuh struktur jelas

Contoh:

```text
users
orders
order_items
products
```

Kelebihan:

- kuat untuk query
- familiar untuk developer yang tahu SQL
- cocok untuk data tabular

Kekurangan:

- lebih kompleks untuk pemula
- perlu memahami tabel, kolom, query, migration

### File Storage

Cocok untuk:

- menyimpan file teks
- menyimpan export/import JSON
- menyimpan file sementara
- menyimpan gambar atau dokumen lokal

Biasanya memakai package seperti `path_provider`.

### Firestore

Firestore bukan local storage murni, tetapi cloud database. Firestore juga punya kemampuan offline persistence, tetapi secara konsep tetap database cloud.

Cocok untuk:

- data online
- sinkron antar device
- banyak user
- aplikasi yang butuh login

Contoh:

```text
task per user
chat
notes online
data profile
```

---

## 4. Cara Memilih Storage

Gunakan pertanyaan ini:

### Data kecil atau besar?

Jika kecil:

```text
shared_preferences
```

Jika banyak:

```text
Hive/Isar atau SQLite
```

### Butuh query kompleks?

Jika butuh filter/query relational:

```text
SQLite
```

Jika hanya simpan dan ambil object:

```text
Hive/Isar
```

### Butuh online dan multi-user?

Jika iya:

```text
Firestore atau backend API
```

### Data harus bisa offline?

Jika iya:

```text
Local storage
```

Jika offline dan online:

```text
Local storage + sync ke cloud
```

---

## 5. Rekomendasi untuk Pemula

Urutan belajar yang paling nyaman:

```text
shared_preferences
-> simpan String/int/bool
-> simpan object sebagai JSON
-> simpan List object sebagai JSON
-> load data saat app dibuka
-> update storage saat data berubah
```

Setelah itu:

```text
Hive/Isar atau SQLite
```

Baru setelah itu:

```text
Firestore atau API online
```

Untuk project Task Manager, kita bisa mulai dari:

```text
Task List di memory
-> ubah Task menjadi JSON
-> simpan List<Task> sebagai String
-> load List<Task> saat app dibuka
```

---

## 6. Alur Penyimpanan Data

Alur saat menambah data:

```text
User isi form
-> aplikasi membuat object Task
-> Task dimasukkan ke List
-> List diubah menjadi JSON
-> JSON disimpan ke local storage
-> UI diperbarui
```

Alur saat aplikasi dibuka:

```text
Aplikasi start
-> baca data dari local storage
-> jika data ada, ubah JSON menjadi List<Task>
-> masukkan ke state aplikasi
-> tampilkan ke UI
```

Alur saat menghapus data:

```text
User hapus task
-> task dihapus dari List
-> List terbaru diubah menjadi JSON
-> storage ditimpa dengan data terbaru
-> UI diperbarui
```

Konsep penting:

```text
State di memory untuk UI
Storage untuk menyimpan data agar tidak hilang
```

Jangan menjadikan storage sebagai satu-satunya tempat membaca data setiap kali UI berubah. Biasanya, data dibaca dari storage saat awal, lalu disimpan di state. Saat state berubah, storage ikut diperbarui.

---

## 7. JSON untuk Object

Local storage sederhana biasanya tidak langsung menyimpan object Dart. Object perlu diubah menjadi format yang bisa disimpan, salah satunya JSON.

Contoh object:

```dart
class Task {
  final int id;
  final String title;

  const Task({
    required this.id,
    required this.title,
  });
}
```

Object ini belum bisa langsung disimpan sebagai string. Kita perlu ubah ke Map:

```dart
Map<String, dynamic> toJson() {
  return {
    'id': id,
    'title': title,
  };
}
```

Lalu nanti Map bisa diubah menjadi JSON string:

```dart
final jsonString = jsonEncode(task.toJson());
```

Untuk membaca kembali:

```dart
final map = jsonDecode(jsonString) as Map<String, dynamic>;
final task = Task.fromJson(map);
```

Inilah konsep dasar `toJson` dan `fromJson`.

---

## 8. toJson dan fromJson

Contoh lengkap:

```dart
class Task {
  final int id;
  final String title;

  const Task({
    required this.id,
    required this.title,
  });

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
    };
  }

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] as int,
      title: json['title'] as String,
    );
  }
}
```

Penjelasan:

- `toJson`: object Dart menjadi Map.
- `fromJson`: Map menjadi object Dart.
- `jsonEncode`: Map/List menjadi String.
- `jsonDecode`: String menjadi Map/List.

Kenapa ini penting?

Karena local storage, API, dan Firebase sering berhubungan dengan data berbentuk Map/JSON.

---

## 9. Menyimpan List Object

Jika punya banyak task:

```dart
final tasks = [
  const Task(id: 1, title: 'Belajar Flutter'),
  const Task(id: 2, title: 'Belajar Local Storage'),
];
```

Ubah ke List Map:

```dart
final jsonList = tasks.map((task) => task.toJson()).toList();
```

Ubah ke String:

```dart
final jsonString = jsonEncode(jsonList);
```

Baca kembali:

```dart
final decoded = jsonDecode(jsonString) as List<dynamic>;

final tasks = decoded
    .map((item) => Task.fromJson(item as Map<String, dynamic>))
    .toList();
```

Pola ini akan sering dipakai saat menyimpan list sederhana ke `shared_preferences`.

---

## 10. Loading State Saat Membaca Storage

Membaca storage bisa membutuhkan waktu. Walaupun cepat, tetap anggap sebagai operasi async.

State yang umum:

```dart
bool isLoading = true;
List<Task> tasks = [];
String? errorMessage;
```

Alur:

```text
isLoading = true
-> baca storage
-> jika berhasil, isi tasks
-> jika gagal, isi errorMessage
-> isLoading = false
```

UI:

```dart
if (isLoading) {
  return const Center(
    child: CircularProgressIndicator(),
  );
}

if (errorMessage != null) {
  return Center(
    child: Text(errorMessage!),
  );
}

if (tasks.isEmpty) {
  return const Center(
    child: Text('Belum ada data'),
  );
}
```

Ini membuat aplikasi lebih siap menghadapi kondisi nyata.

---

## 11. Error yang Sering Terjadi

### Data tidak tersimpan

Penyebab umum:

- lupa memanggil function save
- key storage berbeda saat save dan load
- data hanya ditambah ke List, tapi tidak disimpan ke storage

### Data gagal dibaca

Penyebab umum:

- format JSON berubah
- casting salah
- key tidak ditemukan
- data lama tidak sesuai model baru

### UI tidak update

Penyebab umum:

- lupa `setState`
- lupa `notifyListeners`
- state diubah tapi storage saja yang berubah

Ingat:

```text
Storage berubah tidak otomatis membuat UI berubah.
State aplikasi tetap harus diperbarui.
```

---

## 12. Checklist Local Storage Dasar

Pastikan sudah paham:

- [ ] Data di `List` memory hilang saat app ditutup.
- [ ] Local storage membuat data tetap ada di device.
- [ ] `shared_preferences` cocok untuk data kecil.
- [ ] Hive/Isar cocok untuk object lokal yang lebih banyak.
- [ ] SQLite cocok untuk data relational dan query.
- [ ] Firestore cocok untuk data cloud/multi-user.
- [ ] Object perlu `toJson` dan `fromJson`.
- [ ] List object bisa disimpan sebagai JSON string.
- [ ] Saat app dibuka, data perlu di-load dari storage.
- [ ] Saat data berubah, storage perlu ikut di-update.
- [ ] UI tetap membutuhkan state, bukan hanya storage.

Jika checklist ini sudah aman, lanjut ke **Shared Preferences untuk Pemula**.
