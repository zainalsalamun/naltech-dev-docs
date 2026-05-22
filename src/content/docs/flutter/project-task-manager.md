---
title: "Project 2: Task Manager"
description: "Project Flutter step-by-step untuk membuat aplikasi task manager dengan CRUD lokal, filter status, search, edit task, dan konfirmasi hapus."
category: "Flutter"
level: "Project"
order: 50
tags: ["flutter", "project", "task-manager", "crud", "state"]
updated: "2026-05-21"
---

# Project 2: Task Manager

Project ini adalah lanjutan setelah **Project 1: Aplikasi Catatan Belajar**. Jika project pertama fokus pada tambah, tampilkan, dan hapus data sederhana, maka project ini naik satu level dengan fitur edit, status task, filter, search, dan konfirmasi hapus.

Target project:

- Membuat data task dengan model yang rapi.
- Menambah task baru.
- Mengedit task.
- Menghapus task dengan konfirmasi.
- Mengubah status task.
- Filter task berdasarkan status.
- Search task berdasarkan title dan description.
- Menampilkan empty state sesuai kondisi.

---

## 1. Gambaran Aplikasi

Alur aplikasi:

```text
Task List Page
-> user melihat semua task
-> user bisa search task
-> user bisa filter berdasarkan status
-> user bisa tambah task
-> user bisa edit task
-> user bisa ubah status task
-> user bisa hapus task
```

Status task:

- `todo`: task belum dikerjakan
- `progress`: task sedang dikerjakan
- `done`: task selesai

Skill yang dilatih:

- `StatefulWidget`
- `setState`
- `enum`
- `copyWith`
- `ListView.builder`
- `ChoiceChip`
- `TextEditingController`
- `Navigator.push`
- `showDialog`

---

## 2. Struktur Folder

Buat struktur folder seperti ini:

```text
lib/
  main.dart
  models/
    task.dart
  pages/
    task_list_page.dart
    task_form_page.dart
  widgets/
    task_card.dart
    task_status_chip.dart
```

Penjelasan:

- `models/`: menyimpan bentuk data.
- `pages/`: menyimpan halaman aplikasi.
- `widgets/`: menyimpan komponen UI kecil.

Struktur ini belum terlalu rumit, tapi sudah cukup rapi untuk project pemula-menengah.

---

## 3. Membuat Model Task

Buat file `lib/models/task.dart`.

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
}
```

Penjelasan:

- `TaskStatus` membatasi pilihan status task.
- `extension TaskStatusLabel` membuat label status lebih enak dibaca.
- `Task` adalah model utama aplikasi.
- `copyWith` dipakai saat mengedit data tanpa mengubah object lama secara langsung.

Kenapa pakai `copyWith`?

Karena property `Task` dibuat `final`. Artinya, object lebih aman dan tidak berubah sembarangan. Jika ada perubahan, kita membuat object baru dari object lama.

---

## 4. Setup main.dart

Isi `lib/main.dart`.

```dart
import 'package:flutter/material.dart';

import 'pages/task_list_page.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Task Manager',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(
          seedColor: Colors.blue,
        ),
        useMaterial3: true,
      ),
      home: const TaskListPage(),
    );
  }
}
```

Penjelasan:

- `TaskListPage` menjadi halaman utama.
- `ThemeData` memakai Material 3.
- `debugShowCheckedModeBanner` dimatikan agar tampilan lebih bersih.

---

## 5. Membuat TaskStatusChip

Buat file `lib/widgets/task_status_chip.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/task.dart';

class TaskStatusChip extends StatelessWidget {
  final TaskStatus status;

  const TaskStatusChip({
    super.key,
    required this.status,
  });

  Color get color {
    switch (status) {
      case TaskStatus.todo:
        return Colors.orange;
      case TaskStatus.progress:
        return Colors.blue;
      case TaskStatus.done:
        return Colors.green;
    }
  }

  @override
  Widget build(BuildContext context) {
    return Chip(
      label: Text(status.label),
      side: BorderSide(color: color),
      labelStyle: TextStyle(color: color),
    );
  }
}
```

Penjelasan:

- Widget ini hanya bertanggung jawab menampilkan status.
- Warna chip berbeda sesuai status.
- Dengan dipisah, `TaskCard` nanti lebih bersih.

---

## 6. Membuat TaskCard

Buat file `lib/widgets/task_card.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/task.dart';
import 'task_status_chip.dart';

class TaskCard extends StatelessWidget {
  final Task task;
  final VoidCallback onEdit;
  final VoidCallback onDelete;
  final ValueChanged<TaskStatus> onStatusChanged;

