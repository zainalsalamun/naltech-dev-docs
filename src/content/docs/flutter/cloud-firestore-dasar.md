---
title: "Cloud Firestore Dasar"
description: "Pengenalan Cloud Firestore untuk Flutter: collection, document, path data per user, CRUD konsep, realtime stream, timestamp, query, dan security rules dasar."
category: "Flutter"
level: "Firebase"
order: 71
tags: ["flutter", "firebase", "firestore", "database", "crud"]
updated: "2026-05-23"
---

# Cloud Firestore Dasar

Cloud Firestore adalah database NoSQL dari Firebase untuk menyimpan data aplikasi secara online. Firestore cocok untuk aplikasi yang membutuhkan data realtime, sinkron antar device, dan data per user.

Materi ini adalah pengantar sebelum masuk ke **Firestore CRUD untuk Pemula**.

Yang akan dipelajari:

- apa itu Firestore
- collection dan document
- struktur data
- path data per user
- add, get, update, delete
- realtime stream
- timestamp
- query dasar
- security rules konsep dasar

---

## 1. Apa Itu Cloud Firestore

Cloud Firestore adalah database cloud. Artinya data disimpan di server Firebase, bukan hanya di device user.

Contoh penggunaan:

- task manager online
- notes online
- chat app
- data profile user
- habit tracker
- aplikasi inventory sederhana

Perbedaan dengan local storage:

| Local Storage | Firestore |
| --- | --- |
| Data di device | Data di cloud |
| Bisa offline | Bisa online dan sinkron |
| Hanya untuk satu device | Bisa antar device |
| Tidak butuh login | Biasanya butuh login |
| Cocok untuk cache/offline | Cocok untuk database aplikasi |

Firestore cocok setelah kita punya Firebase Authentication, karena data bisa disimpan berdasarkan `uid` user.

---

## 2. Konsep Collection dan Document

Firestore menyimpan data dalam bentuk:

```text
collection
-> document
-> field
```

Contoh:

```text
tasks
  task_001
    title: "Belajar Flutter"
    isDone: false
```

Penjelasan:

- `tasks` adalah collection.
- `task_001` adalah document.
- `title` dan `isDone` adalah field.

Analogi:

```text
Collection = folder
Document = file
Field = isi file
```

Contoh lain:

```text
users
  user_123
    email: "budi@example.com"
    name: "Budi"
```

---

## 3. Struktur Data Firestore

Firestore tidak memakai tabel seperti SQL. Firestore memakai collection dan document.

Contoh SQL:

```text
table users
table tasks
```

Contoh Firestore:

```text
users/{userId}
tasks/{taskId}
```

Atau dengan subcollection:

```text
users/{userId}/tasks/{taskId}
```

Untuk Task Manager per user, struktur yang disarankan:

```text
users
  {uid}
    email: "budi@example.com"
    createdAt: timestamp
    tasks
      {taskId}
        title: "Belajar Firestore"
        description: "CRUD online"
        status: "todo"
        createdAt: timestamp
        updatedAt: timestamp
```

Kenapa pakai `users/{uid}/tasks/{taskId}`?

- task user A terpisah dari user B
- security rules lebih mudah
- query task per user lebih jelas

---

## 4. Document ID

Document ID bisa dibuat otomatis oleh Firestore:

```dart
FirebaseFirestore.instance.collection('tasks').add(data);
```

Atau ditentukan sendiri:

```dart
FirebaseFirestore.instance.collection('tasks').doc(taskId).set(data);
```

Perbedaan:

| Cara | Cocok Untuk |
| --- | --- |
| `add()` | Firestore membuat id otomatis |
| `doc(id).set()` | Kita menentukan id sendiri |

Untuk task:

- `add()` cocok untuk membuat task baru
- `doc(task.id).set()` cocok jika id dibuat dari aplikasi

Untuk user:

```dart
doc(uid)
```

lebih cocok karena `uid` dari Firebase Auth adalah identitas user.

---

## 5. Install Package

Tambahkan package:

```bash
flutter pub add cloud_firestore
```

Pastikan juga sudah ada:

```bash
flutter pub add firebase_core
```

Import:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';
```

Pastikan Firebase sudah diinisialisasi:

```dart
await Firebase.initializeApp(
  options: DefaultFirebaseOptions.currentPlatform,
);
```

---

## 6. Membuat Reference

Reference adalah alamat ke collection atau document.

Collection reference:

```dart
final tasksRef = FirebaseFirestore.instance.collection('tasks');
```

Document reference:

```dart
final taskRef = FirebaseFirestore.instance
    .collection('tasks')
    .doc('task_001');
```

Path per user:

```dart
final userTasksRef = FirebaseFirestore.instance
    .collection('users')
    .doc(uid)
    .collection('tasks');
```

Jika user login:

```dart
final uid = FirebaseAuth.instance.currentUser!.uid;
```

Maka task collection user:

```dart
users/{uid}/tasks
```

---

## 7. Data Map

Firestore menyimpan data sebagai Map.

Contoh:

```dart
final data = {
  'title': 'Belajar Firestore',
  'description': 'Membuat CRUD online',
  'status': 'todo',
  'createdAt': FieldValue.serverTimestamp(),
};
```

Tipe data yang umum:

- `String`
- `int`
- `double`
- `bool`
- `List`
- `Map`
- `Timestamp`
- `null`

Untuk model Dart, biasanya kita membuat:

```dart
toJson()
fromJson()
```

Sama seperti local storage, tetapi timestamp perlu diperhatikan.

---

## 8. Create Data

Membuat document dengan id otomatis:

```dart
Future<void> addTask() async {
  await FirebaseFirestore.instance.collection('tasks').add({
    'title': 'Belajar Firestore',
    'description': 'CRUD online',
    'status': 'todo',
    'createdAt': FieldValue.serverTimestamp(),
  });
}
```

Membuat document dengan id tertentu:

```dart
Future<void> setTask(String taskId) async {
  await FirebaseFirestore.instance.collection('tasks').doc(taskId).set({
    'title': 'Belajar Firestore',
    'description': 'CRUD online',
    'status': 'todo',
    'createdAt': FieldValue.serverTimestamp(),
  });
}
```

Perbedaan:

- `add()` membuat id otomatis.
- `set()` menulis ke document tertentu.

---

## 9. Read Data Sekali

Membaca collection satu kali:

```dart
Future<void> getTasks() async {
  final snapshot = await FirebaseFirestore.instance
      .collection('tasks')
      .get();

  for (final doc in snapshot.docs) {
    print(doc.id);
    print(doc.data());
  }
}
```

Membaca document satu kali:

```dart
Future<void> getTask(String taskId) async {
  final snapshot = await FirebaseFirestore.instance
      .collection('tasks')
      .doc(taskId)
      .get();

  if (!snapshot.exists) {
    print('Task tidak ditemukan');
    return;
  }

  print(snapshot.data());
}
```

Gunakan `get()` jika hanya butuh membaca sekali.

---

## 10. Realtime Stream

Salah satu kekuatan Firestore adalah realtime.

Membaca collection realtime:

```dart
Stream<QuerySnapshot<Map<String, dynamic>>> taskStream() {
  return FirebaseFirestore.instance
      .collection('tasks')
      .snapshots();
}
```

Di UI:

```dart
StreamBuilder<QuerySnapshot<Map<String, dynamic>>>(
  stream: FirebaseFirestore.instance.collection('tasks').snapshots(),
  builder: (context, snapshot) {
    if (snapshot.connectionState == ConnectionState.waiting) {
      return const CircularProgressIndicator();
    }

    if (snapshot.hasError) {
      return Text('Error: ${snapshot.error}');
    }

    final docs = snapshot.data?.docs ?? [];

    return ListView.builder(
      itemCount: docs.length,
      itemBuilder: (context, index) {
        final data = docs[index].data();
        return ListTile(
          title: Text(data['title'] as String),
        );
      },
    );
  },
)
```

Jika data berubah di Firestore, UI akan ikut update.

---

## 11. Update Data

Update field tertentu:

```dart
Future<void> updateTask(String taskId) async {
  await FirebaseFirestore.instance.collection('tasks').doc(taskId).update({
    'title': 'Judul baru',
    'status': 'done',
    'updatedAt': FieldValue.serverTimestamp(),
  });
}
```

Catatan:

`update()` akan gagal jika document belum ada.

Jika ingin membuat document jika belum ada, gunakan `set()`.

---

## 12. Delete Data

Menghapus document:

```dart
Future<void> deleteTask(String taskId) async {
  await FirebaseFirestore.instance.collection('tasks').doc(taskId).delete();
}
```

Catatan penting:

Menghapus document tidak otomatis menghapus subcollection di dalamnya. Jika document punya subcollection, perlu strategi khusus untuk menghapus subcollection.

Untuk task sederhana tanpa subcollection, `delete()` sudah cukup.

---

## 13. Query Dasar

Filter berdasarkan field:

```dart
final snapshot = await FirebaseFirestore.instance
    .collection('tasks')
    .where('status', isEqualTo: 'done')
    .get();
