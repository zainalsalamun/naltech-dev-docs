---
title: "Task Manager Online per User"
description: "Tutorial menggabungkan Firebase Auth dan Cloud Firestore untuk membuat Task Manager online yang datanya terpisah berdasarkan user login."
category: "Flutter"
level: "Firebase"
order: 73
tags: ["flutter", "firebase", "auth", "firestore", "task-manager"]
updated: "2026-05-23"
---

# Task Manager Online per User

Materi ini adalah lanjutan dari Firebase Authentication, Cloud Firestore Dasar, dan Firestore CRUD.

Di materi sebelumnya kita sudah belajar:

- membuat user login
- membaca `uid` user dari Firebase Auth
- membuat model `Task`
- melakukan create, read, update, dan delete data di Firestore

Sekarang kita akan menggabungkan semuanya menjadi aplikasi yang lebih nyata: **Task Manager online per user**.

Artinya:

- user A hanya melihat task milik user A
- user B hanya melihat task milik user B
- task tersimpan di Firestore
- data tetap ada walaupun aplikasi ditutup
- task bisa dibaca secara realtime

---

## 1. Gambaran Fitur

Kita akan membuat fitur:

- cek user yang sedang login
- menambah task dengan `userId`
- membaca task berdasarkan `uid`
- update judul task
- toggle selesai atau belum selesai
- hapus task
- logout
- menampilkan loading dan pesan error sederhana

Alur sederhananya:

```text
User login
  -> Firebase Auth memberikan uid
  -> App menyimpan task ke Firestore dengan field userId
  -> App membaca task dengan query where userId == uid
  -> User hanya melihat task miliknya sendiri
```

`uid` adalah identitas unik user dari Firebase Auth. Inilah yang akan kita pakai untuk memisahkan data antar user.

---

## 2. Kenapa Harus per User?

Kalau task tidak diberi `userId`, semua data bisa bercampur.

Contoh data yang kurang aman:

```json
{
  "title": "Belajar Flutter",
  "isDone": false
}
```

Masalahnya: kita tidak tahu task ini milik siapa.

Data yang lebih benar:

```json
{
  "title": "Belajar Flutter",
  "isDone": false,
  "userId": "uid_user_login",
  "createdAt": "server_timestamp"
}
```

Dengan `userId`, aplikasi bisa melakukan query:

```text
Ambil task yang userId-nya sama dengan uid user login.
```

Ini adalah pola penting saat membuat aplikasi multi-user.

---

## 3. Struktur Collection Firestore

Untuk pemula, kita gunakan struktur collection global:

```text
tasks
  taskId_1
    title: "Belajar Flutter"
    isDone: false
    userId: "abc123"
    createdAt: Timestamp
    updatedAt: Timestamp

  taskId_2
    title: "Belajar Firebase"
    isDone: true
    userId: "xyz789"
    createdAt: Timestamp
    updatedAt: Timestamp
```

Kelebihan struktur ini:

- mudah dipahami
- mudah di-query dengan `where`
- cocok untuk belajar CRUD
- mudah dikembangkan dengan filter status

Alternatif lain adalah subcollection per user:

```text
users
  userId
    tasks
      taskId
```

Struktur subcollection juga bagus, tetapi untuk materi ini kita mulai dari collection `tasks` agar konsep query `where userId == uid` lebih jelas.

---

## 4. Package yang Dibutuhkan

Pastikan package berikut sudah ada:

```bash
flutter pub add firebase_core
flutter pub add firebase_auth
flutter pub add cloud_firestore
```

Lalu pastikan Firebase sudah diinisialisasi di `main.dart`:

```dart
import 'package:firebase_core/firebase_core.dart';
import 'firebase_options.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await Firebase.initializeApp(
    options: DefaultFirebaseOptions.currentPlatform,
  );

  runApp(const MyApp());
}
```

Tanpa `Firebase.initializeApp`, Firebase Auth dan Firestore belum bisa digunakan.

---

## 5. Struktur Folder

Gunakan struktur folder sederhana:

