---
title: "Firestore Security Rules Dasar"
description: "Panduan dasar Cloud Firestore Security Rules untuk Flutter: auth.uid, read, create, update, delete, validasi field, owner data, dan testing rules."
category: "Flutter"
level: "Firebase"
order: 74
tags: ["flutter", "firebase", "firestore", "security-rules", "auth"]
updated: "2026-05-23"
---

# Firestore Security Rules Dasar

Materi ini adalah lanjutan dari **Task Manager Online per User**.

Di materi sebelumnya kita sudah membuat task yang disimpan berdasarkan `userId`. Sekarang kita akan belajar cara melindungi data tersebut dengan **Cloud Firestore Security Rules**.

Security Rules penting karena aplikasi client seperti Flutter tidak boleh dipercaya sepenuhnya. Walaupun UI kita hanya menampilkan task milik user login, user yang paham teknis tetap bisa mencoba mengakses data lain langsung ke Firestore. Di sinilah rules bekerja.

Target materi:

- memahami fungsi Security Rules
- memahami `request.auth`
- memahami `request.auth.uid`
- membatasi akses data per user
- membedakan `resource.data` dan `request.resource.data`
- membuat rules untuk create, read, update, delete
- validasi field sederhana
- memahami error `permission-denied`
- testing rules secara manual

---

## 1. Apa itu Firestore Security Rules?

Firestore Security Rules adalah aturan keamanan yang menentukan siapa boleh membaca atau menulis data di Cloud Firestore.

Contoh pertanyaan yang dijawab oleh rules:

- apakah user sudah login?
- apakah data ini milik user yang sedang login?
- apakah user boleh membuat data baru?
- apakah user boleh mengubah field tertentu?
- apakah user boleh menghapus document?
- apakah bentuk data yang dikirim valid?

Rules berjalan di sisi Firebase, bukan di aplikasi Flutter. Jadi walaupun seseorang memodifikasi aplikasi client, rules tetap menjadi penjaga terakhir di server.

---

## 2. Kenapa Rules Wajib?

Misalnya aplikasi Flutter punya query:

```dart
FirebaseFirestore.instance
    .collection('tasks')
    .where('userId', isEqualTo: uid)
    .snapshots();
```

Query ini sudah benar di sisi aplikasi karena hanya mengambil task milik user login.

Tetapi query di aplikasi saja belum cukup. Tanpa rules yang benar, orang lain bisa mencoba membaca collection `tasks` secara langsung.

Jadi kita butuh dua lapis:

- Flutter query membatasi data yang diminta
- Firestore Security Rules membatasi data yang diizinkan

Keduanya harus sejalan.

---

## 3. Rules Bukan Filter

Ini konsep yang sangat penting.

Security Rules bukan filter data otomatis.

Artinya, kalau rules hanya mengizinkan user membaca task miliknya, query Flutter juga harus meminta task miliknya.

Contoh rules:

```text
allow read: if request.auth != null
  && resource.data.userId == request.auth.uid;
```

Query yang benar:

```dart
FirebaseFirestore.instance
    .collection('tasks')
    .where('userId', isEqualTo: uid)
    .get();
```

Query yang salah:

```dart
FirebaseFirestore.instance
    .collection('tasks')
    .get();
```

Walaupun nanti aplikasi hanya ingin menampilkan data user tertentu, Firestore akan menolak query kedua karena query itu berpotensi membaca data semua user.

Jadi ingat:

> Rules mengecek apakah sebuah request boleh dilakukan, bukan menyaring hasil query untuk kita.

---

## 4. Struktur Rules Dasar