```

Order berdasarkan tanggal:

```dart
final snapshot = await FirebaseFirestore.instance
    .collection('tasks')
    .orderBy('createdAt', descending: true)
    .get();
```

Limit data:

```dart
final snapshot = await FirebaseFirestore.instance
    .collection('tasks')
    .limit(20)
    .get();
```

Gabungan:

```dart
final snapshot = await FirebaseFirestore.instance
    .collection('tasks')
    .where('status', isEqualTo: 'todo')
    .orderBy('createdAt', descending: true)
    .limit(20)
    .get();
```

Firestore mungkin meminta index untuk query gabungan tertentu. Jika muncul link pembuatan index di error, ikuti link tersebut dari Firebase Console.

---

## 14. Timestamp

Gunakan server timestamp:

```dart
'createdAt': FieldValue.serverTimestamp(),
```

Kenapa?

Karena waktu dari device user bisa salah. Server timestamp memakai waktu server Firebase.

Saat membaca:

```dart
final timestamp = data['createdAt'] as Timestamp?;
final createdAt = timestamp?.toDate();
```

Jika document baru dibuat, `createdAt` bisa sementara `null` sampai server mengisi timestamp. Jadi parsing harus aman.

---

## 15. Model Task untuk Firestore

Contoh:

```dart
class Task {
  final String id;
  final String title;
  final String description;
  final String status;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
    this.createdAt,
    this.updatedAt,
  });

  Map<String, dynamic> toJson() {
    return {
      'title': title,
      'description': description,
      'status': status,
      'updatedAt': FieldValue.serverTimestamp(),
    };
  }

  factory Task.fromFirestore(
    DocumentSnapshot<Map<String, dynamic>> doc,
  ) {
    final data = doc.data()!;

    return Task(
      id: doc.id,
      title: data['title'] as String,
      description: data['description'] as String,
      status: data['status'] as String,
      createdAt: (data['createdAt'] as Timestamp?)?.toDate(),
      updatedAt: (data['updatedAt'] as Timestamp?)?.toDate(),
    );
  }
}
```

Catatan:

- `id` berasal dari `doc.id`.
- `createdAt` dan `updatedAt` bisa nullable.
- `FieldValue.serverTimestamp()` tidak sama dengan `DateTime`, jadi hati-hati saat typing.

---

## 16. Struktur Data Per User

Jika user sudah login:

```dart
final uid = FirebaseAuth.instance.currentUser!.uid;
```

Collection task per user:

```dart
FirebaseFirestore.instance
    .collection('users')
    .doc(uid)
    .collection('tasks');
