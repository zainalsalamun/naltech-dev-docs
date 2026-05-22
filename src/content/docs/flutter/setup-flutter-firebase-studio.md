---
title: "Setup Project Flutter di Firebase Studio"
description: "Panduan lengkap setup project Flutter di Firebase Studio: membuat workspace, import project, menjalankan preview, konfigurasi Firebase, FlutterFire CLI, dan troubleshooting."
category: "Flutter"
level: "Setup"
order: 25
tags: ["flutter", "firebase", "firebase-studio", "setup", "flutterfire"]
updated: "2026-05-21"
---

# Setup Project Flutter di Firebase Studio

Firebase Studio adalah cloud-based development environment dari Firebase/Google untuk membuat, mengedit, menjalankan, dan mengembangkan aplikasi langsung dari browser. Untuk Flutter, Firebase Studio bisa dipakai sebagai workspace online sehingga kita tidak selalu bergantung pada setup lokal di laptop.

Materi ini membahas setup project Flutter di Firebase Studio dari awal sampai siap dikembangkan.

Yang akan dipelajari:

- Apa itu Firebase Studio.
- Kapan cocok memakai Firebase Studio.
- Membuat project Flutter baru.
- Mengimpor project Flutter dari GitHub.
- Menjalankan `flutter pub get`.
- Menjalankan preview Flutter.
- Menghubungkan project Flutter ke Firebase.
- Setup FlutterFire CLI.
- Struktur file penting.
- Troubleshooting error umum.

---

## 1. Apa Itu Firebase Studio

Firebase Studio adalah IDE berbasis browser untuk membuat dan mengembangkan aplikasi. Di dalamnya sudah ada editor kode, terminal, preview aplikasi, integrasi Firebase, dan bantuan AI dari Gemini in Firebase.

Firebase Studio cocok untuk:

- Belajar Flutter tanpa setup lokal yang berat.
- Membuka project dari mana saja.
- Membuat prototype aplikasi dengan cepat.
- Mengembangkan project yang tersimpan di GitHub.
- Mencoba integrasi Firebase seperti Authentication, Firestore, Hosting, atau Cloud Functions.

Hal penting:

- Firebase Studio berjalan di cloud workspace.
- Project tetap sebaiknya disimpan di GitHub agar aman.
- Untuk Flutter, Firebase Studio menyediakan preview Android dan Chrome.
- Firebase Studio masih berada dalam status Preview, jadi fitur dan UI bisa berubah sewaktu-waktu.

---

## 2. Kapan Memakai Firebase Studio

Gunakan Firebase Studio jika:

- Laptop belum siap untuk setup Flutter lengkap.
- Ingin belajar dari browser.
- Ingin cepat mencoba project Flutter.
- Ingin workspace yang bisa dibuka dari device berbeda.
- Ingin memanfaatkan bantuan AI untuk membaca, membuat, atau memperbaiki kode.

Tetap gunakan setup lokal jika:

- Project sudah besar dan butuh performa tinggi.
- Perlu debugging native yang lebih dalam.
- Perlu build release Android/iOS secara serius.
- Perlu akses file, emulator, atau tooling lokal tertentu.

Rekomendasi untuk pemula:

```text
Belajar dan prototype -> Firebase Studio
Project produksi serius -> lokal + GitHub + Firebase Studio sebagai pendamping
```

---

## 3. Persiapan Sebelum Mulai

Sebelum setup, siapkan:

- Akun Google.
- Akun GitHub jika ingin import project.
- Dasar penggunaan terminal.
- Dasar Flutter seperti `flutter pub get` dan `flutter run`.

Jika ingin menghubungkan ke Firebase, siapkan juga:

- Firebase project di Firebase Console.
- Package name Android, misalnya `com.example.task_manager`.
- Bundle ID iOS jika nanti menargetkan iOS, misalnya `com.example.taskManager`.

Untuk tahap belajar, fokus dulu ke Android dan Web/Chrome.

---

## 4. Cara 1: Membuat Project Flutter Baru di Firebase Studio

Langkah umum:

1. Buka Firebase Studio.
2. Login memakai akun Google.
3. Pilih opsi membuat workspace baru.
4. Cari template Flutter jika tersedia.
5. Pilih template Flutter.
6. Beri nama workspace, misalnya `flutter-task-manager`.
7. Tunggu workspace selesai dibuat.

