---
title: "Upgrade Task Manager dengan Riverpod dan Local Storage"
description: "Tutorial upgrade Task Manager agar memakai Riverpod untuk state management dan shared_preferences untuk local storage."
category: "Flutter"
level: "Project"
order: 59
tags: ["flutter", "riverpod", "task-manager", "shared-preferences", "local-storage"]
updated: "2026-05-23"
---

# Upgrade Task Manager dengan Riverpod dan Local Storage

Pada materi ini, kita upgrade Task Manager agar memakai Riverpod sebagai state management dan `shared_preferences` sebagai local storage. Pola ini lebih modern daripada `setState`, dan lebih terpisah dari `BuildContext` dibanding Provider biasa.

Target:

- `TaskStorageService` tetap mengurus local storage.
- `TaskNotifier` mengelola CRUD task.
- `NotifierProvider` menyediakan list task.
- `StateProvider` mengelola filter dan search.
- `Provider` menghitung `visibleTasks` dan `emptyMessage`.
- Data task di-load saat notifier dibuat.
- Storage update saat add/edit/delete/update status.

---

## 1. Gambaran Arsitektur

Arsitektur yang akan dibuat:

```text
TaskListPage
-> membaca state dengan ref.watch
-> memanggil action dengan ref.read

TaskNotifier
-> mengelola List<Task>
-> load dari TaskStorageService
-> save ke TaskStorageService

StateProvider
-> selectedStatus
-> searchQuery

Provider
-> visibleTasks
-> emptyMessage

TaskStorageService
-> shared_preferences
```

Pembagian tugas:

| Bagian | Tugas |
| --- | --- |
| `TaskListPage` | Menampilkan UI |
| `TaskNotifier` | CRUD task dan storage |
| `StateProvider` | State kecil seperti filter/search |
| `Provider` | Data turunan seperti visible tasks |
| `TaskStorageService` | Save/load shared preferences |

---

## 2. Install Package

Tambahkan:

```bash
flutter pub add flutter_riverpod
flutter pub add shared_preferences
```

Lalu:

```bash
flutter pub get
```

Import:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
```

---

## 3. Struktur Folder

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
    task_providers.dart
  services/
    task_storage_service.dart
  widgets/
    task_card.dart
    task_status_chip.dart
```

File baru:

```text
lib/providers/task_providers.dart
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

Service tetap sama seperti materi sebelumnya.

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

## 6. ProviderScope di main.dart

Riverpod membutuhkan `ProviderScope`.

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'pages/task_list_page.dart';

void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Task Manager Riverpod',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const TaskListPage(),
    );
  }
}
```

Jika `ProviderScope` tidak dipasang, provider Riverpod tidak bisa dibaca.

---

## 7. Membuat TaskState

Karena kita butuh loading dan error, buat state khusus.

```dart
class TaskState {
  final List<Task> tasks;
  final bool isLoading;
  final String? errorMessage;

  const TaskState({
    this.tasks = const [],
    this.isLoading = false,
    this.errorMessage,
  });

  TaskState copyWith({
    List<Task>? tasks,
    bool? isLoading,
    String? errorMessage,
    bool clearError = false,
  }) {
    return TaskState(
      tasks: tasks ?? this.tasks,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}
```

Penjelasan:

- `tasks` menyimpan data task.
- `isLoading` dipakai saat load storage.
- `errorMessage` dipakai jika load/save gagal.
- `copyWith` membuat state baru dari state lama.

---

## 8. Membuat Storage Provider

Di file:

```text
lib/providers/task_providers.dart
```

Tambahkan:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';

final taskStorageServiceProvider = Provider<TaskStorageService>((ref) {
  return TaskStorageService();
});
```

Kenapa service dibuat provider?

Supaya `TaskNotifier` bisa membaca service dari Riverpod. Ini juga memudahkan testing karena service bisa di-override.

---

## 9. Membuat TaskNotifier

Tambahkan:

```dart
class TaskNotifier extends Notifier<TaskState> {
  late final TaskStorageService _storageService;

