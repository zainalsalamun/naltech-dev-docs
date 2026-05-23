---
title: "Firestore CRUD untuk Pemula"
description: "Tutorial CRUD Cloud Firestore di Flutter: model Task, TaskFirestoreService, create, read, stream realtime, update, delete, query status, sorting, dan error handling."
category: "Flutter"
level: "Firebase"
order: 72
tags: ["flutter", "firebase", "firestore", "crud", "task"]
updated: "2026-05-23"
---

# Firestore CRUD untuk Pemula

Materi ini adalah praktik setelah memahami Cloud Firestore Dasar. Kita akan membuat service untuk melakukan CRUD task di Firestore.

CRUD:

- Create: menambah data
- Read: membaca data
- Update: mengubah data
- Delete: menghapus data

Target:

- install `cloud_firestore`
- membuat model `Task`
- membuat `TaskFirestoreService`
- create task
- read task sekali
- stream task realtime
- update task
- delete task
- query berdasarkan status
- sorting berdasarkan `createdAt`
- error handling sederhana

---

## 1. Persiapan

Pastikan sudah:

- membuat Firebase project
- menghubungkan Flutter ke Firebase
- menjalankan `flutterfire configure`
- punya `firebase_options.dart`
- inisialisasi Firebase di `main.dart`

Package yang dibutuhkan:

```bash
flutter pub add firebase_core
flutter pub add cloud_firestore
```

Import:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';
```

---

## 2. Struktur Folder

Struktur sederhana:

```text
lib/
  models/
    task.dart
  services/
    task_firestore_service.dart
  pages/
    firestore_task_page.dart
```

Kita mulai dari service layer dulu.

Nanti alurnya:

```text
UI
-> Repository
-> TaskFirestoreService
-> Cloud Firestore
```

Tapi untuk materi ini:

```text
UI
-> TaskFirestoreService
-> Cloud Firestore
```

Supaya konsep CRUD lebih mudah dipahami.

---

## 3. Struktur Data Firestore

Untuk latihan awal, pakai collection:

```text
tasks/{taskId}
```

Contoh document:

```text
tasks
  abc123
    title: "Belajar Firestore"
    description: "Membuat CRUD"
    status: "todo"
    createdAt: timestamp
    updatedAt: timestamp
```

Nanti setelah digabung dengan Firebase Auth, struktur akan berubah menjadi:

```text
users/{uid}/tasks/{taskId}
```

Untuk sekarang, fokus dulu pada CRUD dasar.

---

## 4. Membuat Model Task

Buat file:

```text
lib/models/task.dart
```

Isi:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

enum TaskStatus {
  todo,
  progress,
  done,
}

extension TaskStatusLabel on TaskStatus {
  String get label {
    switch (this) {
      case TaskStatus.todo:
        return 'Todo';
      case TaskStatus.progress:
        return 'Progress';
      case TaskStatus.done:
        return 'Done';
    }
  }
}

class Task {
  final String id;
  final String title;
  final String description;
  final TaskStatus status;
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

  Map<String, dynamic> toCreateJson() {
    return {
      'title': title,
      'description': description,
      'status': status.name,
      'createdAt': FieldValue.serverTimestamp(),
      'updatedAt': FieldValue.serverTimestamp(),
    };
  }

  Map<String, dynamic> toUpdateJson() {
    return {
      'title': title,
      'description': description,
      'status': status.name,
      'updatedAt': FieldValue.serverTimestamp(),
    };
  }

  factory Task.fromFirestore(
    DocumentSnapshot<Map<String, dynamic>> doc,
  ) {
    final data = doc.data();

    if (data == null) {
      throw Exception('Task data kosong');
    }

    return Task(
      id: doc.id,
      title: data['title'] as String,
      description: data['description'] as String,
      status: TaskStatus.values.byName(data['status'] as String),
      createdAt: (data['createdAt'] as Timestamp?)?.toDate(),
      updatedAt: (data['updatedAt'] as Timestamp?)?.toDate(),
    );
  }

  Task copyWith({
    String? id,
    String? title,
    String? description,
    TaskStatus? status,
    DateTime? createdAt,
    DateTime? updatedAt,
  }) {
    return Task(
      id: id ?? this.id,
      title: title ?? this.title,
      description: description ?? this.description,
      status: status ?? this.status,
      createdAt: createdAt ?? this.createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }
}
```

Penjelasan:

- `id` berasal dari `doc.id`.
- `toCreateJson()` dipakai saat create data.
- `toUpdateJson()` dipakai saat update data.
- `createdAt` hanya dibuat saat create.
- `updatedAt` berubah setiap update.
- `Timestamp?` dibuat nullable karena server timestamp bisa sementara kosong.