```text
lib/
  models/
    task.dart
  repositories/
    task_repository.dart
  pages/
    online_task_page.dart
```

Pembagian tanggung jawabnya:

- `models/task.dart`: bentuk data task
- `repositories/task_repository.dart`: semua operasi Firestore
- `pages/online_task_page.dart`: tampilan dan interaksi user

Pola seperti ini membuat kode lebih rapi. Halaman UI tidak perlu langsung memanggil Firestore terlalu banyak.

---

## 6. Membuat Model Task

Buat file:

```text
lib/models/task.dart
```

Isi:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

class Task {
  final String id;
  final String title;
  final bool isDone;
  final String userId;
  final DateTime? createdAt;
  final DateTime? updatedAt;

  const Task({
    required this.id,
    required this.title,
    required this.isDone,
    required this.userId,
    this.createdAt,
    this.updatedAt,
  });

  factory Task.fromFirestore(DocumentSnapshot<Map<String, dynamic>> doc) {
    final data = doc.data();

    if (data == null) {
      throw Exception('Task tidak ditemukan');
    }

    return Task(
      id: doc.id,
      title: data['title'] ?? '',
      isDone: data['isDone'] ?? false,
      userId: data['userId'] ?? '',
      createdAt: (data['createdAt'] as Timestamp?)?.toDate(),
      updatedAt: (data['updatedAt'] as Timestamp?)?.toDate(),
    );
  }

  Map<String, dynamic> toCreateJson() {
    return {
      'title': title,
      'isDone': isDone,
      'userId': userId,
      'createdAt': FieldValue.serverTimestamp(),
      'updatedAt': FieldValue.serverTimestamp(),
    };
  }

  Map<String, dynamic> toUpdateJson() {
    return {
      'title': title,
      'isDone': isDone,
      'updatedAt': FieldValue.serverTimestamp(),
    };
  }

