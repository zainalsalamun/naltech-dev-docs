---
title: "Provider untuk Pemula"
description: "Panduan lengkap belajar Provider di Flutter: ChangeNotifier, ChangeNotifierProvider, Consumer, context.watch, context.read, Selector, MultiProvider, dan contoh Task Manager."
category: "Flutter"
level: "State Management"
order: 37
tags: ["flutter", "provider", "state-management", "changenotifier"]
updated: "2026-05-22"
---

# Provider untuk Pemula

Provider adalah package state management Flutter yang populer dan ramah untuk pemula. Provider membantu kita membagikan state ke banyak widget tanpa harus mengirim data lewat constructor berlapis-lapis.

Di materi sebelumnya, kita sudah belajar:

- state sederhana dengan `setState`
- local state dan shared state
- `ValueNotifier`
- CRUD lokal
- filter dan search

Sekarang kita naik satu tahap: memindahkan logic state ke class khusus menggunakan `ChangeNotifier`, lalu membagikannya ke UI dengan Provider.

---

## 1. Kenapa Perlu Provider

Saat project masih kecil, `setState` cukup.

Contoh:

```dart
setState(() {
  counter++;
});
```

Namun saat aplikasi mulai bertambah fitur, masalah yang sering muncul:

- file page terlalu panjang
- banyak function CRUD menumpuk di satu widget
- data perlu dipakai banyak widget
- harus mengirim data lewat constructor terlalu jauh
- susah tahu bagian mana yang mengubah data

Provider membantu memisahkan:

```text
UI -> menampilkan data dan menerima interaksi
Provider/Notifier -> menyimpan state dan logic perubahan data
Model -> bentuk data
```

Dengan pola ini, widget jadi lebih fokus pada tampilan.

---

## 2. Konsep Utama Provider

Ada beberapa konsep penting:

| Konsep | Fungsi |
| --- | --- |
| `ChangeNotifier` | Class untuk menyimpan state dan memberi tahu UI saat data berubah |
| `notifyListeners()` | Memberi sinyal bahwa UI perlu update |
| `ChangeNotifierProvider` | Menyediakan object `ChangeNotifier` ke widget tree |
| `Consumer` | Membaca provider dan rebuild saat provider berubah |
| `context.watch<T>()` | Membaca provider dan rebuild saat data berubah |
| `context.read<T>()` | Membaca provider tanpa rebuild, cocok untuk tombol/function |
| `Selector` | Membaca sebagian state agar rebuild lebih spesifik |
| `MultiProvider` | Menyediakan banyak provider sekaligus |

Bayangkan Provider seperti pusat data kecil. Widget yang butuh data bisa membaca dari sana. Saat data berubah, widget yang mendengarkan akan ikut update.

---

## 3. Install Provider

Tambahkan package:

```bash
flutter pub add provider
```

Atau tambahkan manual di `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  provider: ^6.1.5
```

Lalu jalankan:

```bash
flutter pub get
```

Import di file Dart:

```dart
import 'package:provider/provider.dart';
```

---

## 4. Contoh Pertama: CounterProvider

Buat file:

```text
lib/providers/counter_provider.dart
```

Isi:

```dart
import 'package:flutter/foundation.dart';

class CounterProvider extends ChangeNotifier {
  int _count = 0;

  int get count => _count;

  void increment() {
    _count++;
    notifyListeners();
  }

  void decrement() {
    if (_count == 0) return;

    _count--;
    notifyListeners();
  }

  void reset() {
    _count = 0;
    notifyListeners();
  }
}
```

Penjelasan:

- `_count` dibuat private supaya tidak diubah langsung dari luar class.
- `get count` dipakai untuk membaca nilai.
- `increment`, `decrement`, dan `reset` adalah function untuk mengubah state.
- `notifyListeners()` wajib dipanggil setelah state berubah.

Jika lupa `notifyListeners()`, data sebenarnya berubah, tapi UI tidak tahu bahwa harus rebuild.

---

## 5. Mendaftarkan Provider di main.dart

