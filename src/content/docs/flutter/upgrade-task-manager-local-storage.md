---
title: "Upgrade Task Manager dengan Local Storage"
description: "Tutorial upgrade Project Task Manager agar data tidak hilang: tambah toJson/fromJson, simpan List<Task> ke shared_preferences, load saat app dibuka, dan update storage saat add/edit/delete."
category: "Flutter"
level: "Project"
order: 57
tags: ["flutter", "task-manager", "shared-preferences", "local-storage", "json"]
updated: "2026-05-23"
---

# Upgrade Task Manager dengan Local Storage

Di Project Task Manager sebelumnya, data task masih disimpan di `List<Task>` biasa. Artinya, data akan hilang saat aplikasi ditutup. Pada materi ini, kita upgrade Task Manager supaya data tetap tersimpan memakai `shared_preferences`.

Yang akan dipelajari:

- menambahkan `toJson` dan `fromJson` ke model `Task`
- menyimpan `List<Task>` ke local storage
- membaca task saat aplikasi dibuka
- update storage saat tambah task
- update storage saat edit task
- update storage saat hapus task
- membuat service agar kode lebih rapi

---

## 1. Gambaran Alur

Sebelum local storage:

```text
User tambah task
-> task masuk ke List
-> UI update
-> aplikasi ditutup
-> List hilang
```

Setelah local storage:

```text
User tambah task
-> task masuk ke List
-> List disimpan ke shared_preferences
-> UI update
-> aplikasi ditutup
-> aplikasi dibuka lagi
-> task dibaca dari shared_preferences
-> UI menampilkan task lama
```

Prinsip penting:

```text
State di memory tetap dipakai untuk UI.
Local storage dipakai agar data tidak hilang.
```

Jadi UI tidak membaca langsung ke storage setiap saat. Storage dibaca saat awal, lalu data dimasukkan ke state. Ketika state berubah, storage ikut diperbarui.

---

## 2. Install Package

Tambahkan package:

```bash
flutter pub add shared_preferences
```

Lalu:

```bash
flutter pub get
```

Import yang akan dipakai:

```dart
import 'dart:convert';
import 'package:shared_preferences/shared_preferences.dart';
```

---

## 3. Struktur Folder

Struktur project yang disarankan:

```text
lib/
  main.dart
  models/
    task.dart
  pages/
    task_list_page.dart
    task_form_page.dart
  services/
    task_storage_service.dart
  widgets/
    task_card.dart
    task_status_chip.dart
```

File baru yang akan dibuat:

```text
lib/services/task_storage_service.dart
```

File yang akan diubah:

```text
lib/models/task.dart
lib/pages/task_list_page.dart
```

---

## 4. Update Model Task

Buka file:

```text
lib/models/task.dart
```

Contoh model awal:

```dart
enum TaskStatus {
  todo,
  progress,
  done,
}

class Task {
  final int id;
  final String title;
  final String description;
  final TaskStatus status;
  final DateTime createdAt;

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
    required this.createdAt,
  });
}
```

Tambahkan `toJson`, `fromJson`, dan `copyWith`:

```dart
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
  final int id;
  final String title;
  final String description;
  final TaskStatus status;
  final DateTime createdAt;

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
    required this.createdAt,
  });

  Task copyWith({
    String? title,
    String? description,
    TaskStatus? status,
  }) {
    return Task(
      id: id,
      title: title ?? this.title,
      description: description ?? this.description,
      status: status ?? this.status,
      createdAt: createdAt,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'status': status.name,
      'createdAt': createdAt.toIso8601String(),
    };
  }

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] as int,
      title: json['title'] as String,
      description: json['description'] as String,
      status: TaskStatus.values.byName(json['status'] as String),
      createdAt: DateTime.parse(json['createdAt'] as String),
    );
  }
}
```

Penjelasan:

- `toJson()` mengubah object `Task` menjadi `Map`.
- `fromJson()` mengubah `Map` menjadi object `Task`.
- `status.name` menyimpan enum sebagai string, misalnya `todo`.
- `TaskStatus.values.byName(...)` mengubah string menjadi enum.
- `createdAt.toIso8601String()` menyimpan tanggal sebagai string.
- `DateTime.parse(...)` mengubah string kembali menjadi `DateTime`.