  Task copyWith({
    String? id,
    String? title,
    bool? isDone,
    String? userId,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Task(
      id: id ?? this.id,
      title: title ?? this.title,
      isDone: isDone ?? this.isDone,
      userId: userId ?? this.userId,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
```

Penjelasan:

- `id` berasal dari document id Firestore
- `title` adalah judul task
- `isDone` menyimpan status selesai atau belum
- `userId` menyimpan pemilik task
- `createdAt` menyimpan waktu task dibuat
- `updatedAt` menyimpan waktu task terakhir diubah
- `fromFirestore` mengubah document Firestore menjadi object Dart
- `toCreateJson` dipakai saat membuat task baru
- `toUpdateJson` dipakai saat mengubah task
- `copyWith` dipakai untuk membuat object baru dari object lama dengan sebagian data diubah

Kenapa `createdAt` tidak ikut di `toUpdateJson`?

Karena waktu pembuatan task tidak boleh berubah saat task diedit. Yang berubah hanya `updatedAt`.

---

## 7. Membaca User yang Sedang Login

Firebase Auth menyediakan user login lewat:

```dart
FirebaseAuth.instance.currentUser
```

Contoh:

```dart
final user = FirebaseAuth.instance.currentUser;

if (user == null) {
  throw Exception('User belum login');
}

final uid = user.uid;
```

Catatan penting:

- `currentUser` bisa `null` kalau user belum login
- jangan membuat task kalau user belum login
- gunakan `uid` sebagai `userId`

---

## 8. Membuat TaskRepository

Buat file:

```text
lib/repositories/task_repository.dart
```

Isi:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';
import 'package:firebase_auth/firebase_auth.dart';

import '../models/task.dart';

class TaskRepository {
  final FirebaseFirestore _firestore;
  final FirebaseAuth _auth;

  TaskRepository({
    FirebaseFirestore? firestore,
    FirebaseAuth? auth,
  })  : _firestore = firestore ?? FirebaseFirestore.instance,
        _auth = auth ?? FirebaseAuth.instance;

  CollectionReference<Map<String, dynamic>> get _tasksCollection {
    return _firestore.collection('tasks');
  }

  String get _currentUserId {
    final user = _auth.currentUser;

    if (user == null) {
      throw Exception('User belum login');
    }

    return user.uid;
  }

  Stream<List<Task>> watchMyTasks() {
    final uid = _currentUserId;

    return _tasksCollection
        .where('userId', isEqualTo: uid)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map(Task.fromFirestore).toList();
    });
  }

  Future<void> addTask(String title) async {
    final trimmedTitle = title.trim();

    if (trimmedTitle.isEmpty) {
      throw Exception('Judul task tidak boleh kosong');
    }

    final task = Task(
      id: '',
      title: trimmedTitle,
      isDone: false,
      userId: _currentUserId,
    );

    await _tasksCollection.add(task.toCreateJson());
  }

  Future<void> updateTaskTitle({
    required String taskId,
    required String title,
  }) async {
    final trimmedTitle = title.trim();

    if (trimmedTitle.isEmpty) {
      throw Exception('Judul task tidak boleh kosong');
    }

    await _tasksCollection.doc(taskId).update({
      'title': trimmedTitle,
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }

  Future<void> toggleTask(Task task) async {
    await _tasksCollection.doc(task.id).update({
      'isDone': !task.isDone,
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }

  Future<void> deleteTask(String taskId) async {
    await _tasksCollection.doc(taskId).delete();
  }
}
```

Penjelasan:

- `_tasksCollection` menunjuk ke collection `tasks`
- `_currentUserId` mengambil `uid` user login
- `watchMyTasks` membaca task milik user login secara realtime
- `addTask` membuat task baru dan otomatis mengisi `userId`
- `updateTaskTitle` hanya mengubah judul task
- `toggleTask` membalik status selesai
- `deleteTask` menghapus task

Kenapa query memakai `where('userId', isEqualTo: uid)`?

Karena aplikasi hanya boleh mengambil task yang pemiliknya sama dengan user login.

---

## 9. Membuat Halaman Task Manager Online

Buat file:

```text
lib/pages/online_task_page.dart
```

Isi:

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import '../models/task.dart';
import '../repositories/task_repository.dart';

class OnlineTaskPage extends StatefulWidget {
  const OnlineTaskPage({super.key});

  @override
  State<OnlineTaskPage> createState() => _OnlineTaskPageState();
}

class _OnlineTaskPageState extends State<OnlineTaskPage> {
  final TaskRepository _repository = TaskRepository();
  final TextEditingController _titleController = TextEditingController();

  @override
  void dispose() {
    _titleController.dispose();
    super.dispose();
  }

  Future<void> _addTask() async {
    try {
      await _repository.addTask(_titleController.text);
      _titleController.clear();
    } catch (error) {
      _showMessage(error.toString());
    }
  }

  Future<void> _editTask(Task task) async {
    final controller = TextEditingController(text: task.title);

    final newTitle = await showDialog<String>(
      context: context,
      builder: (context) {
        return AlertDialog(
          title: const Text('Edit Task'),
          content: TextField(
            controller: controller,
            autofocus: true,
            decoration: const InputDecoration(
              labelText: 'Judul task',
            ),
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Batal'),
            ),
            ElevatedButton(
              onPressed: () => Navigator.pop(context, controller.text),
              child: const Text('Simpan'),
            ),
          ],
        );
      },
    );

    controller.dispose();

    if (newTitle == null) return;

    try {
      await _repository.updateTaskTitle(
        taskId: task.id,
        title: newTitle,
      );
    } catch (error) {
      _showMessage(error.toString());
    }
  }

  Future<void> _logout() async {
    await FirebaseAuth.instance.signOut();
  }

  void _showMessage(String message) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text(message)),
    );
  }

