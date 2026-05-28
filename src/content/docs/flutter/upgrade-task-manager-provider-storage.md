---
title: "Upgrade Task Manager dengan Provider dan Local Storage"
description: "Tutorial upgrade Task Manager agar memakai Provider untuk state management dan shared_preferences untuk local storage."
category: "Flutter"
level: "Project"
order: 58
tags: ["flutter", "provider", "task-manager", "shared-preferences", "local-storage"]
updated: "2026-05-23"
---

# Upgrade Task Manager dengan Provider dan Local Storage

Pada materi sebelumnya, Task Manager sudah bisa menyimpan data ke local storage memakai `shared_preferences`. Namun logic state masih banyak berada di halaman. Di materi ini, kita upgrade struktur project agar state dan logic task dipindahkan ke `TaskProvider`.

Target:

- UI lebih bersih.
- Logic CRUD pindah ke Provider.
- Local storage tetap dikelola oleh service.
- Data task di-load saat provider dibuat.
- Storage update otomatis saat add/edit/delete/update status.

---

## 1. Gambaran Arsitektur

Sebelum memakai Provider:

```text
TaskListPage
-> menyimpan List<Task>
-> load storage
-> add/edit/delete
-> save storage
-> filter/search
-> render UI
```

Masalahnya, page menjadi terlalu banyak tanggung jawab.

Setelah memakai Provider:

```text
TaskListPage
-> membaca state dari TaskProvider
-> memanggil action TaskProvider

TaskProvider
-> menyimpan List<Task>
-> mengelola filter/search
-> memanggil TaskStorageService

TaskStorageService
-> save/load shared_preferences
```

Pembagian tugas:

| Bagian | Tugas |
| --- | --- |
| `TaskListPage` | Menampilkan UI |
| `TaskProvider` | Mengelola state dan logic task |
| `TaskStorageService` | Menyimpan dan membaca local storage |
| `Task` | Bentuk data |

---

## 2. Struktur Folder

Struktur yang disarankan:

```text
lib/
  main.dart
  models/
    task.dart
  pages/
    task_list_page.dart
    task_form_page.dart
  providers/
    task_provider.dart
  services/
    task_storage_service.dart
  widgets/
    task_card.dart
    task_status_chip.dart
```

File baru:

```text
lib/providers/task_provider.dart
```

File yang tetap dipakai:

```text
lib/services/task_storage_service.dart
```

---

## 3. Install Package

Pastikan package berikut sudah ada:

```bash
flutter pub add provider
flutter pub add shared_preferences
```

Lalu:

```bash
flutter pub get
```

Import Provider:

```dart
import 'package:provider/provider.dart';
```

---

## 4. Model Task

Model `Task` tetap memakai `toJson` dan `fromJson`.

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

---

## 5. TaskStorageService

Service tetap bertugas menyimpan dan membaca data.

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

Kenapa service tidak digabung ke provider?

Supaya tanggung jawabnya jelas:

```text
Provider -> state dan logic aplikasi
Service -> detail teknis storage
```

Jika nanti pindah dari `shared_preferences` ke Hive atau Firestore, kita bisa mengubah service tanpa banyak mengganggu UI.

---

## 6. Membuat TaskProvider

Buat file:

```text
lib/providers/task_provider.dart
```

Isi:

```dart
import 'package:flutter/foundation.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';

class TaskProvider extends ChangeNotifier {
  final TaskStorageService _storageService;

  TaskProvider({
    TaskStorageService? storageService,
  }) : _storageService = storageService ?? TaskStorageService() {
    loadTasks();
  }

  final List<Task> _tasks = [];
  TaskStatus? _selectedStatus;
  String _searchQuery = '';
  bool _isLoading = true;
  String? _errorMessage;

  List<Task> get tasks => List.unmodifiable(_tasks);
  TaskStatus? get selectedStatus => _selectedStatus;
  String get searchQuery => _searchQuery;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;
}
```

Penjelasan:

- `_tasks` private agar tidak diubah langsung dari UI.
- `tasks` mengembalikan `List.unmodifiable`.
- `_isLoading` dipakai saat membaca storage.
- `_errorMessage` dipakai jika load/save gagal.
- `loadTasks()` dipanggil saat provider dibuat.