  @override
  TaskState build() {
    _storageService = ref.read(taskStorageServiceProvider);
    loadTasks();

    return const TaskState(isLoading: true);
  }
}
```

Penjelasan:

- `TaskNotifier` mengelola `TaskState`.
- `build()` adalah tempat state awal dibuat.
- `loadTasks()` dipanggil saat notifier dibuat.
- State awal `isLoading: true` karena data sedang dibaca.

---

## 10. Load Tasks

Tambahkan function:

```dart
Future<void> loadTasks() async {
  state = state.copyWith(
    isLoading: true,
    clearError: true,
  );

  try {
    final savedTasks = await _storageService.loadTasks();

    state = state.copyWith(
      tasks: savedTasks,
      isLoading: false,
      clearError: true,
    );
  } catch (error) {
    state = state.copyWith(
      isLoading: false,
      errorMessage: 'Gagal membaca task',
    );
  }
}
```

Alur:

```text
state loading true
-> baca storage
-> jika berhasil, isi tasks
-> jika gagal, isi errorMessage
-> loading false
```

---

## 11. Helper Save Current Tasks

Tambahkan:

```dart
Future<void> _saveCurrentTasks(List<Task> tasks) async {
  try {
    await _storageService.saveTasks(tasks);
  } catch (error) {
    state = state.copyWith(
      errorMessage: 'Gagal menyimpan task',
    );
  }
}
```

Kenapa menerima parameter `tasks`?

Karena setelah membuat list baru, kita ingin menyimpan list terbaru tersebut langsung ke storage.

---

## 12. Add Task

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

  state = state.copyWith(
    tasks: updatedTasks,
    clearError: true,
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Perhatikan:

```dart
final updatedTasks = [...state.tasks, task];
```

Kita membuat list baru, bukan mengubah list lama secara langsung. Pola immutable seperti ini lebih cocok untuk Riverpod.

---

## 13. Update Task

Tambahkan:

```dart
Future<void> updateTask(Task updatedTask) async {
  final updatedTasks = [
    for (final task in state.tasks)
      if (task.id == updatedTask.id) updatedTask else task,
  ];

  state = state.copyWith(
    tasks: updatedTasks,
    clearError: true,
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Alur:

```text
Loop semua task
-> jika id sama, pakai updatedTask
-> jika id beda, pakai task lama
-> hasilnya menjadi list baru
```

---

## 14. Update Status

Tambahkan:

```dart
Future<void> updateStatus(int id, TaskStatus status) async {
  final updatedTasks = [
    for (final task in state.tasks)
      if (task.id == id) task.copyWith(status: status) else task,
  ];

  state = state.copyWith(
    tasks: updatedTasks,
    clearError: true,
  );

  await _saveCurrentTasks(updatedTasks);
}
```

`copyWith` dipakai karena `Task` immutable.

---

## 15. Delete Task

Tambahkan:

```dart
Future<void> deleteTask(int id) async {
  final updatedTasks = state.tasks
      .where((task) => task.id != id)
      .toList();

  state = state.copyWith(
    tasks: updatedTasks,
    clearError: true,
  );

  await _saveCurrentTasks(updatedTasks);
}
```

Jika storage tidak di-update setelah delete, task akan muncul lagi saat app dibuka ulang.

---

## 16. TaskNotifier Lengkap

```dart
class TaskNotifier extends Notifier<TaskState> {
  late final TaskStorageService _storageService;

  @override
  TaskState build() {
    _storageService = ref.read(taskStorageServiceProvider);
    loadTasks();

    return const TaskState(isLoading: true);
  }

  Future<void> loadTasks() async {
    state = state.copyWith(
      isLoading: true,
      clearError: true,
    );

    try {
      final savedTasks = await _storageService.loadTasks();

      state = state.copyWith(
        tasks: savedTasks,
        isLoading: false,
        clearError: true,
      );
    } catch (error) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Gagal membaca task',
      );
    }
  }

  Future<void> _saveCurrentTasks(List<Task> tasks) async {
    try {
      await _storageService.saveTasks(tasks);
    } catch (error) {
      state = state.copyWith(
        errorMessage: 'Gagal menyimpan task',
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

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateTask(Task updatedTask) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == updatedTask.id) updatedTask else task,
    ];

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateStatus(int id, TaskStatus status) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == id) task.copyWith(status: status) else task,
    ];

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> deleteTask(int id) async {
    final updatedTasks = state.tasks
        .where((task) => task.id != id)
        .toList();

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }
}
```

---

## 17. NotifierProvider

Tambahkan:

```dart
final taskNotifierProvider =
    NotifierProvider<TaskNotifier, TaskState>(TaskNotifier.new);
```

Membaca state:

```dart
final taskState = ref.watch(taskNotifierProvider);
```

Memanggil action:

```dart
await ref.read(taskNotifierProvider.notifier).addTask(
  title: 'Belajar Riverpod',
  description: 'Upgrade Task Manager',
);
```

---

## 18. Filter dan Search Provider

Tambahkan:

```dart
final selectedStatusProvider = StateProvider<TaskStatus?>((ref) {
  return null;
});

final searchQueryProvider = StateProvider<String>((ref) {
  return '';
});
```

Kenapa dipisah?

Karena filter dan search adalah state kecil. Tidak perlu masuk ke `TaskNotifier` jika ingin dipisahkan dengan jelas.

---

## 19. visibleTasksProvider

Tambahkan:

```dart
final visibleTasksProvider = Provider<List<Task>>((ref) {
  final taskState = ref.watch(taskNotifierProvider);
  final selectedStatus = ref.watch(selectedStatusProvider);
  final searchQuery = ref.watch(searchQueryProvider).toLowerCase();

  final filteredByStatus = selectedStatus == null
      ? taskState.tasks
      : taskState.tasks
          .where((task) => task.status == selectedStatus)
          .toList();

  if (searchQuery.isEmpty) {
    return filteredByStatus;
  }

  return filteredByStatus.where((task) {
    final title = task.title.toLowerCase();
    final description = task.description.toLowerCase();

    return title.contains(searchQuery) || description.contains(searchQuery);
  }).toList();
});
```

Penjelasan:

- Provider ini membaca task, filter, dan search.
- Jika salah satu berubah, hasil akan dihitung ulang.
- UI cukup membaca `visibleTasksProvider`.

---

## 20. emptyMessageProvider

Tambahkan:

```dart
final emptyMessageProvider = Provider<String>((ref) {
  final selectedStatus = ref.watch(selectedStatusProvider);
  final searchQuery = ref.watch(searchQueryProvider);

  if (searchQuery.isNotEmpty) {
    return 'Task tidak ditemukan';
  }

  if (selectedStatus != null) {
    return 'Belum ada task dengan status ini';
  }

  return 'Belum ada task';
});
```

UI tidak perlu membuat logic pesan kosong sendiri.

---

## 21. task_providers.dart Lengkap

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';

import '../models/task.dart';
import '../services/task_storage_service.dart';

final taskStorageServiceProvider = Provider<TaskStorageService>((ref) {
  return TaskStorageService();
});

class TaskState {
  final List<Task> tasks;
  final bool isLoading;
  final String? errorMessage;

  const TaskState({
    this.tasks = const [],
    this.isLoading = false,
    this.errorMessage,
  });

  TaskState copyWith({
    List<Task>? tasks,
    bool? isLoading,
    String? errorMessage,
    bool clearError = false,
  }) {
    return TaskState(
      tasks: tasks ?? this.tasks,
      isLoading: isLoading ?? this.isLoading,
      errorMessage: clearError ? null : errorMessage ?? this.errorMessage,
    );
  }
}

class TaskNotifier extends Notifier<TaskState> {
  late final TaskStorageService _storageService;

  @override
  TaskState build() {
    _storageService = ref.read(taskStorageServiceProvider);
    loadTasks();

    return const TaskState(isLoading: true);
  }

  Future<void> loadTasks() async {
    state = state.copyWith(
      isLoading: true,
      clearError: true,
    );

    try {
      final savedTasks = await _storageService.loadTasks();

      state = state.copyWith(
        tasks: savedTasks,
        isLoading: false,
        clearError: true,
      );
    } catch (error) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Gagal membaca task',
      );
    }
  }

  Future<void> _saveCurrentTasks(List<Task> tasks) async {
    try {
      await _storageService.saveTasks(tasks);
    } catch (error) {
      state = state.copyWith(
        errorMessage: 'Gagal menyimpan task',
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

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateTask(Task updatedTask) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == updatedTask.id) updatedTask else task,
    ];

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> updateStatus(int id, TaskStatus status) async {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == id) task.copyWith(status: status) else task,
    ];

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }

  Future<void> deleteTask(int id) async {
    final updatedTasks = state.tasks
        .where((task) => task.id != id)
        .toList();

    state = state.copyWith(
      tasks: updatedTasks,
      clearError: true,
    );

    await _saveCurrentTasks(updatedTasks);
  }
}