  @override
  Widget build(BuildContext context) {
    final user = FirebaseAuth.instance.currentUser;

    if (user == null) {
      return const Scaffold(
        body: Center(
          child: Text('Silakan login terlebih dahulu'),
        ),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Manager Online'),
        actions: [
          IconButton(
            onPressed: _logout,
            icon: const Icon(Icons.logout),
          ),
        ],
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Row(
              children: [
                Expanded(
                  child: TextField(
                    controller: _titleController,
                    decoration: const InputDecoration(
                      labelText: 'Task baru',
                      border: OutlineInputBorder(),
                    ),
                    onSubmitted: (_) => _addTask(),
                  ),
                ),
                const SizedBox(width: 8),
                ElevatedButton(
                  onPressed: _addTask,
                  child: const Text('Tambah'),
                ),
              ],
            ),
          ),
          Expanded(
            child: StreamBuilder<List<Task>>(
              stream: _repository.watchMyTasks(),
              builder: (context, snapshot) {
                if (snapshot.connectionState == ConnectionState.waiting) {
                  return const Center(
                    child: CircularProgressIndicator(),
                  );
                }

                if (snapshot.hasError) {
                  return Center(
                    child: Text('Error: ${snapshot.error}'),
                  );
                }

                final tasks = snapshot.data ?? [];

                if (tasks.isEmpty) {
                  return const Center(
                    child: Text('Belum ada task'),
                  );
                }

                return ListView.separated(
                  itemCount: tasks.length,
                  separatorBuilder: (context, index) => const Divider(height: 1),
                  itemBuilder: (context, index) {
                    final task = tasks[index];

                    return ListTile(
                      leading: Checkbox(
                        value: task.isDone,
                        onChanged: (_) => _repository.toggleTask(task),
                      ),
                      title: Text(
                        task.title,
                        style: TextStyle(
                          decoration: task.isDone
                              ? TextDecoration.lineThrough
                              : TextDecoration.none,
                        ),
                      ),
                      subtitle: Text('Owner: ${task.userId}'),
                      onTap: () => _editTask(task),
                      trailing: IconButton(
                        onPressed: () => _repository.deleteTask(task.id),
                        icon: const Icon(Icons.delete),
                      ),
                    );
                  },
                );
              },
            ),
          ),
        ],
      ),
    );
  }
}
```

Penjelasan bagian penting:

- `StreamBuilder` dipakai karena data Firestore bisa berubah realtime
- saat task baru ditambah, list otomatis berubah
- saat task dihapus dari device lain, list juga ikut berubah
- `snapshot.connectionState` dipakai untuk menampilkan loading
- `snapshot.hasError` dipakai untuk menampilkan error
- `tasks.isEmpty` dipakai untuk empty state
- `Checkbox` memanggil `toggleTask`
- tap item membuka dialog edit
- tombol delete menghapus task

---

## 10. Menyambungkan Halaman ke main.dart

Contoh sederhana:

```dart
import 'package:flutter/material.dart';

import 'pages/online_task_page.dart';

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Task Manager Online',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const OnlineTaskPage(),
    );
  }
}
```

Untuk aplikasi sungguhan, biasanya `home` diarahkan ke halaman auth wrapper:

```text
jika user login    -> OnlineTaskPage
jika belum login   -> LoginPage
```

Tetapi untuk fokus materi ini, kita cukup menampilkan `OnlineTaskPage`.

---

## 11. Membuat Auth Wrapper Sederhana

Agar aplikasi otomatis pindah halaman berdasarkan status login, gunakan `authStateChanges`.

Contoh:

```dart
import 'package:firebase_auth/firebase_auth.dart';
import 'package:flutter/material.dart';

import 'login_page.dart';
import 'online_task_page.dart';

class AuthWrapper extends StatelessWidget {
  const AuthWrapper({super.key});