---

## 7. Load Task Saat Provider Dibuat

Tambahkan function:

```dart
Future<void> loadTasks() async {
  try {
    _isLoading = true;
    _errorMessage = null;
    notifyListeners();

    final savedTasks = await _storageService.loadTasks();

    _tasks
      ..clear()
      ..addAll(savedTasks);
  } catch (error) {
    _errorMessage = 'Gagal membaca task';
  } finally {
    _isLoading = false;
    notifyListeners();
  }
}
```

Penjelasan:

- `try` dipakai untuk menangani error.
- Saat load dimulai, `isLoading` dibuat `true`.
- Jika berhasil, data storage masuk ke `_tasks`.
- Jika gagal, `_errorMessage` diisi.
- `finally` memastikan loading selesai.
- `notifyListeners()` membuat UI update.

---

## 8. Helper saveCurrentTasks

Tambahkan helper:

```dart
Future<void> _saveCurrentTasks() async {
  try {
    await _storageService.saveTasks(_tasks);
  } catch (error) {
    _errorMessage = 'Gagal menyimpan task';
    notifyListeners();
  }
}
```

Kenapa private?

Karena UI tidak perlu memanggil save storage langsung. UI cukup memanggil `addTask`, `updateTask`, atau `deleteTask`. Provider yang mengurus kapan storage harus disimpan.

---

## 9. Computed State: visibleTasks dan emptyMessage

Tambahkan:

```dart
List<Task> get visibleTasks {
  final filteredByStatus = _selectedStatus == null
      ? _tasks
      : _tasks.where((task) => task.status == _selectedStatus).toList();

  final query = _searchQuery.toLowerCase();

  if (query.isEmpty) {
    return filteredByStatus;
  }

  return filteredByStatus.where((task) {
    final title = task.title.toLowerCase();
    final description = task.description.toLowerCase();

    return title.contains(query) || description.contains(query);
  }).toList();
}

String get emptyMessage {
  if (_searchQuery.isNotEmpty) {
    return 'Task tidak ditemukan';
  }

  if (_selectedStatus != null) {
    return 'Belum ada task dengan status ini';
  }

  return 'Belum ada task';
}
```

Penjelasan:

- `visibleTasks` adalah hasil akhir setelah filter dan search.
- UI tidak perlu menghitung filter sendiri.
- `emptyMessage` membuat pesan kosong sesuai kondisi.

---

## 10. Add Task + Save Storage

Tambahkan:

```dart
Future<void> addTask({
  required String title,
  required String description,
  TaskStatus status = TaskStatus.todo,
}) async {
  final task = Task(
    id: DateTime.now().millisecondsSinceEpoch,
    title: title,
    description: description,
    status: status,
    createdAt: DateTime.now(),
  );

  _tasks.add(task);
  notifyListeners();

  await _saveCurrentTasks();
}
```

Alur:

```text
UI memanggil addTask
-> provider membuat Task baru
-> Task masuk ke _tasks
-> notifyListeners
-> UI update
-> provider menyimpan _tasks ke storage
```

---

## 11. Update Task + Save Storage

Tambahkan:

```dart
Future<void> updateTask(Task updatedTask) async {
  final index = _tasks.indexWhere((task) => task.id == updatedTask.id);
  if (index == -1) return;

  _tasks[index] = updatedTask;
  notifyListeners();

  await _saveCurrentTasks();
}
```

Penjelasan:

- task dicari berdasarkan `id`
- jika tidak ditemukan, function berhenti
- jika ditemukan, task lama diganti
- storage disimpan ulang

---

## 12. Update Status + Save Storage

Tambahkan:

```dart
Future<void> updateStatus(int id, TaskStatus status) async {
  final index = _tasks.indexWhere((task) => task.id == id);
  if (index == -1) return;

  _tasks[index] = _tasks[index].copyWith(status: status);
  notifyListeners();

  await _saveCurrentTasks();
}
```

Kenapa memakai `copyWith`?

