---
title: "Shared Preferences untuk Pemula"
description: "Tutorial memakai shared_preferences di Flutter: install package, simpan String/int/bool, simpan object dengan JSON, load data saat app dibuka, dan contoh mini profile app."
category: "Flutter"
level: "Storage"
order: 56
tags: ["flutter", "shared-preferences", "local-storage", "json", "storage"]
updated: "2026-05-23"
---

# Shared Preferences untuk Pemula

`shared_preferences` adalah package Flutter untuk menyimpan data sederhana secara lokal di device. Package ini cocok untuk data kecil seperti setting aplikasi, status onboarding, theme mode, nama user, token sederhana, atau cache ringan.

Materi ini membahas:

- install package
- menyimpan `String`
- menyimpan `int`
- menyimpan `bool`
- membaca data
- menghapus data
- menyimpan object dengan JSON
- load data saat app dibuka

---

## 1. Kapan Memakai shared_preferences

Gunakan `shared_preferences` untuk data kecil.

Contoh yang cocok:

```text
themeMode = "dark"
isOnboardingDone = true
userName = "Budi"
lastOpenedPage = 2
```

Contoh yang kurang cocok:

```text
ribuan task
data transaksi besar
relasi tabel kompleks
chat history panjang
file gambar/video
```

Jika data mulai besar atau butuh query, gunakan Hive/Isar atau SQLite. Jika data harus online dan multi-user, gunakan Firestore atau backend API.

Catatan penting:

`shared_preferences` hanya menyimpan tipe data sederhana seperti `String`, `int`, `double`, `bool`, dan `List<String>`. Jika ingin menyimpan object, object perlu diubah menjadi JSON string.

---

## 2. Install Package

Jalankan command:

```bash
flutter pub add shared_preferences
```

Lalu:

```bash
flutter pub get
```

Import di file Dart:

```dart
import 'package:shared_preferences/shared_preferences.dart';
```

Untuk memakai JSON, tambahkan import:

```dart
import 'dart:convert';
```

---

## 3. Konsep Key-Value

`shared_preferences` menyimpan data dengan pola key-value.

Contoh:

```text
key: "userName"
value: "Budi"
```

Saat menyimpan:

```dart
await prefs.setString('userName', 'Budi');
```

Saat membaca:

```dart
final userName = prefs.getString('userName');
```

Key harus konsisten. Jika saat menyimpan pakai key `userName`, saat membaca juga harus pakai `userName`.

Kesalahan umum:

```dart
await prefs.setString('username', 'Budi');
final name = prefs.getString('userName');
```

Data tidak terbaca karena key berbeda: `username` dan `userName`.

---

## 4. Menyimpan String

Contoh menyimpan nama user:

```dart
Future<void> saveUserName(String name) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('userName', name);
}
```

Membaca:

```dart
Future<String?> loadUserName() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('userName');
}
```

Contoh penggunaan:

```dart
await saveUserName('Budi');

final name = await loadUserName();
print(name);
```

Hasil:

```text
Budi
```

Perhatikan return type:

```dart
Future<String?>
```

Nilainya nullable karena bisa saja data belum pernah disimpan.

---

## 5. Menyimpan int

Contoh menyimpan jumlah app dibuka:

```dart
Future<void> saveOpenCount(int count) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setInt('openCount', count);
}
```

Membaca:

```dart
Future<int> loadOpenCount() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getInt('openCount') ?? 0;
}
```

Kenapa memakai `?? 0`?

Karena `getInt` bisa menghasilkan `null` jika data belum ada. Dengan `?? 0`, kita memberi nilai default.

Contoh menaikkan counter:

```dart
Future<void> increaseOpenCount() async {
  final prefs = await SharedPreferences.getInstance();
  final currentCount = prefs.getInt('openCount') ?? 0;
  await prefs.setInt('openCount', currentCount + 1);
}
```

---

## 6. Menyimpan bool

Contoh menyimpan status onboarding:

```dart
Future<void> saveOnboardingStatus(bool isDone) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setBool('isOnboardingDone', isDone);
}
```

Membaca:

```dart
Future<bool> loadOnboardingStatus() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getBool('isOnboardingDone') ?? false;
}
```

Contoh penggunaan:

```dart
final isDone = await loadOnboardingStatus();

if (isDone) {
  print('Buka halaman home');
} else {
  print('Buka halaman onboarding');
}
```

Pola ini sangat sering dipakai untuk menentukan halaman awal aplikasi.

---

## 7. Menghapus Data