---

## 5. Kenapa Enum Disimpan sebagai String

Enum tidak bisa langsung disimpan ke JSON.

Kurang tepat:

```dart
'status': status,
```

Lebih aman:

```dart
'status': status.name,
```

Jika `status` bernilai:

```dart
TaskStatus.todo
```

Maka `status.name` menghasilkan:

```text
todo
```

Saat membaca:

```dart
TaskStatus.values.byName('todo')
```

Hasilnya:

```dart
TaskStatus.todo
```

---

## 6. Membuat TaskStorageService

Buat file:

```text
lib/services/task_storage_service.dart
```

Isi:

```dart
import 'dart:convert';

import 'package:shared_preferences/shared_preferences.dart';

import '../models/task.dart';

class TaskStorageService {
  static const _tasksKey = 'tasks';

  Future<void> saveTasks(List<Task> tasks) async {
    final prefs = await SharedPreferences.getInstance();

    final jsonList = tasks.map((task) => task.toJson()).toList();
    final jsonString = jsonEncode(jsonList);

    await prefs.setString(_tasksKey, jsonString);
  }

  Future<List<Task>> loadTasks() async {
    final prefs = await SharedPreferences.getInstance();
    final jsonString = prefs.getString(_tasksKey);

    if (jsonString == null) {
      return [];
    }

    final jsonList = jsonDecode(jsonString) as List<dynamic>;

    return jsonList
        .map((item) => Task.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  Future<void> clearTasks() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_tasksKey);
  }
}
```

Penjelasan:

- `_tasksKey` adalah key untuk menyimpan semua task.
- `saveTasks` mengubah `List<Task>` menjadi JSON string.
- `loadTasks` membaca JSON string lalu mengubahnya menjadi `List<Task>`.
- `clearTasks` menghapus data task dari storage.

Kenapa dibuat service?

Supaya logic storage tidak bercampur dengan UI. Page cukup memanggil:

```dart
storageService.saveTasks(tasks);
storageService.loadTasks();
```

---

## 7. Memahami saveTasks

Bagian penting:

```dart
final jsonList = tasks.map((task) => task.toJson()).toList();
```

Ini mengubah:

```text
List<Task>
```

menjadi:

```text
List<Map<String, dynamic>>
```

Lalu:

```dart
final jsonString = jsonEncode(jsonList);
```

Ini mengubah list map menjadi string.

Baru disimpan:

```dart
await prefs.setString(_tasksKey, jsonString);
```

Alur:

```text
List<Task>
-> List<Map>
-> String JSON
-> shared_preferences
```

---

## 8. Memahami loadTasks

Bagian penting:

```dart
final jsonString = prefs.getString(_tasksKey);
```

Jika belum ada data:

```dart
if (jsonString == null) {
  return [];
}
```

Jika ada data:

```dart
final jsonList = jsonDecode(jsonString) as List<dynamic>;
```

Lalu ubah setiap item menjadi `Task`:

```dart
return jsonList
    .map((item) => Task.fromJson(item as Map<String, dynamic>))
    .toList();
```

Alur:

```text
shared_preferences
-> String JSON
-> List<dynamic>
-> List<Task>
```

---

## 9. Update TaskListPage

Buka file:

```text
lib/pages/task_list_page.dart
```

Tambahkan service:

```dart
final taskStorageService = TaskStorageService();
```

Tambahkan state loading:

```dart
bool isLoading = true;
```

Contoh struktur:

```dart
class _TaskListPageState extends State<TaskListPage> {
  final taskStorageService = TaskStorageService();

  final List<Task> tasks = [];
  TaskStatus? selectedStatus;
  String searchQuery = '';
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadTasks();
  }

  Future<void> loadTasks() async {
    final savedTasks = await taskStorageService.loadTasks();

    setState(() {
      tasks
        ..clear()
        ..addAll(savedTasks);
      isLoading = false;
    });
  }
}
```

Penjelasan:

- `initState()` dipanggil saat halaman pertama kali dibuat.
- `loadTasks()` membaca data dari storage.
- `tasks.clear()` menghapus isi list saat ini.
- `tasks.addAll(savedTasks)` mengisi list dari storage.
- `isLoading = false` menandakan proses load selesai.