Karena model `Task` immutable. Saat status berubah, kita membuat object baru dari object lama.

---

## 13. Delete Task + Save Storage

Tambahkan:

```dart
Future<void> deleteTask(int id) async {
  _tasks.removeWhere((task) => task.id == id);
  notifyListeners();

  await _saveCurrentTasks();
}
```

Alur:

```text
Task dihapus dari _tasks
-> UI update
-> storage ditimpa dengan list terbaru
```

Jika task dihapus dari UI tapi storage tidak di-update, task akan muncul lagi saat aplikasi dibuka ulang.

---

## 14. Filter dan Search

Tambahkan:

```dart
void setStatusFilter(TaskStatus? status) {
  _selectedStatus = status;
  notifyListeners();
}

void setSearchQuery(String query) {
  _searchQuery = query;
  notifyListeners();
}
```

Kenapa filter/search tidak perlu save storage?

Karena filter dan search hanya memengaruhi tampilan, bukan data utama.

```text
Tambah/edit/delete -> data berubah -> save storage
Filter/search -> tampilan berubah -> tidak perlu save storage
```

---

## 15. TaskProvider Lengkap

Gabungan final:

```dart
import 'package:flutter/foundation.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';

class TaskProvider extends ChangeNotifier {
  final TaskStorageService _storageService;

  TaskProvider({
    TaskStorageService? storageService,
  }) : _storageService = storageService ?? TaskStorageService() {
    loadTasks();
  }

  final List<Task> _tasks = [];
  TaskStatus? _selectedStatus;
  String _searchQuery = '';
  bool _isLoading = true;
  String? _errorMessage;

  List<Task> get tasks => List.unmodifiable(_tasks);
  TaskStatus? get selectedStatus => _selectedStatus;
  String get searchQuery => _searchQuery;
  bool get isLoading => _isLoading;
  String? get errorMessage => _errorMessage;

  List<Task> get visibleTasks {
    final filteredByStatus = _selectedStatus == null
        ? _tasks
        : _tasks.where((task) => task.status == _selectedStatus).toList();

    final query = _searchQuery.toLowerCase();

    if (query.isEmpty) {
      return filteredByStatus;
    }

    return filteredByStatus.where((task) {
      final title = task.title.toLowerCase();
      final description = task.description.toLowerCase();

      return title.contains(query) || description.contains(query);
    }).toList();
  }

  String get emptyMessage {
    if (_searchQuery.isNotEmpty) {
      return 'Task tidak ditemukan';
    }

    if (_selectedStatus != null) {
      return 'Belum ada task dengan status ini';
    }

    return 'Belum ada task';
  }

  Future<void> loadTasks() async {
    try {
      _isLoading = true;
      _errorMessage = null;
      notifyListeners();

      final savedTasks = await _storageService.loadTasks();

      _tasks
        ..clear()
        ..addAll(savedTasks);
    } catch (error) {
      _errorMessage = 'Gagal membaca task';
    } finally {
      _isLoading = false;
      notifyListeners();
    }
  }

  Future<void> _saveCurrentTasks() async {
    try {
      await _storageService.saveTasks(_tasks);
    } catch (error) {
      _errorMessage = 'Gagal menyimpan task';
      notifyListeners();
    }
  }

  Future<void> addTask({
    required String title,
    required String description,
    TaskStatus status = TaskStatus.todo,
  }) async {
    final task = Task(
      id: DateTime.now().millisecondsSinceEpoch,
      title: title,
      description: description,
      status: status,
      createdAt: DateTime.now(),
    );

    _tasks.add(task);
    notifyListeners();

    await _saveCurrentTasks();
  }

  Future<void> updateTask(Task updatedTask) async {
    final index = _tasks.indexWhere((task) => task.id == updatedTask.id);
    if (index == -1) return;

    _tasks[index] = updatedTask;
    notifyListeners();

    await _saveCurrentTasks();
  }

  Future<void> updateStatus(int id, TaskStatus status) async {
    final index = _tasks.indexWhere((task) => task.id == id);
    if (index == -1) return;

    _tasks[index] = _tasks[index].copyWith(status: status);
    notifyListeners();

    await _saveCurrentTasks();
  }

  Future<void> deleteTask(int id) async {
    _tasks.removeWhere((task) => task.id == id);
    notifyListeners();

    await _saveCurrentTasks();
  }

  void setStatusFilter(TaskStatus? status) {
    _selectedStatus = status;
    notifyListeners();
  }

  void setSearchQuery(String query) {
    _searchQuery = query;
    notifyListeners();
  }
}
```

