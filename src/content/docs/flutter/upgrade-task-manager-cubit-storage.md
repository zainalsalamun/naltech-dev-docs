---
title: "Upgrade Task Manager dengan Cubit dan Local Storage"
description: "Tutorial upgrade Task Manager agar memakai Cubit/flutter_bloc untuk state management dan shared_preferences untuk local storage."
category: "Flutter"
level: "Project"
order: 60
tags: ["flutter", "cubit", "bloc", "task-manager", "shared-preferences", "local-storage"]
updated: "2026-05-23"
---

# Upgrade Task Manager dengan Cubit dan Local Storage

Pada materi ini, kita upgrade Task Manager agar memakai Cubit sebagai state management dan `shared_preferences` sebagai local storage. Cubit cocok untuk project yang ingin state lebih rapi, eksplisit, dan mudah dipisahkan dari UI tanpa boilerplate Bloc yang terlalu banyak.

Target:

- `TaskStorageService` mengurus save/load storage.
- `TaskState` menyimpan semua state layar.
- `TaskCubit` mengelola CRUD, filter, search, loading, error, dan storage.
- UI membaca state dengan `BlocBuilder`.
- UI memanggil action dengan `context.read<TaskCubit>()`.
- Error bisa ditangani dengan `BlocListener`.

---

## 1. Gambaran Arsitektur

Arsitektur yang akan dibuat:

```text
TaskListPage
-> membaca TaskState dari TaskCubit
-> memanggil action Cubit

TaskCubit
-> menyimpan TaskState
-> mengelola CRUD
-> mengelola filter/search
-> load dan save storage

TaskState
-> tasks
-> selectedStatus
-> searchQuery
-> isLoading
-> errorMessage

TaskStorageService
-> shared_preferences
```

Pembagian tugas:

| Bagian | Tugas |
| --- | --- |
| `TaskListPage` | Menampilkan UI |
| `TaskCubit` | Logic dan perubahan state |
| `TaskState` | Kondisi layar saat ini |
| `TaskStorageService` | Save/load local storage |
| `Task` | Bentuk data |

---

## 2. Install Package

Tambahkan:

```bash
flutter pub add flutter_bloc
flutter pub add shared_preferences
```

Lalu:

```bash
flutter pub get
```

Import:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';
```

---

## 3. Struktur Folder

Struktur yang disarankan:

```text
lib/
  main.dart
  models/
    task.dart
  cubits/
    task_cubit.dart
    task_state.dart
  pages/
    task_list_page.dart
    task_form_page.dart
  services/
    task_storage_service.dart
  widgets/
    task_card.dart
    task_status_chip.dart
```

File baru:

```text
lib/cubits/task_state.dart
lib/cubits/task_cubit.dart
```

---

## 4. Model Task

Model tetap memakai `toJson` dan `fromJson`.

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

---

## 6. Membuat TaskState

Buat file:

```text
lib/cubits/task_state.dart
```

Isi:

```dart
import '../models/task.dart';

class TaskState {
  final List<Task> tasks;
  final TaskStatus? selectedStatus;
  final String searchQuery;
  final bool isLoading;
  final String? errorMessage;

  const TaskState({
    this.tasks = const [],
    this.selectedStatus,
    this.searchQuery = '',
    this.isLoading = false,
    this.errorMessage,
  });

  List<Task> get visibleTasks {
    final filteredByStatus = selectedStatus == null
        ? tasks
        : tasks.where((task) => task.status == selectedStatus).toList();

    final query = searchQuery.toLowerCase();

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
    if (searchQuery.isNotEmpty) {
      return 'Task tidak ditemukan';
    }

    if (selectedStatus != null) {
      return 'Belum ada task dengan status ini';
    }

    return 'Belum ada task';
  }