  @override
  Widget build(BuildContext context) {
    return StreamBuilder<User?>(
      stream: FirebaseAuth.instance.authStateChanges(),
      builder: (context, snapshot) {
        if (snapshot.connectionState == ConnectionState.waiting) {
          return const Scaffold(
            body: Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        if (snapshot.data == null) {
          return const LoginPage();
        }

        return const OnlineTaskPage();
      },
    );
  }
}
```

Lalu di `main.dart`:

```dart
home: const AuthWrapper(),
```

Dengan pola ini:

- user belum login akan melihat `LoginPage`
- user sudah login akan masuk ke `OnlineTaskPage`
- saat logout, halaman otomatis kembali ke login

---

## 12. Query Data Milik User Login

Bagian paling penting ada di sini:

```dart
return _tasksCollection
    .where('userId', isEqualTo: uid)
    .orderBy('createdAt', descending: true)
    .snapshots();
```

Query ini artinya:

- cari document di collection `tasks`
- ambil hanya document dengan `userId` sama dengan `uid`
- urutkan dari yang terbaru
- pantau perubahan secara realtime

Kalau query ini tidak memakai `where`, semua task dari semua user bisa muncul.

Firebase Security Rules juga harus dibuat sesuai query ini. Rules bukan filter otomatis. Query aplikasi tetap harus menuliskan batasan data yang benar.

---

## 13. Index Firestore

Query gabungan seperti ini kadang membutuhkan index:

```dart
.where('userId', isEqualTo: uid)
.orderBy('createdAt', descending: true)
```

Kalau Firestore meminta index, biasanya error akan menampilkan link untuk membuat index otomatis.

Langkahnya:

1. jalankan aplikasi
2. buka halaman task
3. jika muncul error index, salin atau klik link dari error
4. buka Firebase Console
5. buat index
6. tunggu status index menjadi enabled
7. jalankan ulang fitur

Ini normal di Firestore. Query yang semakin spesifik sering membutuhkan index.

---

## 14. Security Rules Dasar

Untuk tahap belajar, gunakan rules yang membatasi user hanya bisa membaca dan mengubah task miliknya.

Contoh:

```text
rules_version = '2';

service cloud.firestore {
  match /databases/{database}/documents {
    match /tasks/{taskId} {
      allow read: if request.auth != null
        && resource.data.userId == request.auth.uid;

      allow create: if request.auth != null
        && request.resource.data.userId == request.auth.uid;

      allow update, delete: if request.auth != null
        && resource.data.userId == request.auth.uid;
    }
  }
}
```

Penjelasan:

- `request.auth != null` memastikan user sudah login
- `request.auth.uid` adalah uid user login
- `resource.data` adalah data lama yang sudah ada di Firestore
- `request.resource.data` adalah data baru yang akan ditulis
- `allow read` memastikan user hanya membaca task miliknya
- `allow create` memastikan user hanya bisa membuat task dengan `userId` miliknya sendiri
- `allow update, delete` memastikan user hanya bisa mengubah atau menghapus task miliknya

Materi security rules akan kita bahas lebih detail di bagian berikutnya, karena rules adalah bagian penting untuk keamanan aplikasi.

---

## 15. Validasi Data Sederhana

Selain membatasi user, kita juga bisa validasi bentuk data.

Contoh rules yang lebih ketat:

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

      function hasValidTaskFields() {
        return request.resource.data.keys().hasOnly([
          'title',
          'isDone',
          'userId',
          'createdAt',
          'updatedAt'
        ])
        && request.resource.data.title is string
        && request.resource.data.title.size() > 0
        && request.resource.data.title.size() <= 100
        && request.resource.data.isDone is bool
        && request.resource.data.userId is string;
      }

      allow read: if isSignedIn() && isOwner();
      allow create: if isSignedIn()
        && isCreatingOwnTask()
        && hasValidTaskFields();
      allow update: if isSignedIn()
        && isOwner()
        && hasValidTaskFields()
        && request.resource.data.userId == resource.data.userId;
      allow delete: if isSignedIn() && isOwner();
    }
  }
}
```

Rules ini lebih panjang, tetapi lebih aman karena:

- field dibatasi
- title harus string
- title tidak boleh kosong
- title maksimal 100 karakter
- `isDone` harus boolean
- `userId` tidak boleh diganti saat update

---

## 16. Menampilkan Filter Task

Setelah task per user berjalan, kita bisa menambahkan filter.

Contoh enum:

```dart
enum TaskFilter {
  all,
  active,
  done,
}
```

Modifikasi repository:

```dart
Stream<List<Task>> watchMyTasks({
  TaskFilter filter = TaskFilter.all,
}) {
  final uid = _currentUserId;

  Query<Map<String, dynamic>> query = _tasksCollection
      .where('userId', isEqualTo: uid)
      .orderBy('createdAt', descending: true);

  if (filter == TaskFilter.active) {
    query = query.where('isDone', isEqualTo: false);
  }

  if (filter == TaskFilter.done) {
    query = query.where('isDone', isEqualTo: true);
  }

  return query.snapshots().map((snapshot) {
    return snapshot.docs.map(Task.fromFirestore).toList();
  });
}
```

Dengan filter ini:

- `all`: tampilkan semua task
- `active`: tampilkan task yang belum selesai
- `done`: tampilkan task yang sudah selesai

Kalau query meminta index baru, buat index dari link error yang diberikan Firestore.

---

## 17. Error yang Sering Muncul

### User belum login

Penyebab:

- `FirebaseAuth.instance.currentUser` bernilai `null`
- halaman task dibuka sebelum login

Solusi:

- gunakan `AuthWrapper`
- arahkan user ke `LoginPage`

### Permission denied

Penyebab:

- security rules menolak request
- `userId` tidak sama dengan `request.auth.uid`
- user belum login

Solusi:

- cek rules Firestore
- cek field `userId`
- cek apakah user sudah login

### The query requires an index

Penyebab:

- query memakai kombinasi `where` dan `orderBy`
- Firestore membutuhkan index tambahan

Solusi:

- buka link index dari error
- buat index di Firebase Console
- tunggu sampai enabled

### Type Timestamp error

Penyebab:

- field `createdAt` atau `updatedAt` belum ada
- data lama tidak punya timestamp

Solusi:

- gunakan nullable timestamp
- parsing dengan aman:

```dart
createdAt: (data['createdAt'] as Timestamp?)?.toDate(),
```

---

## 18. Checklist Testing Manual

Gunakan checklist ini untuk memastikan fitur berjalan:

- user bisa login
- user bisa tambah task
- task muncul di list
- task tersimpan di Firestore
- field `userId` sama dengan uid user login
- task tetap ada setelah aplikasi ditutup
- task bisa diedit
- task bisa ditandai selesai
- task bisa dihapus
- user bisa logout
- user lain tidak melihat task user sebelumnya
- rules menolak akses data yang bukan milik user

Testing dengan dua akun sangat disarankan.

Contoh:

1. login dengan akun A
2. buat task "Belajar Firebase"
3. logout
4. login dengan akun B
5. pastikan task akun A tidak muncul
6. buat task akun B
7. logout
8. login lagi dengan akun A
9. pastikan task akun A masih ada

---

## 19. Kesimpulan

Di materi ini kita sudah belajar membuat Task Manager online per user.

Poin penting:

- data user harus dipisahkan dengan `uid`
- task perlu menyimpan field `userId`
- query harus memakai `where('userId', isEqualTo: uid)`
- Firestore realtime cocok untuk aplikasi task
- Security Rules tetap wajib untuk keamanan
- UI sebaiknya tidak langsung terlalu banyak berisi logic Firestore
- repository membantu memisahkan logic data dari tampilan

Setelah memahami materi ini, kamu sudah mulai masuk ke pola aplikasi Flutter yang lebih nyata.

---

## 20. Selanjutnya

Materi berikutnya yang paling cocok adalah **Firestore Security Rules Dasar**.

Alasannya:

- kita sudah punya data per user
- sekarang perlu memastikan data benar-benar aman
- user tidak boleh membaca atau mengubah data milik user lain
- rules perlu dipahami sebelum aplikasi dipakai publik

Referensi resmi:

- [Firebase Auth Flutter](https://firebase.google.com/docs/auth/flutter/start)
- [Cloud Firestore add and update data](https://firebase.google.com/docs/firestore/manage-data/add-data)
- [Firestore secure queries](https://firebase.google.com/docs/firestore/security/rules-query)
- [Firestore Security Rules conditions](https://firebase.google.com/docs/firestore/security/rules-conditions)