  const TaskCard({
    super.key,
    required this.task,
    required this.onEdit,
    required this.onDelete,
    required this.onStatusChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.only(bottom: 12),
      child: Padding(
        padding: const EdgeInsets.all(12),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Expanded(
                  child: Text(
                    task.title,
                    style: Theme.of(context).textTheme.titleMedium,
                  ),
                ),
                PopupMenuButton<String>(
                  onSelected: (value) {
                    if (value == 'edit') onEdit();
                    if (value == 'delete') onDelete();
                  },
                  itemBuilder: (context) {
                    return const [
                      PopupMenuItem(
                        value: 'edit',
                        child: Text('Edit'),
                      ),
                      PopupMenuItem(
                        value: 'delete',
                        child: Text('Hapus'),
                      ),
                    ];
                  },
                ),
              ],
            ),
            const SizedBox(height: 6),
            Text(task.description),
            const SizedBox(height: 12),
            Row(
              children: [
                TaskStatusChip(status: task.status),
                const Spacer(),
                DropdownButton<TaskStatus>(
                  value: task.status,
                  underline: const SizedBox(),
                  onChanged: (value) {
                    if (value == null) return;
                    onStatusChanged(value);
                  },
                  items: TaskStatus.values.map((status) {
                    return DropdownMenuItem(
                      value: status,
                      child: Text(status.label),
                    );
                  }).toList(),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
```

Penjelasan:

- `onEdit` dipanggil saat user memilih menu edit.
- `onDelete` dipanggil saat user memilih menu hapus.
- `onStatusChanged` dipanggil saat status task diubah.
- `DropdownButton` memakai data dari `TaskStatus.values`.

---

## 7. Membuat Halaman Form Task

Buat file `lib/pages/task_form_page.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/task.dart';

class TaskFormPage extends StatefulWidget {
  final Task? task;

  const TaskFormPage({
    super.key,
    this.task,
  });

  @override
  State<TaskFormPage> createState() => _TaskFormPageState();
}

class _TaskFormPageState extends State<TaskFormPage> {
  final titleController = TextEditingController();
  final descriptionController = TextEditingController();
  TaskStatus selectedStatus = TaskStatus.todo;

  bool get isEditMode => widget.task != null;

  @override
  void initState() {
    super.initState();

    final task = widget.task;
    if (task != null) {
      titleController.text = task.title;
      descriptionController.text = task.description;
      selectedStatus = task.status;
    }
  }

  @override
  void dispose() {
    titleController.dispose();
    descriptionController.dispose();
    super.dispose();
  }

  void saveTask() {
    final title = titleController.text.trim();
    final description = descriptionController.text.trim();

    if (title.isEmpty || description.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Judul dan deskripsi wajib diisi'),
        ),
      );
      return;
    }

    final oldTask = widget.task;

    final task = oldTask == null
        ? Task(
            id: DateTime.now().millisecondsSinceEpoch,
            title: title,
            description: description,
            status: selectedStatus,
            createdAt: DateTime.now(),
          )
        : oldTask.copyWith(
            title: title,
            description: description,
            status: selectedStatus,
          );

    Navigator.pop(context, task);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text(isEditMode ? 'Edit Task' : 'Tambah Task'),
      ),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          TextField(
            controller: titleController,
            decoration: const InputDecoration(
              labelText: 'Judul',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          TextField(
            controller: descriptionController,
            maxLines: 4,
            decoration: const InputDecoration(
              labelText: 'Deskripsi',
              border: OutlineInputBorder(),
            ),
          ),
          const SizedBox(height: 12),
          DropdownButtonFormField<TaskStatus>(
            value: selectedStatus,
            decoration: const InputDecoration(
              labelText: 'Status',
              border: OutlineInputBorder(),
            ),
            items: TaskStatus.values.map((status) {
              return DropdownMenuItem(
                value: status,
                child: Text(status.label),
              );
            }).toList(),
            onChanged: (value) {
              if (value == null) return;
              setState(() {
                selectedStatus = value;
              });
            },
          ),
          const SizedBox(height: 16),
          FilledButton(
            onPressed: saveTask,
            child: Text(isEditMode ? 'Simpan Perubahan' : 'Tambah Task'),
          ),
        ],
      ),
    );
  }
}
```

Penjelasan:

- Jika `task == null`, form dipakai untuk tambah data.
- Jika `task != null`, form dipakai untuk edit data.
- `initState()` mengisi form saat mode edit.
- `Navigator.pop(context, task)` mengirim hasil ke halaman list.

---

## 8. Membuat Halaman List Task

Buat file `lib/pages/task_list_page.dart`.

```dart
import 'package:flutter/material.dart';

import '../models/task.dart';
import '../widgets/task_card.dart';
import 'task_form_page.dart';

class TaskListPage extends StatefulWidget {
  const TaskListPage({super.key});