---

## 5. Kenapa Ada toCreateJson dan toUpdateJson

Saat create:

```dart
createdAt
updatedAt
```

perlu diisi.

Saat update:

```dart
createdAt
```

sebaiknya tidak diubah.

Karena itu kita pisahkan:

```dart
toCreateJson()
toUpdateJson()
```

Ini membuat data lebih rapi.

---

## 6. Membuat TaskFirestoreService

Buat file:

```text
lib/services/task_firestore_service.dart
```

Isi awal:

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

import '../models/task.dart';

class TaskFirestoreService {
  final FirebaseFirestore _firestore;

  TaskFirestoreService({
    FirebaseFirestore? firestore,
  }) : _firestore = firestore ?? FirebaseFirestore.instance;

  CollectionReference<Map<String, dynamic>> get _tasksRef {
    return _firestore.collection('tasks');
  }
}
```

Penjelasan:

- `_firestore` adalah instance Firestore.
- `_tasksRef` adalah reference ke collection `tasks`.
- Service dibuat agar kode Firestore tidak tersebar di UI.

---

## 7. Create Task

Tambahkan:

```dart
Future<void> createTask({
  required String title,
  required String description,
  TaskStatus status = TaskStatus.todo,
}) async {
  final task = Task(
    id: '',
    title: title,
    description: description,
    status: status,
  );

  await _tasksRef.add(task.toCreateJson());
}
```

Penggunaan:

```dart
await taskFirestoreService.createTask(
  title: 'Belajar Firestore',
  description: 'Membuat create task',
);
```

Firestore akan membuat document id otomatis.

---

## 8. Create Task dengan ID Sendiri

Jika ingin membuat id sendiri:

```dart
Future<void> setTask(Task task) async {
  await _tasksRef.doc(task.id).set(task.toCreateJson());
}
```

Namun untuk pemula, `add()` lebih mudah.

Gunakan:

```dart
add()
```

jika Firestore boleh membuat id.

Gunakan:

```dart
doc(id).set()
```

jika id sudah ditentukan aplikasi.

---

## 9. Read Task Sekali

Membaca semua task sekali:

```dart
Future<List<Task>> getTasks() async {
  final snapshot = await _tasksRef
      .orderBy('createdAt', descending: true)
      .get();

  return snapshot.docs.map(Task.fromFirestore).toList();
}
```

Penggunaan:

```dart
final tasks = await taskFirestoreService.getTasks();
```

Kapan memakai `get()`?

- saat hanya perlu membaca sekali
- saat halaman tidak perlu realtime
- saat ingin refresh manual

---

## 10. Read Task Realtime

Membaca realtime:

```dart
Stream<List<Task>> watchTasks() {
  return _tasksRef
      .orderBy('createdAt', descending: true)
      .snapshots()
      .map((snapshot) {
    return snapshot.docs.map(Task.fromFirestore).toList();
  });
}
```

Penggunaan di UI:

```dart
StreamBuilder<List<Task>>(
  stream: taskFirestoreService.watchTasks(),
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

    return ListView.builder(
      itemCount: tasks.length,
      itemBuilder: (context, index) {
        final task = tasks[index];
        return ListTile(
          title: Text(task.title),
          subtitle: Text(task.description),
        );
      },
    );
  },
)
```

Kapan memakai `snapshots()`?

- saat UI harus realtime
- saat data bisa berubah dari device lain
- saat ingin update otomatis

---

## 11. Read Task Berdasarkan ID

```dart
Future<Task?> getTaskById(String id) async {
  final snapshot = await _tasksRef.doc(id).get();

  if (!snapshot.exists) {
    return null;
  }

  return Task.fromFirestore(snapshot);
}
```

Penggunaan:

```dart
final task = await taskFirestoreService.getTaskById(taskId);
```

Jika task tidak ada, return `null`.

---

## 12. Update Task

```dart
Future<void> updateTask(Task task) async {
  await _tasksRef.doc(task.id).update(task.toUpdateJson());
}
```

Penggunaan:

```dart
await taskFirestoreService.updateTask(
  task.copyWith(
    title: 'Judul baru',
    status: TaskStatus.done,
  ),
);
```

Catatan:

`update()` akan gagal jika document tidak ada.

---

## 13. Update Status

Jika hanya ingin update status:

```dart
Future<void> updateTaskStatus({
  required String id,
  required TaskStatus status,
}) async {
  await _tasksRef.doc(id).update({
    'status': status.name,
    'updatedAt': FieldValue.serverTimestamp(),
  });
}
```

Penggunaan:

```dart
await taskFirestoreService.updateTaskStatus(
  id: task.id,
  status: TaskStatus.done,
);
```

Ini lebih ringan daripada mengirim semua field.

---

## 14. Delete Task

```dart
Future<void> deleteTask(String id) async {
  await _tasksRef.doc(id).delete();
}
```

Penggunaan:

```dart
await taskFirestoreService.deleteTask(task.id);
```

Jika document punya subcollection, delete document tidak otomatis menghapus subcollection. Untuk Task sederhana tanpa subcollection, aman.

---

## 15. Query Berdasarkan Status

Membaca task dengan status tertentu:

```dart
Future<List<Task>> getTasksByStatus(TaskStatus status) async {
  final snapshot = await _tasksRef
      .where('status', isEqualTo: status.name)
      .orderBy('createdAt', descending: true)
      .get();

  return snapshot.docs.map(Task.fromFirestore).toList();
}
```

Realtime:

```dart
Stream<List<Task>> watchTasksByStatus(TaskStatus status) {
  return _tasksRef
      .where('status', isEqualTo: status.name)
      .orderBy('createdAt', descending: true)
      .snapshots()
      .map((snapshot) {
    return snapshot.docs.map(Task.fromFirestore).toList();
  });
}
```

Catatan:

Query gabungan `where + orderBy` mungkin membutuhkan index. Jika Firestore memberi error index, ikuti link yang diberikan Firebase.

---

## 16. TaskFirestoreService Lengkap

```dart
import 'package:cloud_firestore/cloud_firestore.dart';