---

## 10. Tampilkan Loading Saat Membaca Storage

Di `build`, tambahkan kondisi:

```dart
if (isLoading) {
  return Scaffold(
    appBar: AppBar(
      title: const Text('Task Manager'),
    ),
    body: const Center(
      child: CircularProgressIndicator(),
    ),
  );
}
```

Tujuannya:

- user tahu aplikasi sedang membaca data
- UI tidak langsung menampilkan empty state sebelum load selesai

Tanpa loading, user bisa melihat "Belum ada task" sebentar walaupun sebenarnya task masih sedang dibaca.

---

## 11. Simpan Storage Saat Add Task

Sebelumnya:

```dart
setState(() {
  tasks.add(result);
});
```

Ubah menjadi:

```dart
setState(() {
  tasks.add(result);
});

await taskStorageService.saveTasks(tasks);
```

Contoh lengkap:

```dart
Future<void> openCreatePage() async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => const TaskFormPage(),
    ),
  );

  if (result == null) return;

  setState(() {
    tasks.add(result);
  });

  await taskStorageService.saveTasks(tasks);
}
```

Alur:

```text
Form mengembalikan task
-> task ditambahkan ke List
-> List disimpan ke local storage
```

---

## 12. Simpan Storage Saat Edit Task

Sebelumnya:

```dart
setState(() {
  tasks[index] = result;
});
```

Tambahkan save:

```dart
setState(() {
  tasks[index] = result;
});

await taskStorageService.saveTasks(tasks);
```

Contoh lengkap:

```dart
Future<void> openEditPage(Task task) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => TaskFormPage(task: task),
    ),
  );

  if (result == null) return;

  final index = tasks.indexWhere((item) => item.id == result.id);
  if (index == -1) return;

  setState(() {
    tasks[index] = result;
  });

  await taskStorageService.saveTasks(tasks);
}
```

Setiap edit selesai, storage harus ditimpa dengan list terbaru.

---

## 13. Simpan Storage Saat Update Status

Sebelumnya:

```dart
setState(() {
  tasks[index] = tasks[index].copyWith(status: status);
});
```

Ubah function menjadi async:

```dart
Future<void> updateTaskStatus(int id, TaskStatus status) async {
  final index = tasks.indexWhere((task) => task.id == id);
  if (index == -1) return;

  setState(() {
    tasks[index] = tasks[index].copyWith(status: status);
  });

  await taskStorageService.saveTasks(tasks);
}
```

Pemanggilan:

```dart
onStatusChanged: (status) {
  updateTaskStatus(task.id, status);
},
```

Tidak perlu `await` di UI jika tidak ada aksi setelah update. Tapi function tetap async agar bisa menyimpan data.

---

## 14. Simpan Storage Saat Delete Task

Sebelumnya:

```dart
setState(() {
  tasks.removeWhere((item) => item.id == task.id);
});
```

Tambahkan save:

```dart
setState(() {
  tasks.removeWhere((item) => item.id == task.id);
});

await taskStorageService.saveTasks(tasks);
```

Contoh lengkap:

```dart
Future<void> confirmDelete(Task task) async {
  final result = await showDialog<bool>(
    context: context,
    builder: (context) {
      return AlertDialog(
        title: const Text('Hapus task?'),
        content: Text('Task "${task.title}" akan dihapus.'),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Batal'),
          ),
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Hapus'),
          ),
        ],
      );
    },
  );

  if (result != true) return;

  setState(() {
    tasks.removeWhere((item) => item.id == task.id);
  });

  await taskStorageService.saveTasks(tasks);
}
```

Setelah task dihapus dari memory, storage harus ikut diperbarui.

---

## 15. Membuat Helper saveCurrentTasks

Agar tidak menulis:

```dart
await taskStorageService.saveTasks(tasks);
```

berulang-ulang, buat helper:

```dart
Future<void> saveCurrentTasks() async {
  await taskStorageService.saveTasks(tasks);
}
```

Lalu gunakan:

```dart
setState(() {
  tasks.add(result);
});

await saveCurrentTasks();
```