Menghapus satu data berdasarkan key:

```dart
Future<void> removeUserName() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('userName');
}
```

Menghapus semua data:

```dart
Future<void> clearAllPreferences() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.clear();
}
```

Hati-hati memakai `clear()`, karena semua data yang disimpan oleh `shared_preferences` akan hilang.

Gunakan `remove()` jika hanya ingin menghapus satu data.

---

## 8. Membuat Keys agar Tidak Typo

Supaya key tidak tercecer dan typo, buat class khusus.

```dart
class PreferenceKeys {
  static const userName = 'userName';
  static const openCount = 'openCount';
  static const isOnboardingDone = 'isOnboardingDone';
}
```

Penggunaan:

```dart
await prefs.setString(PreferenceKeys.userName, 'Budi');
final name = prefs.getString(PreferenceKeys.userName);
```

Keuntungan:

- key lebih konsisten
- mudah dicari
- mengurangi typo
- lebih mudah refactor

---

## 9. Menyimpan Object dengan JSON

Misalnya punya model `UserProfile`.

```dart
class UserProfile {
  final String name;
  final int age;
  final bool isPremium;

  const UserProfile({
    required this.name,
    required this.age,
    required this.isPremium,
  });

  Map<String, dynamic> toJson() {
    return {
      'name': name,
      'age': age,
      'isPremium': isPremium,
    };
  }

  factory UserProfile.fromJson(Map<String, dynamic> json) {
    return UserProfile(
      name: json['name'] as String,
      age: json['age'] as int,
      isPremium: json['isPremium'] as bool,
    );
  }
}
```

Simpan object:

```dart
Future<void> saveUserProfile(UserProfile profile) async {
  final prefs = await SharedPreferences.getInstance();

  final jsonString = jsonEncode(profile.toJson());

  await prefs.setString('userProfile', jsonString);
}
```

Baca object:

```dart
Future<UserProfile?> loadUserProfile() async {
  final prefs = await SharedPreferences.getInstance();
  final jsonString = prefs.getString('userProfile');

  if (jsonString == null) {
    return null;
  }

  final jsonMap = jsonDecode(jsonString) as Map<String, dynamic>;
  return UserProfile.fromJson(jsonMap);
}
```

Alurnya:

```text
Object Dart
-> toJson
-> Map
-> jsonEncode
-> String
-> shared_preferences
```

Saat membaca:

```text
shared_preferences
-> String
-> jsonDecode
-> Map
-> fromJson
-> Object Dart
```

---

## 10. Load Data Saat App Dibuka

Biasanya data dibaca di `initState`.

Contoh:

```dart
class ProfilePage extends StatefulWidget {
  const ProfilePage({super.key});

  @override
  State<ProfilePage> createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  UserProfile? profile;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  Future<void> loadData() async {
    final result = await loadUserProfile();

    setState(() {
      profile = result;
      isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (profile == null) {
      return const Scaffold(
        body: Center(
          child: Text('Belum ada profile'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile'),
      ),
      body: Center(
        child: Text(profile!.name),
      ),
    );
  }
}
```

Penjelasan:

- `initState` dipanggil saat widget pertama kali dibuat.
- `loadData` membaca data dari storage.
- Selama membaca data, UI menampilkan loading.
- Jika data tidak ada, tampilkan empty state.
- Jika data ada, tampilkan profile.

---

## 11. Contoh Mini App: Profile Storage

Contoh ini menyimpan nama user ke `shared_preferences`.

```dart
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

class ProfileStoragePage extends StatefulWidget {
  const ProfileStoragePage({super.key});

  @override
  State<ProfileStoragePage> createState() => _ProfileStoragePageState();
}

class _ProfileStoragePageState extends State<ProfileStoragePage> {
  final nameController = TextEditingController();
  String? savedName;
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadName();
  }

  @override
  void dispose() {
    nameController.dispose();
    super.dispose();
  }

  Future<void> loadName() async {
    final prefs = await SharedPreferences.getInstance();
    final name = prefs.getString('userName');

    setState(() {
      savedName = name;
      nameController.text = name ?? '';
      isLoading = false;
    });
  }

  Future<void> saveName() async {
    final prefs = await SharedPreferences.getInstance();
    final name = nameController.text.trim();

    if (name.isEmpty) return;

    await prefs.setString('userName', name);

    setState(() {
      savedName = name;
    });
  }

  Future<void> deleteName() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove('userName');

    setState(() {
      savedName = null;
      nameController.clear();
    });
  }

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return const Scaffold(
        body: Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profile Storage'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Text(
              savedName == null
                  ? 'Belum ada nama tersimpan'
                  : 'Nama tersimpan: $savedName',
            ),
            const SizedBox(height: 12),
            TextField(
              controller: nameController,
              decoration: const InputDecoration(
                labelText: 'Nama',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            FilledButton(
              onPressed: saveName,
              child: const Text('Simpan'),
            ),
            const SizedBox(height: 8),
            OutlinedButton(
              onPressed: deleteName,
              child: const Text('Hapus'),
            ),
          ],
        ),
      ),
    );
  }
}
```