Setelah workspace terbuka, biasanya kamu akan melihat:

```text
lib/
android/
ios/
web/
pubspec.yaml
```

Jika template Flutter belum langsung menyediakan project, kamu bisa membuat project dari terminal:

```bash
flutter create task_manager
cd task_manager
flutter pub get
```

Lalu jalankan:

```bash
flutter doctor
```

Tujuannya untuk mengecek apakah Flutter environment di workspace sudah siap.

---

## 5. Cara 2: Import Project Flutter dari GitHub

Cara ini cocok jika project sudah ada di GitHub.

Langkah:

1. Buka Firebase Studio.
2. Klik **Import a project**.
3. Masukkan URL repository GitHub, GitLab, atau Bitbucket.
4. Masukkan nama project.
5. Jika project adalah Flutter app, aktifkan pilihan **This is a Flutter app**.
6. Klik **Import**.
7. Jika repository private, ikuti proses autentikasi.

Setelah import selesai, buka terminal di Firebase Studio dan jalankan:

```bash
flutter pub get
```

Kenapa perlu `flutter pub get`?

Karena saat project di-import, dependency Flutter belum tentu otomatis di-install. Command ini membaca `pubspec.yaml`, lalu mengambil package yang dibutuhkan project.

Jika ada error dependency, coba:

```bash
flutter clean
flutter pub get
```

---

## 6. Cara 3: Upload Project ZIP

Jika project belum ada di GitHub, kamu bisa upload archive.

Langkah:

1. Zip folder project Flutter.
2. Pastikan ukuran file tidak terlalu besar.
3. Buka Firebase Studio.
4. Pilih upload/import project.
5. Upload file `.zip`.
6. Setelah workspace terbuka, jalankan:

```bash
flutter pub get
```

Catatan:

- Jangan masukkan folder build ke ZIP.
- Jangan masukkan file yang tidak perlu.
- Lebih baik pakai GitHub untuk project jangka panjang.

Contoh file/folder yang tidak perlu ikut:

```text
build/
.dart_tool/
.idea/
.vscode/
```

---

## 7. Menjalankan Project Flutter

Setelah dependency selesai, cek device yang tersedia:

```bash
flutter devices
```

Biasanya Firebase Studio menyediakan preview untuk Flutter seperti:

- Android preview
- Chrome preview

Untuk menjalankan di Chrome:

```bash
flutter run -d chrome
```

Untuk menjalankan di Android emulator:

```bash
flutter run
```

Jika ada beberapa device:

```bash
flutter run -d <device_id>
```

Contoh:

```bash
flutter run -d chrome
```

Saat aplikasi berjalan, coba ubah teks di `lib/main.dart`, lalu simpan file. Flutter biasanya mendukung hot reload atau hot restart sesuai mode preview.

---

## 8. File Penting di Project Flutter

File dan folder yang paling sering dipakai:

```text
lib/
  main.dart
pubspec.yaml
android/
ios/
web/
```

Penjelasan:

- `lib/main.dart`: entry point aplikasi Flutter.
- `pubspec.yaml`: daftar dependency, asset, font, dan informasi project.
- `android/`: konfigurasi Android.
- `ios/`: konfigurasi iOS.
- `web/`: konfigurasi Flutter Web.

Untuk project yang mulai rapi, struktur `lib/` bisa dibuat seperti ini:

```text
lib/
  main.dart
  app.dart
  models/
  pages/
  widgets/
  services/
```

Jika memakai Firebase:

```text
lib/
  firebase_options.dart
```

File `firebase_options.dart` biasanya dibuat otomatis oleh FlutterFire CLI.

---

## 9. Menghubungkan Flutter ke Firebase

Jika project Flutter ingin memakai Firebase Authentication, Firestore, Storage, Analytics, atau service Firebase lain, project harus dikonfigurasi dengan Firebase.

Langkah umum:

1. Buat Firebase project di Firebase Console.
2. Install Firebase CLI.
3. Login Firebase dari terminal.
4. Install FlutterFire CLI.
5. Jalankan `flutterfire configure`.
6. Tambahkan package Firebase di Flutter.
7. Inisialisasi Firebase di `main.dart`.

---