final taskNotifierProvider =
    NotifierProvider<TaskNotifier, TaskState>(TaskNotifier.new);

final selectedStatusProvider = StateProvider<TaskStatus?>((ref) {
  return null;
});

final searchQueryProvider = StateProvider<String>((ref) {
  return '';
});

final visibleTasksProvider = Provider<List<Task>>((ref) {
  final taskState = ref.watch(taskNotifierProvider);
  final selectedStatus = ref.watch(selectedStatusProvider);
  final searchQuery = ref.watch(searchQueryProvider).toLowerCase();

  final filteredByStatus = selectedStatus == null
      ? taskState.tasks
      : taskState.tasks
          .where((task) => task.status == selectedStatus)
          .toList();

  if (searchQuery.isEmpty) {
    return filteredByStatus;
  }

  return filteredByStatus.where((task) {
    final title = task.title.toLowerCase();
    final description = task.description.toLowerCase();

    return title.contains(searchQuery) || description.contains(searchQuery);
  }).toList();
});

final emptyMessageProvider = Provider<String>((ref) {
  final selectedStatus = ref.watch(selectedStatusProvider);
  final searchQuery = ref.watch(searchQueryProvider);

  if (searchQuery.isNotEmpty) {
    return 'Task tidak ditemukan';
  }

  if (selectedStatus != null) {
    return 'Belum ada task dengan status ini';
  }

  return 'Belum ada task';
});
```

---

## 22. TaskListPage dengan ConsumerWidget

Gunakan `ConsumerWidget`.

```dart
class TaskListPage extends ConsumerWidget {
  const TaskListPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final taskState = ref.watch(taskNotifierProvider);
    final visibleTasks = ref.watch(visibleTasksProvider);
    final emptyMessage = ref.watch(emptyMessageProvider);