Contoh struktur dasar:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read, write: if false;
    }
  }
}
```

Penjelasan:

- `rules_version = '2'` memakai versi rules terbaru
- `service cloud.firestore` berarti aturan untuk Cloud Firestore
- `match /databases/{database}/documents` adalah root document database
- `match /tasks/{taskId}` berarti aturan berlaku untuk collection `tasks`
- `allow read, write: if false` berarti semua akses ditolak

Rules paling aman adalah menolak semua dulu, lalu buka akses sedikit demi sedikit sesuai kebutuhan.

---

## 5. Mengenal request.auth

`request.auth` berisi informasi user yang sedang login.

Kalau user belum login:

```text
request.auth == null
```

Kalau user sudah login:

```text
request.auth != null
```

UID user login bisa dibaca lewat:

```text
request.auth.uid
```

Contoh rules hanya user login yang boleh membaca:

```text
allow read: if request.auth != null;
```

Rules ini sudah lebih aman daripada public access, tetapi belum cukup untuk data pribadi. Semua user login masih bisa membaca data semua user.

---

## 6. Data Task yang Akan Diamankan

Kita gunakan struktur document seperti ini:

```json
{
  "title": "Belajar Firestore Rules",
  "isDone": false,
  "userId": "uid_user_login",
  "createdAt": "server_timestamp",
  "updatedAt": "server_timestamp"
}
```

Field paling penting adalah:

```text
userId
```

Field ini menentukan siapa pemilik task.

---

## 7. Rules Read per User

Rules untuk membaca task milik sendiri:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read: if request.auth != null
        && resource.data.userId == request.auth.uid;
    }
  }
}
```

Penjelasan:

- `request.auth != null`: user wajib login
- `resource.data.userId`: `userId` dari data yang sudah ada di Firestore
- `request.auth.uid`: uid user yang sedang login
- akses hanya diberikan kalau keduanya sama

Dengan rules ini, user A tidak bisa membaca task milik user B.

---

## 8. Rules Create per User

Saat membuat document baru, data lama belum ada. Karena itu kita tidak bisa memakai `resource.data`.

Untuk data baru, gunakan:

```text
request.resource.data
```

Rules create:

```text
allow create: if request.auth != null
  && request.resource.data.userId == request.auth.uid;
```

Penjelasan:

- user wajib login
- data baru harus punya `userId`
- `userId` di data baru harus sama dengan uid user login

Ini mencegah user membuat task untuk user lain.

Contoh yang diizinkan:

```json
{
  "title": "Belajar Flutter",
  "isDone": false,
  "userId": "uid_user_login"
}
```

Contoh yang ditolak:

```json
{
  "title": "Task palsu",
  "isDone": false,
  "userId": "uid_user_lain"
}
```

---

## 9. Rules Update per User

Rules update perlu memastikan:

- user sudah login
- document lama memang milik user
- data baru tetap memakai `userId` yang sama

Contoh:

```text
allow update: if request.auth != null
  && resource.data.userId == request.auth.uid
  && request.resource.data.userId == resource.data.userId;
```

Penjelasan:

- `resource.data.userId == request.auth.uid` memastikan document lama milik user login
- `request.resource.data.userId == resource.data.userId` mencegah user mengganti pemilik task

Tanpa pengecekan kedua, user bisa mencoba mengubah `userId` document.

---

## 10. Rules Delete per User

Untuk delete, cukup pastikan document yang akan dihapus adalah milik user login:

```text
allow delete: if request.auth != null
  && resource.data.userId == request.auth.uid;
```

Delete tidak memakai `request.resource.data` karena setelah delete tidak ada data baru.

---

## 11. Rules CRUD Lengkap

Gabungan rules dasar:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read: if request.auth != null
        && resource.data.userId == request.auth.uid;

      allow create: if request.auth != null
        && request.resource.data.userId == request.auth.uid;

      allow update: if request.auth != null
        && resource.data.userId == request.auth.uid
        && request.resource.data.userId == resource.data.userId;

      allow delete: if request.auth != null
        && resource.data.userId == request.auth.uid;
    }
  }
}
```

Rules ini sudah cukup untuk tahap awal belajar aplikasi task per user.

---

## 12. Membuat Helper Function

Rules bisa dibuat lebih rapi dengan function.

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      function isSignedIn() {
        return request.auth != null;
      }

      function isOwner() {
        return resource.data.userId == request.auth.uid;
      }

      function isCreatingOwnTask() {
        return request.resource.data.userId == request.auth.uid;
      }

      function keepsSameOwner() {
        return request.resource.data.userId == resource.data.userId;
      }

      allow read: if isSignedIn() && isOwner();
      allow create: if isSignedIn() && isCreatingOwnTask();
      allow update: if isSignedIn() && isOwner() && keepsSameOwner();
      allow delete: if isSignedIn() && isOwner();
    }
  }
}
```