import '../models/task.dart';

class TaskFirestoreService {
  final FirebaseFirestore _firestore;

  TaskFirestoreService({
    FirebaseFirestore? firestore,
  }) : _firestore = firestore ?? FirebaseFirestore.instance;

  CollectionReference<Map<String, dynamic>> get _tasksRef {
    return _firestore.collection('tasks');
  }

  Future<void> createTask({
    required String title,
    required String description,
    TaskStatus status = TaskStatus.todo,
  }) async {
    final task = Task(
      id: '',
      title: title,
      description: description,
      status: status,
    );

    await _tasksRef.add(task.toCreateJson());
  }

  Future<void> setTask(Task task) async {
    await _tasksRef.doc(task.id).set(task.toCreateJson());
  }

  Future<List<Task>> getTasks() async {
    final snapshot = await _tasksRef
        .orderBy('createdAt', descending: true)
        .get();

    return snapshot.docs.map(Task.fromFirestore).toList();
  }

  Stream<List<Task>> watchTasks() {
    return _tasksRef
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map(Task.fromFirestore).toList();
    });
  }

  Future<Task?> getTaskById(String id) async {
    final snapshot = await _tasksRef.doc(id).get();

    if (!snapshot.exists) {
      return null;
    }

    return Task.fromFirestore(snapshot);
  }

  Future<void> updateTask(Task task) async {
    await _tasksRef.doc(task.id).update(task.toUpdateJson());
  }

  Future<void> updateTaskStatus({
    required String id,
    required TaskStatus status,
  }) async {
    await _tasksRef.doc(id).update({
      'status': status.name,
      'updatedAt': FieldValue.serverTimestamp(),
    });
  }

  Future<void> deleteTask(String id) async {
    await _tasksRef.doc(id).delete();
  }

  Future<List<Task>> getTasksByStatus(TaskStatus status) async {
    final snapshot = await _tasksRef
        .where('status', isEqualTo: status.name)
        .orderBy('createdAt', descending: true)
        .get();

    return snapshot.docs.map(Task.fromFirestore).toList();
  }

  Stream<List<Task>> watchTasksByStatus(TaskStatus status) {
    return _tasksRef
        .where('status', isEqualTo: status.name)
        .orderBy('createdAt', descending: true)
        .snapshots()
        .map((snapshot) {
      return snapshot.docs.map(Task.fromFirestore).toList();
    });
  }
}
```

---

## 17. Contoh Halaman Test CRUD

Buat halaman sederhana untuk test.

```dart
class FirestoreTaskPage extends StatelessWidget {
  FirestoreTaskPage({super.key});

  final service = TaskFirestoreService();