## 10. Install Firebase CLI

Di terminal Firebase Studio, cek apakah Firebase CLI sudah tersedia:

```bash
firebase --version
```

Jika belum tersedia, ikuti cara install Firebase CLI sesuai dokumentasi Firebase.

Setelah tersedia, login:

```bash
firebase login
```

Jika login berbasis browser tidak berjalan mulus di workspace cloud, gunakan opsi login yang disediakan Firebase CLI atau login dari environment yang mendukung browser.

Setelah login, cek daftar project:

```bash
firebase projects:list
```

---

## 11. Install FlutterFire CLI

FlutterFire CLI dipakai untuk menghubungkan project Flutter dengan Firebase.

Install:

```bash
dart pub global activate flutterfire_cli
```

Pastikan command `flutterfire` bisa dipanggil:

```bash
flutterfire --version
```

Jika command tidak ditemukan, tambahkan path pub cache ke environment.

Biasanya path-nya:

```bash
export PATH="$PATH":"$HOME/.pub-cache/bin"
```

Setelah itu cek ulang:

```bash
flutterfire --version
```

---

## 12. Jalankan FlutterFire Configure

Dari root project Flutter, jalankan:

```bash
flutterfire configure
```

Ikuti pilihan yang muncul:

1. Pilih Firebase project.
2. Pilih platform yang dipakai, misalnya Android dan Web.
3. Masukkan Android package name jika diminta.
4. Tunggu proses selesai.

Output yang biasanya dibuat:

```text
lib/firebase_options.dart
```

File ini berisi konfigurasi Firebase untuk setiap platform.

Jangan edit file ini sembarangan. Jika konfigurasi berubah, jalankan ulang:

```bash
flutterfire configure
```

---

## 13. Tambahkan Package Firebase

Package minimal:

```bash
flutter pub add firebase_core
```

Jika ingin memakai Firestore:

```bash
flutter pub add cloud_firestore
```

Jika ingin memakai Authentication:

```bash
flutter pub add firebase_auth
```

Jika ingin memakai Storage:

```bash
flutter pub add firebase_storage
```

Setelah menambah package:

```bash
flutter pub get
```

---

## 14. Inisialisasi Firebase di main.dart

Ubah `lib/main.dart`:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/material.dart';

import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const MyApp());
}
```

Penjelasan:

- `WidgetsFlutterBinding.ensureInitialized()` memastikan Flutter siap sebelum menjalankan kode async.
- `Firebase.initializeApp()` menghubungkan aplikasi dengan Firebase.
- `DefaultFirebaseOptions.currentPlatform` mengambil konfigurasi sesuai platform.

Jika lupa inisialisasi Firebase, biasanya akan muncul error saat memakai Firebase service.

---

## 15. Contoh Test Koneksi Firestore

Jika memakai Firestore, coba buat function sederhana:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

Future<void> addTestData() async {
  await FirebaseFirestore.instance.collection('notes').add({
    'title': 'Belajar Firebase Studio',
    'createdAt': FieldValue.serverTimestamp(),
  });
}
```

Panggil dari tombol:

```dart
ElevatedButton(
  onPressed: addTestData,
  child: const Text('Tambah Data Test'),
)
```

Lalu cek Firebase Console:

```text
Firestore Database -> Data -> notes
```

Jika data muncul, koneksi Flutter ke Firebase berhasil.

---

## 16. Konfigurasi dev.nix di Firebase Studio

Firebase Studio memakai file `.idx/dev.nix` untuk mengatur environment workspace.

File ini bisa mengatur:

- tool yang tersedia di terminal
- extension editor
- command preview
- environment variable

Contoh konsep sederhana:

```nix
{ pkgs, ... }: {
  channel = "stable-23.11";

  packages = [
    pkgs.flutter
  ];

  idx.previews = {
    enable = true;
  };
}
```

Catatan:

- Jika membuat project dari template Flutter, biasanya konfigurasi workspace sudah disiapkan.
- Jika import project, kamu mungkin perlu menyesuaikan `.idx/dev.nix`.
- Jangan ubah `dev.nix` terlalu banyak sebelum memahami efeknya.

Jika dependency ingin otomatis di-install saat workspace dibuat, kamu bisa menambahkan hook setup di konfigurasi workspace. Untuk Flutter, command yang biasanya dibutuhkan adalah:

```bash
flutter pub get
```

---

## 17. Workflow yang Disarankan

Workflow belajar:

```text
Buat workspace Firebase Studio
-> buat/import project Flutter
-> flutter pub get
-> jalankan preview
-> edit UI
-> hot reload
-> commit ke GitHub
```

Workflow dengan Firebase:

```text
Buat Firebase project
-> firebase login
-> install FlutterFire CLI
-> flutterfire configure
-> flutter pub add firebase_core
-> initialize Firebase
-> tambah service sesuai kebutuhan
```

Workflow kerja harian:

```bash
git pull
flutter pub get
flutter run -d chrome
```

Sebelum selesai:

```bash
flutter analyze
git status
git add .
git commit -m "Update Flutter project"
git push
```

---

## 18. Troubleshooting

### flutter: command not found

Artinya Flutter belum tersedia di environment.

Solusi:

- Pastikan workspace memakai template Flutter.
- Cek `.idx/dev.nix`.
- Rebuild environment jika Firebase Studio meminta.

### Package tidak ditemukan

Jalankan:

```bash
flutter pub get
```

Jika masih error:

```bash
flutter clean
flutter pub get
```

### flutterfire: command not found

Install FlutterFire CLI:

```bash
dart pub global activate flutterfire_cli
```

Tambahkan path:

```bash
export PATH="$PATH":"$HOME/.pub-cache/bin"
```

### Firebase belum login

Jalankan:

```bash
firebase login
```

Lalu cek:

```bash
firebase projects:list
```

### Firebase.initializeApp error

Cek:

- Package `firebase_core` sudah terpasang.
- File `lib/firebase_options.dart` sudah ada.
- `Firebase.initializeApp()` sudah dipanggil sebelum `runApp`.
- Import `firebase_options.dart` sudah benar.

### Android package name salah

Cek file:

```text
android/app/build.gradle
```

Atau pada project Flutter baru:

```text
android/app/build.gradle.kts
```

Pastikan package name sesuai dengan konfigurasi Firebase.

Jika berubah, jalankan ulang:

```bash
flutterfire configure
```

---

## 19. Checklist Setup Firebase Studio

Pastikan checklist berikut sudah aman:

- [ ] Bisa membuka Firebase Studio.
- [ ] Bisa membuat atau import project Flutter.
- [ ] Bisa menjalankan `flutter pub get`.
- [ ] Bisa menjalankan preview Flutter.
- [ ] Bisa membuka terminal di Firebase Studio.
- [ ] Bisa commit project ke GitHub.
- [ ] Bisa login Firebase CLI.
- [ ] Bisa install FlutterFire CLI.
- [ ] Bisa menjalankan `flutterfire configure`.
- [ ] File `firebase_options.dart` berhasil dibuat.
- [ ] `firebase_core` sudah ditambahkan.
- [ ] `Firebase.initializeApp()` sudah dipasang di `main.dart`.

Jika checklist ini sudah selesai, project Flutter sudah siap memakai layanan Firebase.

---

## 20. Rekomendasi Lanjutan

Setelah setup Firebase Studio selesai, urutan belajar yang cocok:

1. Firebase Authentication untuk login/register.
2. Cloud Firestore untuk database online.
3. Firebase Storage untuk upload gambar/file.
4. Firebase Hosting untuk Flutter Web.
5. Firebase Cloud Messaging untuk notifikasi.

Untuk project Task Manager, langkah berikutnya bisa dibuat:

```text
Task Manager lokal
-> simpan ke local storage
-> sinkron ke Firestore
-> tambah login user
-> task per user
```

Dengan urutan ini, aplikasi berkembang pelan-pelan dari lokal, lalu online, lalu multi-user.

---

## Referensi Resmi

- [Firebase Studio documentation](https://firebase.google.com/docs/studio)
- [Get started with an existing project in Firebase Studio](https://firebase.google.com/docs/studio/get-started-import)
- [Customize your Firebase Studio workspace](https://firebase.google.com/docs/studio/customize-workspace)
- [Debug your app in Firebase Studio](https://firebase.google.com/docs/studio/debug)
- [Add Firebase to your Flutter app](https://firebase.google.com/docs/flutter/setup)