Kelebihan function:

- rules lebih mudah dibaca
- kondisi tidak terlalu panjang
- logic bisa dipakai ulang
- lebih mudah dikembangkan

---

## 13. Validasi Field

Rules juga bisa memvalidasi bentuk data.

Misalnya task hanya boleh punya field:

- `title`
- `isDone`
- `userId`
- `createdAt`
- `updatedAt`

Tambahkan function:

```text
function hasOnlyAllowedFields() {
  return request.resource.data.keys().hasOnly([
    'title',
    'isDone',
    'userId',
    'createdAt',
    'updatedAt'
  ]);
}
```

Rules ini mencegah user mengirim field aneh seperti:

```json
{
  "role": "admin"
}
```

---

## 14. Validasi Tipe Data

Kita juga bisa memastikan tipe data benar.

```text
function hasValidTypes() {
  return request.resource.data.title is string
    && request.resource.data.isDone is bool
    && request.resource.data.userId is string;
}
```

Dengan ini:

- `title` harus string
- `isDone` harus boolean
- `userId` harus string

Contoh data yang ditolak:

```json
{
  "title": 123,
  "isDone": "belum",
  "userId": true
}
```

---

## 15. Validasi Panjang Title

Title sebaiknya tidak kosong dan tidak terlalu panjang.

```text
function hasValidTitle() {
  return request.resource.data.title.size() > 0
    && request.resource.data.title.size() <= 100;
}
```

Dengan rules ini:

- title kosong ditolak
- title lebih dari 100 karakter ditolak

Validasi ini tetap perlu dilakukan juga di Flutter. Rules adalah pengaman server, bukan pengganti validasi UI.

---

## 16. Rules Lengkap dengan Validasi

Contoh rules yang lebih lengkap:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      function isSignedIn() {
        return request.auth != null;
      }

      function isOwner() {
        return resource.data.userId == request.auth.uid;
      }

      function isCreatingOwnTask() {
        return request.resource.data.userId == request.auth.uid;
      }

      function keepsSameOwner() {
        return request.resource.data.userId == resource.data.userId;
      }

      function hasOnlyAllowedFields() {
        return request.resource.data.keys().hasOnly([
          'title',
          'isDone',
          'userId',
          'createdAt',
          'updatedAt'
        ]);
      }

      function hasValidTypes() {
        return request.resource.data.title is string
          && request.resource.data.isDone is bool
          && request.resource.data.userId is string;
      }

      function hasValidTitle() {
        return request.resource.data.title.size() > 0
          && request.resource.data.title.size() <= 100;
      }

      function hasValidTaskData() {
        return hasOnlyAllowedFields()
          && hasValidTypes()
          && hasValidTitle();
      }

      allow read: if isSignedIn() && isOwner();

      allow create: if isSignedIn()
        && isCreatingOwnTask()
        && hasValidTaskData();

      allow update: if isSignedIn()
        && isOwner()
        && keepsSameOwner()
        && hasValidTaskData();

      allow delete: if isSignedIn() && isOwner();
    }
  }
}
```

Ini adalah rules yang lebih cocok untuk aplikasi belajar yang mulai mendekati aplikasi nyata.

---

## 17. Query Flutter Harus Sesuai Rules

Kalau rules membaca data berdasarkan `userId`, query Flutter juga harus menyertakan `userId`.

Benar:

```dart
final uid = FirebaseAuth.instance.currentUser!.uid;

FirebaseFirestore.instance
    .collection('tasks')
    .where('userId', isEqualTo: uid)
    .orderBy('createdAt', descending: true)
    .snapshots();
```

Salah:

```dart
FirebaseFirestore.instance
    .collection('tasks')
    .orderBy('createdAt', descending: true)
    .snapshots();