Cara mencoba:

1. Jalankan aplikasi.
2. Isi nama.
3. Tekan simpan.
4. Tutup aplikasi.
5. Buka lagi.
6. Nama harus tetap muncul.

---

## 12. Membuat Service Agar Rapi

Kalau semua kode storage ditulis di page, file UI akan panjang. Lebih rapi jika dibuat service.

Buat file:

```text
lib/services/preference_service.dart
```

Isi:

```dart
import 'package:shared_preferences/shared_preferences.dart';

class PreferenceService {
  static const _userNameKey = 'userName';
  static const _isOnboardingDoneKey = 'isOnboardingDone';

  Future<void> saveUserName(String name) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(_userNameKey, name);
  }

  Future<String?> loadUserName() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getString(_userNameKey);
  }

  Future<void> saveOnboardingDone(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_isOnboardingDoneKey, value);
  }

  Future<bool> loadOnboardingDone() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_isOnboardingDoneKey) ?? false;
  }
}
```

Penggunaan di page:

```dart
final preferenceService = PreferenceService();

final name = await preferenceService.loadUserName();
await preferenceService.saveUserName('Budi');
```

Keuntungan:

- UI lebih bersih
- storage logic terkumpul di satu tempat
- mudah diganti nanti jika pindah ke storage lain

---

## 13. Catatan API Baru shared_preferences

Versi terbaru `shared_preferences` juga menyediakan API seperti `SharedPreferencesAsync` dan `SharedPreferencesWithCache`.

Untuk pemula, pola `SharedPreferences.getInstance()` masih mudah dipahami dan banyak dipakai di contoh pembelajaran. Namun, jika aplikasi lebih kompleks, terutama punya banyak isolate atau perlu perilaku async yang lebih konsisten, pelajari API baru tersebut dari dokumentasi resmi.

Intinya:

- mulai dari pola sederhana dulu
- pahami key-value storage
- pahami save dan load
- setelah itu baru pelajari API yang lebih baru jika dibutuhkan

---

## 14. Kesalahan Umum

### Lupa await

Kurang tepat:

```dart
prefs.setString('userName', name);
```

Lebih aman:

```dart
await prefs.setString('userName', name);
```

### Key berbeda

```dart
await prefs.setString('user_name', 'Budi');
final name = prefs.getString('userName');
```

Data tidak terbaca karena key berbeda.

### Tidak memberi default value

```dart
final count = prefs.getInt('count');
```

`count` bisa null.

Lebih aman:

```dart
final count = prefs.getInt('count') ?? 0;
```

### Menyimpan object langsung

Tidak bisa:

```dart
await prefs.setString('profile', profile);
```

Harus diubah ke JSON string:

```dart
await prefs.setString(
  'profile',
  jsonEncode(profile.toJson()),
);
```

---

## 15. Checklist Shared Preferences

Pastikan sudah paham:

- [ ] Bisa install `shared_preferences`.
- [ ] Bisa menyimpan `String`.
- [ ] Bisa menyimpan `int`.
- [ ] Bisa menyimpan `bool`.
- [ ] Bisa membaca data dengan default value.
- [ ] Bisa menghapus data dengan `remove`.
- [ ] Bisa membuat key konstan agar tidak typo.
- [ ] Bisa membuat model `toJson` dan `fromJson`.
- [ ] Bisa menyimpan object sebagai JSON string.
- [ ] Bisa load data saat app dibuka.
- [ ] Bisa membuat service agar kode storage lebih rapi.

Jika checklist ini sudah aman, lanjut ke **Upgrade Task Manager dengan Shared Preferences**.

---

## Referensi Resmi

- [Store key-value data on disk - Flutter docs](https://docs.flutter.dev/cookbook/persistence/key-value)
- [shared_preferences package - pub.dev](https://pub.dev/packages/shared_preferences)
- [shared_preferences API docs](https://pub.dev/documentation/shared_preferences/latest/shared_preferences/)