Ini membuat kode lebih mudah dibaca.

---

## 16. Contoh TaskListPage Ringkas

Contoh potongan penting:

```dart
class _TaskListPageState extends State<TaskListPage> {
  final taskStorageService = TaskStorageService();

  final List<Task> tasks = [];
  TaskStatus? selectedStatus;
  String searchQuery = '';
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    loadTasks();
  }

  Future<void> loadTasks() async {
    final savedTasks = await taskStorageService.loadTasks();

    setState(() {
      tasks
        ..clear()
        ..addAll(savedTasks);
      isLoading = false;
    });
  }

  Future<void> saveCurrentTasks() async {
    await taskStorageService.saveTasks(tasks);
  }

  Future<void> addTask(Task task) async {
    setState(() {
      tasks.add(task);
    });

    await saveCurrentTasks();
  }

  Future<void> updateTask(Task updatedTask) async {
    final index = tasks.indexWhere((task) => task.id == updatedTask.id);
    if (index == -1) return;

    setState(() {
      tasks[index] = updatedTask;
    });

    await saveCurrentTasks();
  }

  Future<void> deleteTask(int id) async {
    setState(() {
      tasks.removeWhere((task) => task.id == id);
    });

    await saveCurrentTasks();
  }
}
```

Dengan pola ini, setiap perubahan data selalu diikuti penyimpanan storage.

---

## 17. Testing Manual

Setelah selesai, lakukan test manual:

1. Jalankan aplikasi.
2. Tambahkan beberapa task.
3. Tutup aplikasi.
4. Buka lagi.
5. Pastikan task masih ada.
6. Edit task.
7. Tutup dan buka lagi.
8. Pastikan hasil edit masih ada.
9. Hapus task.
10. Tutup dan buka lagi.
11. Pastikan task yang dihapus tidak muncul lagi.

Jika semua berhasil, local storage sudah bekerja.

---

## 18. Error yang Sering Terjadi

### Data tidak muncul setelah app dibuka

Cek:

- apakah `loadTasks()` dipanggil di `initState`
- apakah key storage sama
- apakah `saveTasks()` berhasil dipanggil
- apakah parsing JSON error

### Data muncul saat ditambah, tapi hilang saat restart

Kemungkinan:

- hanya menambah data ke `List`
- lupa memanggil `saveTasks`

### Error saat parsing enum

Penyebab:

```dart
TaskStatus.values.byName(json['status'] as String)
```

akan error jika string status tidak cocok.

Pastikan value yang disimpan berasal dari:

```dart
status.name
```

### Error saat parsing DateTime

Pastikan tanggal disimpan dengan:

```dart
createdAt.toIso8601String()
```

Dan dibaca dengan:

```dart
DateTime.parse(json['createdAt'] as String)
```

---

## 19. Checklist Upgrade

Pastikan sudah selesai:

- [ ] `Task` punya `toJson`.
- [ ] `Task` punya `fromJson`.
- [ ] `TaskStatus` disimpan dengan `status.name`.
- [ ] `DateTime` disimpan dengan `toIso8601String`.
- [ ] Ada `TaskStorageService`.
- [ ] Bisa menyimpan `List<Task>` ke shared_preferences.
- [ ] Bisa load task saat app dibuka.
- [ ] Ada loading state saat membaca storage.
- [ ] Storage update saat add task.
- [ ] Storage update saat edit task.
- [ ] Storage update saat update status.
- [ ] Storage update saat delete task.
- [ ] Data tetap ada setelah aplikasi ditutup dan dibuka lagi.

Jika checklist ini aman, Task Manager sudah punya local persistence dasar.

---

## 20. Lanjutan Setelah Ini

Setelah memakai `shared_preferences`, langkah berikutnya:

1. Upgrade Task Manager dengan Provider + local storage.
2. Upgrade Task Manager dengan Riverpod + local storage.
3. Simpan task ke Hive/Isar untuk data lokal yang lebih besar.
4. Sinkronkan task ke Firestore.
5. Tambahkan login agar task tersimpan per user.

Urutan paling enak:

```text
setState + shared_preferences
-> Provider + shared_preferences
-> Riverpod + shared_preferences
-> Firestore
```