```

Query kedua akan ditolak karena Firestore melihat query itu berpotensi membaca task semua user.

---

## 18. Mengatasi Permission Denied

Error yang sering muncul:

```text
cloud_firestore/permission-denied
```

Penyebab umum:

- user belum login
- query tidak memakai `where('userId', isEqualTo: uid)`
- data baru tidak mengirim `userId`
- `userId` yang dikirim tidak sama dengan uid user login
- rules terlalu ketat
- field yang dikirim tidak sesuai validasi

Cara debug:

1. cek apakah `FirebaseAuth.instance.currentUser` tidak null
2. print uid user login
3. cek data yang dikirim ke Firestore
4. cek field `userId`
5. cek query sudah sesuai rules
6. coba rules sederhana dulu
7. tambah validasi sedikit demi sedikit

Contoh debug di Flutter:

```dart
final user = FirebaseAuth.instance.currentUser;
debugPrint('UID: ${user?.uid}');
```

---

## 19. Testing Manual dengan Dua Akun

Testing rules jangan hanya memakai satu akun.

Gunakan skenario:

1. login dengan akun A
2. buat task dari akun A
3. pastikan field `userId` sama dengan uid akun A
4. logout
5. login dengan akun B
6. pastikan task akun A tidak muncul
7. buat task akun B
8. pastikan field `userId` sama dengan uid akun B
9. logout
10. login lagi dengan akun A
11. pastikan task akun A masih muncul
12. pastikan task akun B tidak muncul

Kalau task akun lain muncul, berarti query atau rules masih salah.

---

## 20. Testing dari Firebase Console

Firebase Console menyediakan Rules Playground untuk simulasi rules.

Yang bisa dites:

- read document dengan user login
- read document tanpa login
- create document dengan `userId` benar
- create document dengan `userId` user lain
- update title
- update `userId`
- delete document milik sendiri
- delete document milik orang lain

Rules yang baik harus:

- mengizinkan aksi yang benar
- menolak aksi yang salah

Jangan hanya memastikan fitur berhasil. Pastikan juga aksi berbahaya gagal.

---

## 21. Kesalahan Umum Pemula

### Membuka semua akses

Contoh rules berbahaya:

```text
allow read, write: if true;
```

Rules ini berarti semua orang boleh membaca dan menulis semua data.

### Hanya cek login

```text
allow read, write: if request.auth != null;
```

Ini lebih baik daripada public, tetapi semua user login masih bisa mengakses data semua user.

### Tidak mengunci userId saat update

```text
allow update: if resource.data.userId == request.auth.uid;
```

Rules ini belum cukup karena user bisa mencoba mengganti `userId` di data baru.

Tambahkan:

```text
request.resource.data.userId == resource.data.userId
```

### Query tidak sesuai rules

Rules sudah benar, tetapi query Flutter tidak memakai `where userId`. Hasilnya tetap `permission-denied`.

---

## 22. Checklist

Checklist setelah mempelajari materi ini:

- paham fungsi Firestore Security Rules
- paham `request.auth`
- paham `request.auth.uid`
- paham bedanya `resource.data` dan `request.resource.data`
- bisa membuat rules read per user
- bisa membuat rules create per user
- bisa membuat rules update per user
- bisa membuat rules delete per user
- bisa validasi field sederhana
- bisa debug `permission-denied`
- bisa testing dengan dua akun

---

## 23. Kesimpulan

Firestore Security Rules adalah bagian wajib saat membuat aplikasi Firebase.

Untuk aplikasi Task Manager per user, prinsip utamanya:

- user harus login
- document harus punya `userId`
- `userId` harus sama dengan `request.auth.uid`
- query Flutter harus sesuai rules
- update tidak boleh mengganti pemilik data
- validasi data tetap perlu di server

Setelah rules berjalan dengan benar, aplikasi menjadi jauh lebih aman untuk dikembangkan ke tahap berikutnya.

---

## 24. Selanjutnya

Materi berikutnya yang cocok adalah **Repository Pattern dengan Firebase**.

Di materi itu kita akan merapikan kode agar aplikasi tidak terlalu bergantung langsung pada Firestore di halaman UI.

Referensi resmi:

- [Firestore Security Rules Overview](https://firebase.google.com/docs/firestore/security/overview)
- [Securely Query Data](https://firebase.google.com/docs/firestore/security/rules-query)
- [Writing Conditions for Security Rules](https://firebase.google.com/docs/firestore/security/rules-conditions)
- [Get Started with Firebase Auth Flutter](https://firebase.google.com/docs/auth/flutter/start)