---

## 16. Daftarkan Provider di main.dart

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'pages/task_list_page.dart';
import 'providers/task_provider.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => TaskProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Task Manager',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const TaskListPage(),
    );
  }
}
```

Sekarang `TaskProvider` tersedia untuk halaman di bawah `MyApp`.

---

## 17. Membaca Provider di TaskListPage

Contoh struktur:

```dart
class TaskListPage extends StatelessWidget {
  const TaskListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TaskProvider>();

    if (provider.isLoading) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Task Manager'),
        ),
        body: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (provider.errorMessage != null) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Task Manager'),
        ),
        body: Center(
          child: Text(provider.errorMessage!),
        ),
      );
    }

    final visibleTasks = provider.visibleTasks;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Manager'),
      ),
      body: Column(
        children: [
          // Search, filter, dan list task
        ],
      ),
    );
  }
}
```

Penjelasan:

- `context.watch<TaskProvider>()` membuat UI rebuild saat provider berubah.
- Loading dan error dibaca dari provider.
- UI tidak lagi menyimpan `List<Task>` sendiri.

---

## 18. Search dengan Provider

```dart
TextField(
  decoration: const InputDecoration(
    labelText: 'Cari task',
    prefixIcon: Icon(Icons.search),
    border: OutlineInputBorder(),
  ),
  onChanged: (value) {
    context.read<TaskProvider>().setSearchQuery(value);
  },
)
```

Gunakan `read` karena action ini hanya memanggil function.

---

## 19. Filter dengan Provider

```dart
final provider = context.watch<TaskProvider>();

SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: Row(
    children: [
      ChoiceChip(
        label: const Text('Semua'),
        selected: provider.selectedStatus == null,
        onSelected: (_) {
          context.read<TaskProvider>().setStatusFilter(null);
        },
      ),
      const SizedBox(width: 8),
      ...TaskStatus.values.map((status) {
        return Padding(
          padding: const EdgeInsets.only(right: 8),
          child: ChoiceChip(
            label: Text(status.label),
            selected: provider.selectedStatus == status,
            onSelected: (_) {
              context.read<TaskProvider>().setStatusFilter(status);
            },
          ),
        );
      }),
    ],
  ),
)
```

Filter tidak perlu save storage karena hanya mengatur tampilan.

---

## 20. List Task dengan Provider

```dart
Expanded(
  child: visibleTasks.isEmpty
      ? Center(
          child: Text(provider.emptyMessage),
        )
      : ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: visibleTasks.length,
          itemBuilder: (context, index) {
            final task = visibleTasks[index];

            return TaskCard(
              task: task,
              onEdit: () => openEditPage(context, task),
              onDelete: () => confirmDelete(context, task),
              onStatusChanged: (status) {
                context.read<TaskProvider>().updateStatus(
                      task.id,
                      status,
                    );
              },
            );
          },
        ),
)
```

Perhatikan:

- data diambil dari `provider.visibleTasks`
- update status dipanggil lewat provider
- setelah status berubah, provider akan save storage

---

## 21. Add Task dari Form

Jika `TaskFormPage` mengembalikan object `Task`, kamu bisa memakai:

```dart
Future<void> openCreatePage(BuildContext context) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => const TaskFormPage(),
    ),
  );

  if (result == null || !context.mounted) return;

  await context.read<TaskProvider>().addTask(
        title: result.title,
        description: result.description,
        status: result.status,
      );
}
```

Catatan:

Jika form langsung mengirim `title`, `description`, dan `status`, maka provider bisa dipanggil langsung dari form. Tetapi untuk pemula, pola form mengembalikan `Task` masih mudah dipahami.

---

## 22. Edit Task dari Form

```dart
Future<void> openEditPage(BuildContext context, Task task) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => TaskFormPage(task: task),
    ),
  );

  if (result == null || !context.mounted) return;

  await context.read<TaskProvider>().updateTask(result);
}
```

Alur:

```text
User edit task
-> TaskFormPage mengembalikan Task baru
-> provider.updateTask dipanggil
-> _tasks diperbarui
-> notifyListeners
-> storage disimpan ulang
```

---

## 23. Delete Task dengan Konfirmasi

```dart
Future<void> confirmDelete(BuildContext context, Task task) async {
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

  if (result != true || !context.mounted) return;

  await context.read<TaskProvider>().deleteTask(task.id);
}
```

Setelah `deleteTask` dipanggil:

```text
task dihapus dari provider
-> UI update
-> storage update
```

---

## 24. Kenapa UI Jadi Lebih Bersih

Sebelumnya, UI harus mengurus:

- list task
- loading
- error
- load storage
- save storage
- filter
- search
- add
- edit
- delete

Setelah Provider:

```text
UI hanya:
-> menampilkan data
-> menerima input
-> memanggil action provider
```

Logic pindah ke provider:

```text
Provider:
-> menyimpan state
-> menghitung visibleTasks
-> save/load storage
-> CRUD
```

Ini membuat project lebih mudah dikembangkan.

---

## 25. Testing Manual

Test yang perlu dilakukan:

1. Buka aplikasi.
2. Pastikan loading muncul sebentar.
3. Tambah task.
4. Tutup dan buka aplikasi.
5. Pastikan task masih ada.
6. Edit task.
7. Tutup dan buka aplikasi.
8. Pastikan edit tersimpan.
9. Ubah status task.
10. Tutup dan buka aplikasi.
11. Pastikan status tersimpan.
12. Hapus task.
13. Tutup dan buka aplikasi.
14. Pastikan task tidak muncul lagi.
15. Coba filter dan search.
16. Pastikan filter/search tidak menghapus data asli.

---

## 26. Kesalahan Umum

### Lupa notifyListeners

Jika state berubah tapi UI tidak update, cek apakah `notifyListeners()` sudah dipanggil.

### Lupa save storage

Jika data muncul tapi hilang saat restart, kemungkinan action provider belum memanggil `_saveCurrentTasks()`.

### UI masih mengubah list langsung

Jangan lakukan:

```dart
provider.tasks.add(task);
```

Karena `tasks` seharusnya hanya dibaca. Gunakan:

```dart
context.read<TaskProvider>().addTask(...);
```

### Filter/search ikut disimpan

Filter dan search tidak wajib disimpan ke storage. Yang disimpan adalah data task.

---

## 27. Checklist Upgrade Provider Storage

Pastikan sudah selesai:

- [ ] Ada `TaskStorageService`.
- [ ] Ada `TaskProvider`.
- [ ] Provider load task saat dibuat.
- [ ] Provider punya `isLoading`.
- [ ] Provider punya `errorMessage`.
- [ ] Provider punya `visibleTasks`.
- [ ] Provider punya `emptyMessage`.
- [ ] Provider save storage saat add.
- [ ] Provider save storage saat edit.
- [ ] Provider save storage saat update status.
- [ ] Provider save storage saat delete.
- [ ] UI membaca task dari provider.
- [ ] UI tidak lagi menyimpan `List<Task>` sendiri.
- [ ] Data tetap ada setelah aplikasi ditutup.

Jika checklist ini aman, kamu sudah punya Task Manager yang lebih rapi dengan Provider dan local storage.

---

## 28. Lanjutan Setelah Ini

Langkah berikutnya:

1. Upgrade Task Manager dengan Riverpod + Local Storage.
2. Upgrade Task Manager dengan Cubit + Local Storage.
3. Simpan task ke Hive/Isar.
4. Sinkron task ke Firestore.
5. Tambahkan login user.

Urutan yang disarankan:

```text
Provider + shared_preferences
-> Riverpod + shared_preferences
-> Cubit + shared_preferences
-> Firestore
```