  TaskState copyWith({
    List<Task>? tasks,
    TaskStatus? selectedStatus,
    bool clearSelectedStatus = false,
    String? searchQuery,
    bool? isLoading,
    String? errorMessage,
    bool clearError = false,
  }) {
    return TaskState(
      tasks: tasks ?? this.tasks,
      selectedStatus: clearSelectedStatus
          ? null
          : selectedStatus ?? this.selectedStatus,
      searchQuery: searchQuery ?? this.searchQuery,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}
```

Penjelasan:

- `tasks` menyimpan semua data task.
- `selectedStatus` menyimpan filter.
- `searchQuery` menyimpan keyword.
- `isLoading` dipakai saat load storage.
- `errorMessage` dipakai untuk error.
- `visibleTasks` menghitung hasil filter dan search.
- `copyWith` membuat state baru.

---

## 7. Membuat TaskCubit

Buat file:

```text
lib/cubits/task_cubit.dart
```

Isi awal:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';
import 'task_state.dart';

class TaskCubit extends Cubit<TaskState> {
  final TaskStorageService _storageService;

  TaskCubit({
    TaskStorageService? storageService,
  })  : _storageService = storageService ?? TaskStorageService(),
        super(const TaskState(isLoading: true)) {
    loadTasks();
  }
}
```

Penjelasan:

- Cubit menyimpan `TaskState`.
- State awal `isLoading: true`.
- `loadTasks()` dipanggil saat Cubit dibuat.
- `TaskStorageService` bisa di-inject agar lebih mudah dites.

---

## 8. Load Tasks

Tambahkan:

```dart
Future<void> loadTasks() async {
  emit(
    state.copyWith(
      isLoading: true,
      clearError: true,
    ),
  );

  try {
    final savedTasks = await _storageService.loadTasks();

    emit(
      state.copyWith(
        tasks: savedTasks,
        isLoading: false,
        clearError: true,
      ),
    );
  } catch (error) {
    emit(
      state.copyWith(
        isLoading: false,
        errorMessage: 'Gagal membaca task',
      ),
    );
  }
}
```

Alur:

```text
emit loading true
-> baca storage
-> jika berhasil emit data
-> jika gagal emit error
```

---

## 9. Helper Save Current Tasks

Tambahkan:

```dart
Future<void> _saveCurrentTasks(List<Task> tasks) async {
  try {
    await _storageService.saveTasks(tasks);
  } catch (error) {
    emit(
      state.copyWith(
        errorMessage: 'Gagal menyimpan task',
      ),
    );
  }
}
```

Function ini private karena UI tidak perlu memanggil storage langsung.

---

## 10. Add Task

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

  final updatedTasks = [...state.tasks, task];

  emit(
    state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    ),
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Perhatikan:

- membuat task baru
- membuat list baru
- emit state baru
- save ke storage

---

## 11. Update Task

Tambahkan:

```dart
Future<void> updateTask(Task updatedTask) async {
  final updatedTasks = [
    for (final task in state.tasks)
      if (task.id == updatedTask.id) updatedTask else task,
  ];

  emit(
    state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    ),
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Alur:

```text
Cari task dengan id sama
-> ganti dengan updatedTask
-> emit list baru
-> save storage
```

---

## 12. Update Status

Tambahkan:

```dart
Future<void> updateStatus(int id, TaskStatus status) async {
  final updatedTasks = [
    for (final task in state.tasks)
      if (task.id == id) task.copyWith(status: status) else task,
  ];

  emit(
    state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    ),
  );

  await _saveCurrentTasks(updatedTasks);
}
```

`copyWith` dipakai agar object lama tidak diubah langsung.

---

## 13. Delete Task

Tambahkan:

```dart
Future<void> deleteTask(int id) async {
  final updatedTasks = state.tasks
      .where((task) => task.id != id)
      .toList();

  emit(
    state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    ),
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Jika storage tidak ikut disimpan setelah delete, task akan muncul kembali saat aplikasi dibuka ulang.

---

## 14. Filter dan Search

Tambahkan:

```dart
void setStatusFilter(TaskStatus? status) {
  emit(
    state.copyWith(
      selectedStatus: status,
      clearSelectedStatus: status == null,
    ),
  );
}

void setSearchQuery(String query) {
  emit(
    state.copyWith(searchQuery: query),
  );
}
```

Filter dan search tidak perlu save storage karena hanya mengubah tampilan.

---

## 15. TaskCubit Lengkap

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';
import 'task_state.dart';

class TaskCubit extends Cubit<TaskState> {
  final TaskStorageService _storageService;

  TaskCubit({
    TaskStorageService? storageService,
  })  : _storageService = storageService ?? TaskStorageService(),
        super(const TaskState(isLoading: true)) {
    loadTasks();
  }

  Future<void> loadTasks() async {
    emit(
      state.copyWith(
        isLoading: true,
        clearError: true,
      ),
    );

    try {
      final savedTasks = await _storageService.loadTasks();

      emit(
        state.copyWith(
          tasks: savedTasks,
          isLoading: false,
          clearError: true,
        ),
      );
    } catch (error) {
      emit(
        state.copyWith(
          isLoading: false,
          errorMessage: 'Gagal membaca task',
        ),
      );
    }
  }

  Future<void> _saveCurrentTasks(List<Task> tasks) async {
    try {
      await _storageService.saveTasks(tasks);
    } catch (error) {
      emit(
        state.copyWith(
          errorMessage: 'Gagal menyimpan task',
        ),
      );
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

    final updatedTasks = [...state.tasks, task];

    emit(
      state.copyWith(
        tasks: updatedTasks,
        clearError: true,
      ),
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateTask(Task updatedTask) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == updatedTask.id) updatedTask else task,
    ];

    emit(
      state.copyWith(
        tasks: updatedTasks,
        clearError: true,
      ),
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateStatus(int id, TaskStatus status) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == id) task.copyWith(status: status) else task,
    ];

    emit(
      state.copyWith(
        tasks: updatedTasks,
        clearError: true,
      ),
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> deleteTask(int id) async {
    final updatedTasks = state.tasks
        .where((task) => task.id != id)
        .toList();

    emit(
      state.copyWith(
        tasks: updatedTasks,
        clearError: true,
      ),
    );

    await _saveCurrentTasks(updatedTasks);
  }

  void setStatusFilter(TaskStatus? status) {
    emit(
      state.copyWith(
        selectedStatus: status,
        clearSelectedStatus: status == null,
      ),
    );
  }

  void setSearchQuery(String query) {
    emit(
      state.copyWith(searchQuery: query),
    );
  }
}
```

---

## 16. Daftarkan Cubit di main.dart

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'cubits/task_cubit.dart';
import 'pages/task_list_page.dart';

void main() {
  runApp(
    BlocProvider(
      create: (context) => TaskCubit(),
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
      title: 'Task Manager Cubit',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const TaskListPage(),
    );
  }
}
```

---

## 17. Membaca State di UI

Gunakan `BlocBuilder`.

```dart
class TaskListPage extends StatelessWidget {
  const TaskListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocBuilder<TaskCubit, TaskState>(
      builder: (context, state) {
        if (state.isLoading) {
          return Scaffold(
            appBar: AppBar(
              title: const Text('Task Manager'),
            ),
            body: const Center(
              child: CircularProgressIndicator(),
            ),
          );
        }

        if (state.errorMessage != null) {
          return Scaffold(
            appBar: AppBar(
              title: const Text('Task Manager'),
            ),
            body: Center(
              child: Text(state.errorMessage!),
            ),
          );
        }

        final visibleTasks = state.visibleTasks;

        return Scaffold(
          appBar: AppBar(
            title: const Text('Task Manager'),
          ),
          body: Column(
            children: [
              // search, filter, list
            ],
          ),
        );
      },
    );
  }
}
```

Penjelasan:

- `BlocBuilder` rebuild saat `TaskState` berubah.
- UI membaca `isLoading`, `errorMessage`, dan `visibleTasks` dari state.

---

## 18. BlocListener untuk Error

Jika ingin error tampil sebagai `SnackBar`, gunakan `BlocListener`.

```dart
BlocListener<TaskCubit, TaskState>(
  listenWhen: (previous, current) {
    return previous.errorMessage != current.errorMessage &&
        current.errorMessage != null;
  },
  listener: (context, state) {
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text(state.errorMessage!),
      ),
    );
  },
  child: BlocBuilder<TaskCubit, TaskState>(
    builder: (context, state) {
      return const SizedBox();
    },
  ),
)
```

Catatan:

- `BlocBuilder` untuk UI.
- `BlocListener` untuk side effect seperti `SnackBar`.

---

## 19. Search dengan Cubit

```dart
TextField(
  decoration: const InputDecoration(
    labelText: 'Cari task',
    prefixIcon: Icon(Icons.search),
    border: OutlineInputBorder(),
  ),
  onChanged: (value) {
    context.read<TaskCubit>().setSearchQuery(value);
  },
)
```

Search tidak perlu disimpan ke local storage karena hanya memengaruhi tampilan.

---

## 20. Filter dengan Cubit

```dart
SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: Row(
    children: [
      ChoiceChip(
        label: const Text('Semua'),
        selected: state.selectedStatus == null,
        onSelected: (_) {
          context.read<TaskCubit>().setStatusFilter(null);
        },
      ),
      const SizedBox(width: 8),
      ...TaskStatus.values.map((status) {
        return Padding(
          padding: const EdgeInsets.only(right: 8),
          child: ChoiceChip(
            label: Text(status.label),
            selected: state.selectedStatus == status,
            onSelected: (_) {
              context.read<TaskCubit>().setStatusFilter(status);
            },
          ),
        );
      }),
    ],
  ),
)
```

---

## 21. List Task dengan Cubit

```dart
Expanded(
  child: visibleTasks.isEmpty
      ? Center(
          child: Text(state.emptyMessage),
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
                context.read<TaskCubit>().updateStatus(
                      task.id,
                      status,
                    );
              },
            );
          },
        ),
)
```

---

## 22. Add Task

```dart
Future<void> openCreatePage(BuildContext context) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => const TaskFormPage(),
    ),
  );

  if (result == null || !context.mounted) return;

  await context.read<TaskCubit>().addTask(
        title: result.title,
        description: result.description,
        status: result.status,
      );
}
```

---

## 23. Edit Task

```dart
Future<void> openEditPage(BuildContext context, Task task) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => TaskFormPage(task: task),
    ),
  );

  if (result == null || !context.mounted) return;

  await context.read<TaskCubit>().updateTask(result);
}
```

---

## 24. Delete Task

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

  await context.read<TaskCubit>().deleteTask(task.id);
}
```

---

## 25. Kenapa Cubit Lebih Rapi

Sebelum Cubit:

```text
UI menyimpan state
UI mengubah state
UI save storage
UI filter/search
```

Setelah Cubit:

```text
UI menampilkan state
UI memanggil action
Cubit mengubah state
Cubit save storage
```

Keuntungan:

- UI lebih pendek.
- Logic lebih mudah dites.
- Perubahan state lebih eksplisit.
- Loading/error/data berada dalam satu `TaskState`.
- Cocok untuk project yang mulai kompleks.

---

## 26. Testing Manual

Test:

1. Buka aplikasi.
2. Pastikan loading muncul.
3. Tambah task.
4. Tutup dan buka aplikasi.
5. Pastikan task masih ada.
6. Edit task.
7. Tutup dan buka aplikasi.
8. Pastikan edit tersimpan.
9. Ubah status.
10. Tutup dan buka aplikasi.
11. Pastikan status tersimpan.
12. Hapus task.
13. Tutup dan buka aplikasi.
14. Pastikan task hilang.
15. Coba filter/search.
16. Pastikan filter/search tidak menghapus data asli.

---

## 27. Kesalahan Umum

### Lupa emit

Jika state berubah tapi UI tidak update, cek apakah sudah memakai `emit`.

### Mengubah list lama langsung

Kurang aman:

```dart
state.tasks.add(task);
emit(state);
```

Lebih baik:

```dart
final updatedTasks = [...state.tasks, task];
emit(state.copyWith(tasks: updatedTasks));
```

### Side effect di BlocBuilder

Jangan menampilkan `SnackBar` atau navigasi dari `BlocBuilder`. Gunakan `BlocListener`.

### Lupa save storage

Jika data hilang setelah restart, cek apakah action sudah memanggil `_saveCurrentTasks`.

---

## 28. Checklist Cubit + Storage

Pastikan sudah selesai:

- [ ] Ada `TaskStorageService`.
- [ ] Ada `TaskState`.
- [ ] Ada `TaskCubit`.
- [ ] Cubit load task saat dibuat.
- [ ] State punya `isLoading`.
- [ ] State punya `errorMessage`.
- [ ] State punya `visibleTasks`.
- [ ] State punya `emptyMessage`.
- [ ] Cubit save storage saat add.
- [ ] Cubit save storage saat edit.
- [ ] Cubit save storage saat update status.
- [ ] Cubit save storage saat delete.
- [ ] UI memakai `BlocProvider`.
- [ ] UI memakai `BlocBuilder`.
- [ ] UI memakai `BlocListener` untuk error jika diperlukan.
- [ ] UI memanggil action dengan `context.read<TaskCubit>()`.
- [ ] Data tetap ada setelah aplikasi ditutup.

Jika checklist ini aman, kamu sudah memahami pola Cubit + local storage.

---

## 29. Perbandingan Singkat

| Pendekatan | Cocok Untuk | Kelebihan |
| --- | --- | --- |
| `setState` | belajar dasar | sederhana |
| Provider | pemula-menengah | mudah dipahami |
| Riverpod | modern/scalable | tidak bergantung context |
| Cubit | project menengah-besar | state eksplisit dan rapi |
| Bloc | flow kompleks | event-state sangat jelas |

Untuk project pribadi, Cubit sering cukup. Untuk flow yang sangat kompleks, baru pertimbangkan Bloc penuh.

---

## 30. Lanjutan Setelah Ini

Setelah ini, materi yang paling cocok:

1. Repository Pattern sederhana.
2. Firebase Auth.
3. Firestore CRUD.
4. Task Manager sync ke Firestore.
5. Clean Architecture sederhana.

Urutan yang disarankan:

```text
Cubit + shared_preferences
-> Repository Pattern
-> Firebase Auth
-> Firestore CRUD
```