  Future<void> addSampleTask() async {
    await service.createTask(
      title: 'Belajar Firestore',
      description: 'Membuat CRUD task',
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Firestore Task'),
      ),
      body: StreamBuilder<List<Task>>(
        stream: service.watchTasks(),
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

          return ListView.builder(
            itemCount: tasks.length,
            itemBuilder: (context, index) {
              final task = tasks[index];

              return ListTile(
                title: Text(task.title),
                subtitle: Text(task.status.label),
                trailing: IconButton(
                  icon: const Icon(Icons.delete_outline),
                  onPressed: () {
                    service.deleteTask(task.id);
                  },
                ),
              );
            },
          );
        },
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: addSampleTask,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Dengan halaman ini:

- tekan tombol `+` untuk menambah task
- task muncul otomatis karena stream
- tekan delete untuk menghapus task

---

## 18. Error Handling di Service

Untuk pembelajaran, service boleh sederhana. Namun untuk aplikasi lebih rapi, tambahkan error handling.

Contoh:

```dart
Future<void> createTask({
  required String title,
  required String description,
  TaskStatus status = TaskStatus.todo,
}) async {
  try {
    final task = Task(
      id: '',
      title: title,
      description: description,
      status: status,
    );

    await _tasksRef.add(task.toCreateJson());
  } on FirebaseException catch (error) {
    throw Exception(error.message ?? 'Gagal membuat task');
  }
}
```

Error umum:

- permission denied
- network error
- missing index
- data type mismatch

---

## 19. CRUD Per User

Setelah Firebase Auth dipakai, ubah collection menjadi per user.

```dart
CollectionReference<Map<String, dynamic>> userTasksRef(String uid) {
  return _firestore
      .collection('users')
      .doc(uid)
      .collection('tasks');
}
```

Create:

```dart
Future<void> createUserTask({
  required String uid,
  required String title,
  required String description,
}) async {
  await userTasksRef(uid).add({
    'title': title,
    'description': description,
    'status': TaskStatus.todo.name,
    'createdAt': FieldValue.serverTimestamp(),
    'updatedAt': FieldValue.serverTimestamp(),
  });
}
```

Stream:

```dart
Stream<List<Task>> watchUserTasks(String uid) {
  return userTasksRef(uid)
      .orderBy('createdAt', descending: true)
      .snapshots()
      .map((snapshot) {
    return snapshot.docs.map(Task.fromFirestore).toList();
  });
}
```

Ini akan dipakai di materi **Task Manager Online per User**.

---

## 20. Testing Manual

Lakukan test:

1. Jalankan aplikasi.
2. Tekan tambah task.
3. Cek Firebase Console.
4. Pastikan document muncul di collection `tasks`.
5. Hapus task dari aplikasi.
6. Pastikan document hilang di Firebase Console.
7. Tambah task dari Firebase Console.
8. Pastikan UI ikut update jika memakai stream.
9. Ubah status task.
10. Pastikan field status berubah.

---

## 21. Kesalahan Umum

### Permission denied

Biasanya security rules menolak request.

Solusi sementara saat belajar:

- cek rules
- pastikan user login jika rules membutuhkan auth
- pastikan path sesuai rules

### Timestamp null

Gunakan nullable:

```dart
(data['createdAt'] as Timestamp?)?.toDate()
```

### Missing index

Query gabungan bisa butuh index.

Solusi:

- buka link dari error Firestore
- buat index di Firebase Console

### Data type mismatch

Contoh:

```dart
data['title'] as String
```

akan error jika field `title` tidak ada atau bukan String.

Pastikan struktur data konsisten.

---

## 22. Checklist Firestore CRUD

Pastikan sudah bisa:

- [ ] Install `cloud_firestore`.
- [ ] Membuat model `Task`.
- [ ] Membuat `TaskFirestoreService`.
- [ ] Create task dengan `add`.
- [ ] Read task sekali dengan `get`.
- [ ] Read realtime dengan `snapshots`.
- [ ] Read task by id.
- [ ] Update task.
- [ ] Update status task.
- [ ] Delete task.
- [ ] Query task berdasarkan status.
- [ ] Sorting berdasarkan `createdAt`.
- [ ] Memahami `FieldValue.serverTimestamp`.
- [ ] Menangani `Timestamp?`.
- [ ] Memahami permission denied.
- [ ] Memahami konsep task per user.

Jika checklist ini aman, lanjut ke **Task Manager Online per User**.

---

## 23. Lanjutan Setelah Ini

Materi berikutnya:

1. Task Manager Online per User.
2. Repository dengan Firestore.
3. Firestore Security Rules dasar.
4. Sync local storage + Firestore.

Urutan yang disarankan:

```text
Firestore CRUD
-> Task Manager Online per User
-> Security Rules
-> Offline-first sync
```

---

## Referensi Resmi

- [Cloud Firestore FlutterFire usage](https://firebase.flutter.dev/docs/firestore/usage)
- [Add data to Cloud Firestore](https://firebase.google.com/docs/firestore/manage-data/add-data)
- [Delete data from Cloud Firestore](https://docs.cloud.google.com/firestore/native/docs/manage-data/delete-data)