  @override
  State<TaskListPage> createState() => _TaskListPageState();
}

class _TaskListPageState extends State<TaskListPage> {
  final List<Task> tasks = [];
  TaskStatus? selectedStatus;
  String searchQuery = '';

  List<Task> get filteredTasks {
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
  }

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
  }

  void updateTaskStatus(int id, TaskStatus status) {
    final index = tasks.indexWhere((task) => task.id == id);
    if (index == -1) return;

    setState(() {
      tasks[index] = tasks[index].copyWith(status: status);
    });
  }

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
  }

  @override
  Widget build(BuildContext context) {
    final visibleTasks = filteredTasks;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Manager'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: Column(
              children: [
                TextField(
                  decoration: const InputDecoration(
                    labelText: 'Cari task',
                    prefixIcon: Icon(Icons.search),
                    border: OutlineInputBorder(),
                  ),
                  onChanged: (value) {
                    setState(() {
                      searchQuery = value;
                    });
                  },
                ),
                const SizedBox(height: 12),
                SingleChildScrollView(
                  scrollDirection: Axis.horizontal,
                  child: Row(
                    children: [
                      ChoiceChip(
                        label: const Text('Semua'),
                        selected: selectedStatus == null,
                        onSelected: (_) {
                          setState(() {
                            selectedStatus = null;
                          });
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
                              setState(() {
                                selectedStatus = status;
                              });
                            },
                          ),
                        );
                      }),
                    ],
                  ),
                ),
              ],
            ),
          ),
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
                        onEdit: () => openEditPage(task),
                        onDelete: () => confirmDelete(task),
                        onStatusChanged: (status) {
                          updateTaskStatus(task.id, status);
                        },
                      );
                    },
                  ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: openCreatePage,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Penjelasan penting:

- `tasks` adalah sumber data utama.
- `selectedStatus` menyimpan filter status.
- `searchQuery` menyimpan keyword pencarian.
- `filteredTasks` menggabungkan filter dan search.
- `openCreatePage()` membuka form tambah.
- `openEditPage()` membuka form edit.
- `updateTaskStatus()` mengubah status task.
- `confirmDelete()` meminta konfirmasi sebelum hapus.

---

## 9. Memahami Alur Create dan Edit

Tambah task:

```text
User tekan tombol +
-> TaskFormPage terbuka tanpa data task
-> user mengisi form
-> form membuat Task baru
-> Navigator.pop mengirim Task
-> TaskListPage menambahkan Task ke List
```

Edit task:

```text
User pilih Edit
-> TaskFormPage terbuka membawa data task
-> initState mengisi form
-> user mengubah data
-> form membuat Task hasil copyWith
-> Navigator.pop mengirim Task baru
-> TaskListPage mengganti data lama berdasarkan id
```

Perbedaan tambah dan edit ada di data awal:

- tambah: `task == null`
- edit: `task != null`

---

## 10. Memahami Filter dan Search

Filter status:

```dart
selectedStatus == null
```

Artinya semua task ditampilkan.

Jika:

```dart
selectedStatus == TaskStatus.done
```

Artinya hanya task dengan status done yang ditampilkan.

Search:

```dart
title.contains(query) || description.contains(query)
```

Artinya task akan tampil jika keyword ditemukan di title atau description.

Urutan yang dipakai:

```text
tasks
-> filter status
-> search keyword
-> visibleTasks
-> ListView
```

Dengan urutan ini, search hanya mencari dari task yang sudah sesuai filter.

---

## 11. Challenge Pengembangan

Setelah project dasar selesai, lanjutkan challenge berikut:

1. Tampilkan jumlah task per status.
2. Tambahkan tanggal dibuat di card.
3. Tambahkan prioritas task: low, medium, high.
4. Tambahkan sorting terbaru dan terlama.
5. Tambahkan halaman detail task.
6. Tambahkan validasi minimal judul 3 karakter.
7. Simpan task ke local storage.

Urutan challenge yang disarankan:

```text
jumlah task per status
-> tanggal dibuat
-> prioritas
-> sorting
-> detail page
-> local storage
```

---

## 12. Checklist Selesai Project

Project ini dianggap selesai jika kamu sudah bisa:

- [ ] Membuat model `Task`.
- [ ] Membuat `enum TaskStatus`.
- [ ] Membuat extension label status.
- [ ] Membuat `copyWith`.
- [ ] Menambah task baru.
- [ ] Mengedit task.
- [ ] Menghapus task dengan konfirmasi.
- [ ] Mengubah status task.
- [ ] Filter task berdasarkan status.
- [ ] Search task berdasarkan keyword.
- [ ] Menampilkan empty state.
- [ ] Memisahkan file model, page, dan widget.

Jika checklist ini sudah aman, materi berikutnya yang paling cocok adalah **Local Storage** agar task tidak hilang saat aplikasi ditutup.