Provider harus diletakkan di atas widget yang membutuhkan state.

Contoh:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import 'providers/counter_provider.dart';
import 'pages/counter_page.dart';

void main() {
  runApp(
    ChangeNotifierProvider(
      create: (context) => CounterProvider(),
      child: const MyApp(),
    ),
  );
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: CounterPage(),
    );
  }
}
```

Penjelasan:

- `ChangeNotifierProvider` membuat dan menyediakan `CounterProvider`.
- Semua widget di bawah `MyApp` bisa membaca `CounterProvider`.
- Provider otomatis melakukan dispose saat object tidak lagi dipakai.

---

## 6. Membaca Provider dengan Consumer

Buat file:

```text
lib/pages/counter_page.dart
```

Isi:

```dart
import 'package:flutter/material.dart';
import 'package:provider/provider.dart';

import '../providers/counter_provider.dart';

class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Provider Counter'),
      ),
      body: Center(
        child: Consumer<CounterProvider>(
          builder: (context, provider, child) {
            return Text(
              '${provider.count}',
              style: Theme.of(context).textTheme.displayLarge,
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          context.read<CounterProvider>().increment();
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Penjelasan:

- `Consumer<CounterProvider>` membaca data dan rebuild saat `notifyListeners()` dipanggil.
- `context.read<CounterProvider>().increment()` memanggil function tanpa membuat tombol ikut rebuild.
- `Consumer` cocok jika hanya sebagian kecil UI yang perlu berubah.

---

## 7. context.watch dan context.read

Provider juga bisa dibaca langsung lewat `context`.

### context.watch

```dart
final counter = context.watch<CounterProvider>();
```

Gunakan `watch` jika widget perlu rebuild saat data berubah.

Contoh:

```dart
Text('${context.watch<CounterProvider>().count}')
```

### context.read

```dart
context.read<CounterProvider>().increment();
```

Gunakan `read` jika hanya ingin memanggil function atau membaca data sekali tanpa rebuild.

Contoh:

```dart
ElevatedButton(
  onPressed: () {
    context.read<CounterProvider>().reset();
  },
  child: const Text('Reset'),
)
```

Aturan sederhana:

```text
Butuh UI berubah saat data berubah -> watch atau Consumer
Hanya memanggil action -> read
```

Jangan gunakan `context.read` untuk menampilkan data yang harus update otomatis.

---

## 8. Menambah Tombol Decrement dan Reset

Contoh halaman counter lebih lengkap:

```dart
class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    final count = context.watch<CounterProvider>().count;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Provider Counter'),
      ),
      body: Center(
        child: Text(
          '$count',
          style: Theme.of(context).textTheme.displayLarge,
        ),
      ),
      bottomNavigationBar: Padding(
        padding: const EdgeInsets.all(16),
        child: Row(
          children: [
            Expanded(
              child: OutlinedButton(
                onPressed: () {
                  context.read<CounterProvider>().decrement();
                },
                child: const Text('Kurang'),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: OutlinedButton(
                onPressed: () {
                  context.read<CounterProvider>().reset();
                },
                child: const Text('Reset'),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: FilledButton(
                onPressed: () {
                  context.read<CounterProvider>().increment();
                },
                child: const Text('Tambah'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

Di contoh ini:

- `watch` dipakai untuk nilai `count`.
- `read` dipakai untuk action tombol.

---

## 9. MultiProvider

Jika aplikasi punya lebih dari satu provider, gunakan `MultiProvider`.

Contoh:

```dart
void main() {
  runApp(
    MultiProvider(
      providers: [
        ChangeNotifierProvider(
          create: (context) => CounterProvider(),
        ),
        ChangeNotifierProvider(
          create: (context) => ThemeProvider(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

Keuntungannya:

- struktur `main.dart` lebih rapi
- semua provider terlihat di satu tempat
- mudah menambahkan provider baru

Kapan memakai `MultiProvider`?

- saat aplikasi punya lebih dari satu provider
- saat mulai ada provider untuk auth, theme, task, cart, atau profile

---

## 10. Provider untuk Task Manager

Sekarang kita terapkan konsep Provider ke Task Manager.

Struktur folder:

```text
lib/
  models/
    task.dart
  providers/
    task_provider.dart
  pages/
    task_list_page.dart
    task_form_page.dart
  widgets/
    task_card.dart
```

Model `Task` sama seperti materi CRUD:

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

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.status,
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
    );
  }
}
```

---

## 11. Membuat TaskProvider

Buat file:

```text
lib/providers/task_provider.dart
```

Isi:

```dart
import 'package:flutter/foundation.dart';

import '../models/task.dart';

class TaskProvider extends ChangeNotifier {
  final List<Task> _tasks = [];
  TaskStatus? _selectedStatus;
  String _searchQuery = '';

  List<Task> get tasks => List.unmodifiable(_tasks);
  TaskStatus? get selectedStatus => _selectedStatus;
  String get searchQuery => _searchQuery;

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

  void addTask({
    required String title,
    required String description,
    TaskStatus status = TaskStatus.todo,
  }) {
    final task = Task(
      id: DateTime.now().millisecondsSinceEpoch,
      title: title,
      description: description,
      status: status,
    );

    _tasks.add(task);
    notifyListeners();
  }

  void updateTask(Task updatedTask) {
    final index = _tasks.indexWhere((task) => task.id == updatedTask.id);
    if (index == -1) return;

    _tasks[index] = updatedTask;
    notifyListeners();
  }

  void updateStatus(int id, TaskStatus status) {
    final index = _tasks.indexWhere((task) => task.id == id);
    if (index == -1) return;

    _tasks[index] = _tasks[index].copyWith(status: status);
    notifyListeners();
  }

  void deleteTask(int id) {
    _tasks.removeWhere((task) => task.id == id);
    notifyListeners();
  }

  void setStatusFilter(TaskStatus? status) {
    _selectedStatus = status;
    notifyListeners();
  }

  void setSearchQuery(String value) {
    _searchQuery = value;
    notifyListeners();
  }
}
```

Penjelasan:

- `_tasks` private agar tidak diubah langsung dari UI.
- `tasks` mengembalikan `List.unmodifiable` agar data aman.
- `visibleTasks` berisi hasil akhir setelah filter dan search.
- Semua perubahan data memanggil `notifyListeners()`.
- UI cukup memanggil function seperti `addTask`, `deleteTask`, atau `setSearchQuery`.

---

## 12. Daftarkan TaskProvider

Di `main.dart`:

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
      title: 'Task Manager Provider',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue),
        useMaterial3: true,
      ),
      home: const TaskListPage(),
    );
  }
}
```

Sekarang `TaskProvider` bisa dibaca oleh halaman di bawah `MyApp`.

---

## 13. Membaca TaskProvider di Halaman List

Contoh penggunaan di `TaskListPage`:

```dart
class TaskListPage extends StatelessWidget {
  const TaskListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final provider = context.watch<TaskProvider>();
    final visibleTasks = provider.visibleTasks;

    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Manager'),
      ),
      body: Column(
        children: [
          Padding(
            padding: const EdgeInsets.all(16),
            child: TextField(
              decoration: const InputDecoration(
                labelText: 'Cari task',
                prefixIcon: Icon(Icons.search),
                border: OutlineInputBorder(),
              ),
              onChanged: (value) {
                context.read<TaskProvider>().setSearchQuery(value);
              },
            ),
          ),
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

                      return ListTile(
                        title: Text(task.title),
                        subtitle: Text(task.description),
                        trailing: IconButton(
                          icon: const Icon(Icons.delete_outline),
                          onPressed: () {
                            context.read<TaskProvider>().deleteTask(task.id);
                          },
                        ),
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

Penjelasan:

- `context.watch<TaskProvider>()` membuat halaman rebuild saat task/filter/search berubah.
- `context.read<TaskProvider>()` dipakai pada action seperti search dan delete.
- Logic list tidak lagi ditulis langsung di widget, tapi dipindahkan ke `TaskProvider`.

---

## 14. Filter Status dengan Provider

Tambahkan widget filter:

```dart
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

Penjelasan:

- `selectedStatus` dibaca dari provider.
- Saat chip ditekan, provider mengubah filter.
- Setelah `notifyListeners()`, UI otomatis rebuild.

---

## 15. Selector untuk Rebuild Lebih Hemat

Kadang widget hanya butuh satu bagian kecil dari provider. Gunakan `Selector`.

Contoh menampilkan jumlah task:

```dart
Selector<TaskProvider, int>(
  selector: (context, provider) => provider.tasks.length,
  builder: (context, totalTask, child) {
    return Text('Total task: $totalTask');
  },
)
```

Penjelasan:

- Widget hanya peduli pada `tasks.length`.
- Jika bagian provider lain berubah tapi `tasks.length` tetap, rebuild bisa lebih hemat.

Gunakan `Selector` saat:

- provider punya banyak state
- widget hanya butuh sebagian kecil data
- ingin menghindari rebuild yang tidak perlu

Untuk pemula, tidak wajib langsung memakai `Selector`. Pahami `Consumer`, `watch`, dan `read` dulu.

---

## 16. Kesalahan Umum Provider

### Lupa notifyListeners

```dart
void increment() {
  _count++;
}
```

Data berubah, tapi UI tidak update.

Solusi:

```dart
void increment() {
  _count++;
  notifyListeners();
}
```

### Provider diletakkan terlalu bawah

Jika widget membaca provider tapi tidak berada di bawah `ChangeNotifierProvider`, akan muncul error provider tidak ditemukan.

Solusi:

- letakkan provider di atas widget yang membutuhkan
- biasanya di `main.dart` atau di atas halaman tertentu

### Memakai watch untuk tombol action

Kurang ideal:

```dart
onPressed: () {
  context.watch<TaskProvider>().deleteTask(id);
}
```

Gunakan:

```dart
onPressed: () {
  context.read<TaskProvider>().deleteTask(id);
}
```

### Logic masih terlalu banyak di UI

Jika semua logic tetap ditulis di halaman, Provider tidak banyak membantu.

Lebih baik:

```dart
context.read<TaskProvider>().addTask(
  title: title,
  description: description,
);
```

Daripada UI mengurus langsung cara data disimpan.

---

## 17. Kapan Provider Cocok Dipakai

Provider cocok untuk:

- aplikasi kecil sampai menengah
- belajar state management pertama
- CRUD lokal
- theme mode
- cart sederhana
- auth state sederhana
- form dan filter sederhana

Provider mulai terasa kurang nyaman jika:

- async state sangat banyak
- dependency antar provider makin kompleks
- butuh state yang lebih mudah dites secara modular
- project besar dengan banyak flow

Jika mulai terasa seperti itu, lanjut belajar Riverpod atau Bloc/Cubit.

---

## 18. Checklist Provider

Pastikan sudah paham:

- [ ] Provider membantu membagikan state ke widget tree.
- [ ] `ChangeNotifier` menyimpan state dan logic.
- [ ] `notifyListeners()` membuat UI yang mendengarkan ikut update.
- [ ] `ChangeNotifierProvider` menyediakan notifier.
- [ ] `Consumer` membaca provider dan rebuild saat data berubah.
- [ ] `context.watch` dipakai saat UI perlu rebuild.
- [ ] `context.read` dipakai untuk action.
- [ ] `MultiProvider` dipakai untuk banyak provider.
- [ ] `Selector` dipakai untuk rebuild yang lebih spesifik.
- [ ] Logic CRUD bisa dipindahkan dari page ke provider.

Jika checklist ini sudah aman, lanjutkan ke **Riverpod untuk Pemula** atau upgrade Project Task Manager memakai Provider.

---

## Referensi Resmi

- [Simple app state management - Flutter docs](https://docs.flutter.dev/data-and-backend/state-mgmt/simple)
- [provider package - pub.dev](https://pub.dev/packages/provider)
- [provider example - pub.dev](https://pub.dev/packages/provider/example)