```

Path:

```text
users/{uid}/tasks/{taskId}
```

Contoh add:

```dart
Future<void> addUserTask(String uid) async {
  await FirebaseFirestore.instance
      .collection('users')
      .doc(uid)
      .collection('tasks')
      .add({
        'title': 'Belajar Firestore',
        'status': 'todo',
        'createdAt': FieldValue.serverTimestamp(),
      });
}
```

Inilah struktur yang akan dipakai untuk Task Manager online.

---

## 17. Security Rules Konsep Dasar

Firestore harus dilindungi dengan security rules.

Konsep:

```text
User hanya boleh membaca dan menulis data miliknya sendiri.
```

Contoh rules konsep:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /users/{userId}/tasks/{taskId} {
      allow read, write: if request.auth != null
        && request.auth.uid == userId;
    }
  }
}
```

Artinya:

- user harus login
- `request.auth.uid` harus sama dengan `userId` di path

Jika user A punya uid `abc`, user A hanya boleh akses:

```text
users/abc/tasks
```

Tidak boleh akses:

```text
users/xyz/tasks
```

---

## 18. Firestore dan Biaya Read

Firestore menghitung operasi seperti read, write, dan delete.

Hal yang perlu dipahami:

- membaca document dihitung read
- menulis document dihitung write
- menghapus document dihitung delete
- stream realtime juga bisa menghasilkan read saat data berubah

Tips pemula:

- jangan stream collection besar tanpa limit
- gunakan query yang spesifik
- gunakan pagination jika data banyak
- jangan membaca semua data user jika hanya butuh sebagian

Untuk belajar, data kecil tidak masalah. Untuk production, desain query perlu dipikirkan.

---

## 19. Error Umum

### Permission denied

Biasanya karena security rules menolak request.

Cek:

- user sudah login atau belum
- path data sudah benar
- `uid` sesuai dengan rules
- rules sudah dipublish

### Missing or insufficient permissions

Ini juga biasanya rules.

Solusi:

- cek Firebase Console
- cek path collection/document
- cek `request.auth.uid`

### Index required

Firestore kadang butuh index untuk query gabungan.

Solusi:

- buka link yang muncul di error
- buat index dari Firebase Console

### Timestamp null

`FieldValue.serverTimestamp()` bisa sementara null sebelum server mengisi.

Solusi:

```dart
final createdAt = (data['createdAt'] as Timestamp?)?.toDate();
```

---

## 20. Checklist Firestore Dasar

Pastikan sudah paham:

- [ ] Firestore adalah database cloud NoSQL.
- [ ] Data disimpan dalam collection dan document.
- [ ] Field adalah data di dalam document.
- [ ] `add()` membuat document id otomatis.
- [ ] `set()` menulis ke document tertentu.
- [ ] `get()` membaca data sekali.
- [ ] `snapshots()` membaca data realtime.
- [ ] `update()` mengubah field document.
- [ ] `delete()` menghapus document.
- [ ] `where()` dipakai untuk filter.
- [ ] `orderBy()` dipakai untuk sorting.
- [ ] `FieldValue.serverTimestamp()` dipakai untuk waktu server.
- [ ] Data per user bisa memakai `users/{uid}/tasks/{taskId}`.
- [ ] Security rules penting agar user hanya akses data sendiri.

Jika checklist ini aman, lanjut ke **Firestore CRUD untuk Pemula**.

---

## 21. Lanjutan Setelah Ini

Materi berikutnya:

1. Firestore CRUD untuk Pemula.
2. Task Manager online per user.
3. Repository dengan Firestore.
4. Security Rules dasar lebih detail.
5. Offline cache dan sync.

Urutan yang disarankan:

```text
Cloud Firestore Dasar
-> Firestore CRUD
-> Task Manager Online
-> Security Rules
```

---

## Referensi Resmi

- [Cloud Firestore FlutterFire usage](https://firebase.flutter.dev/docs/firestore/usage)
- [Add data to Cloud Firestore](https://firebase.google.com/docs/firestore/manage-data/add-data)
- [Delete data from Cloud Firestore](https://docs.cloud.google.com/firestore/native/docs/manage-data/delete-data)
- [Firestore security rules conditions](https://docs.cloud.google.com/firestore/native/docs/security/rules-conditions)