    if (taskState.isLoading) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Task Manager'),
        ),
        body: const Center(
          child: CircularProgressIndicator(),
        ),
      );
    }

    if (taskState.errorMessage != null) {
      return Scaffold(
        appBar: AppBar(
          title: const Text('Task Manager'),
        ),
        body: Center(
          child: Text(taskState.errorMessage!),
        ),
      );
    }

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
  }
}
```

Penjelasan:

- `ref.watch(taskNotifierProvider)` membaca loading/error/tasks.
- `ref.watch(visibleTasksProvider)` membaca hasil filter/search.
- `ref.watch(emptyMessageProvider)` membaca pesan kosong.

---

## 23. Search dengan Riverpod

```dart
TextField(
  decoration: const InputDecoration(
    labelText: 'Cari task',
    prefixIcon: Icon(Icons.search),
    border: OutlineInputBorder(),
  ),
  onChanged: (value) {
    ref.read(searchQueryProvider.notifier).state = value;
  },
)
```

Search hanya mengubah `searchQueryProvider`, bukan data task asli.

---

## 24. Filter dengan Riverpod

```dart
final selectedStatus = ref.watch(selectedStatusProvider);

SingleChildScrollView(
  scrollDirection: Axis.horizontal,
  child: Row(
    children: [
      ChoiceChip(
        label: const Text('Semua'),
        selected: selectedStatus == null,
        onSelected: (_) {
          ref.read(selectedStatusProvider.notifier).state = null;
        },
      ),
      const SizedBox(width: 8),
      ...TaskStatus.values.map((status) {
        return Padding(
          padding: const EdgeInsets.only(right: 8),
          child: ChoiceChip(
            label: Text(status.label),
            selected: selectedStatus == status,
            onSelected: (_) {
              ref.read(selectedStatusProvider.notifier).state = status;
            },
          ),
        );
      }),
    ],
  ),
)
```

Filter juga tidak perlu disimpan ke storage karena hanya memengaruhi tampilan.

---

## 25. List Task dengan Riverpod

```dart
Expanded(
  child: visibleTasks.isEmpty
      ? Center(
          child: Text(emptyMessage),
        )
      : ListView.builder(
          padding: const EdgeInsets.all(16),
          itemCount: visibleTasks.length,
          itemBuilder: (context, index) {
            final task = visibleTasks[index];

            return TaskCard(
              task: task,
              onEdit: () => openEditPage(context, ref, task),
              onDelete: () => confirmDelete(context, ref, task),
              onStatusChanged: (status) {
                ref.read(taskNotifierProvider.notifier).updateStatus(
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

- data list dari `visibleTasksProvider`
- action CRUD dari `taskNotifierProvider.notifier`

---

## 26. Add Task

```dart
Future<void> openCreatePage(BuildContext context, WidgetRef ref) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => const TaskFormPage(),
    ),
  );

  if (result == null) return;

  await ref.read(taskNotifierProvider.notifier).addTask(
        title: result.title,
        description: result.description,
        status: result.status,
      );
}
```

Alur:

```text
Form mengembalikan Task
-> notifier.addTask dipanggil
-> state berubah
-> storage disimpan
-> UI rebuild
```

---

## 27. Edit Task

```dart
Future<void> openEditPage(
  BuildContext context,
  WidgetRef ref,
  Task task,
) async {
  final result = await Navigator.push<Task>(
    context,
    MaterialPageRoute(
      builder: (context) => TaskFormPage(task: task),
    ),
  );

  if (result == null) return;

  await ref.read(taskNotifierProvider.notifier).updateTask(result);
}
```

---

## 28. Delete Task

```dart
Future<void> confirmDelete(
  BuildContext context,
  WidgetRef ref,
  Task task,
) async {
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

  await ref.read(taskNotifierProvider.notifier).deleteTask(task.id);
}
```

---

## 29. Kenapa Riverpod Lebih Rapi

Dengan Riverpod, logic tersebar sesuai tanggung jawab:

```text
TaskNotifier
-> CRUD dan storage

StateProvider
-> filter/search kecil

Provider
-> computed state

UI
-> render dan action
```

Keuntungan:

- UI lebih bersih.
- State tidak tergantung `BuildContext`.
- Computed state lebih mudah dipisah.
- Async/loading/error lebih mudah dikembangkan.
- Provider bisa di-override saat testing.

---

## 30. Testing Manual

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
16. Pastikan data asli tidak hilang.

---

## 31. Kesalahan Umum

### Lupa ProviderScope

Pastikan root app dibungkus:

```dart
const ProviderScope(
  child: MyApp(),
)
```

### Mengubah list lama langsung

Kurang aman:

```dart
state.tasks.add(task);
```

Lebih baik:

```dart
state = state.copyWith(
  tasks: [...state.tasks, task],
);
```

### Menggunakan read untuk data yang harus rebuild

Untuk UI:

```dart
ref.watch(visibleTasksProvider);
```

Untuk action:

```dart
ref.read(taskNotifierProvider.notifier).deleteTask(id);
```

### Save storage lupa dipanggil

Jika data hilang setelah restart, cek apakah action sudah memanggil `_saveCurrentTasks`.

---

## 32. Checklist Riverpod + Storage

Pastikan sudah selesai:

- [ ] Root app memakai `ProviderScope`.
- [ ] Ada `TaskStorageService`.
- [ ] Ada `TaskState`.
- [ ] Ada `TaskNotifier`.
- [ ] Ada `taskNotifierProvider`.
- [ ] Ada `selectedStatusProvider`.
- [ ] Ada `searchQueryProvider`.
- [ ] Ada `visibleTasksProvider`.
- [ ] Ada `emptyMessageProvider`.
- [ ] Task di-load saat notifier dibuat.
- [ ] Storage update saat add.
- [ ] Storage update saat edit.
- [ ] Storage update saat update status.
- [ ] Storage update saat delete.
- [ ] UI memakai `ConsumerWidget`.
- [ ] UI membaca data dengan `ref.watch`.
- [ ] UI memanggil action dengan `ref.read`.
- [ ] Data tetap ada setelah aplikasi ditutup.

Jika checklist ini aman, Task Manager sudah lebih modern dengan Riverpod dan local storage.

---

## 33. Lanjutan Setelah Ini

Langkah berikutnya:

1. Upgrade Task Manager dengan Cubit + Local Storage.
2. Membuat repository layer agar storage lebih rapi.
3. Sinkron data ke Firestore.
4. Tambahkan Firebase Auth.
5. Task per user.

Urutan yang disarankan:

```text
Riverpod + shared_preferences
-> Cubit + shared_preferences
-> Repository pattern
-> Firestore
```
