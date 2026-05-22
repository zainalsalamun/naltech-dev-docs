---
title: "Riverpod untuk Pemula"
description: "Panduan belajar Riverpod di Flutter: ProviderScope, ConsumerWidget, WidgetRef, StateProvider, NotifierProvider, FutureProvider, AsyncValue, dan contoh Task Manager."
category: "Flutter"
level: "State Management"
order: 38
tags: ["flutter", "riverpod", "state-management", "asyncvalue"]
updated: "2026-05-22"
---

# Riverpod untuk Pemula

Riverpod adalah state management modern untuk Flutter/Dart. Secara konsep, Riverpod mirip dengan Provider karena sama-sama membantu membagikan state ke widget. Bedanya, Riverpod tidak bergantung langsung pada `BuildContext`, lebih mudah dites, dan punya dukungan yang rapi untuk state async seperti loading, data, dan error.

Materi ini cocok dibaca setelah:

- `setState`
- `ValueNotifier`
- Provider
- CRUD lokal
- Task Manager sederhana

Target materi:

- Memahami kenapa Riverpod dipakai.
- Memasang `flutter_riverpod`.
- Memahami `ProviderScope`.
- Membaca provider dengan `ref.watch`.
- Memanggil action dengan `ref.read`.
- Membuat state sederhana dengan `StateProvider`.
- Membuat logic state dengan `NotifierProvider`.
- Membaca data async dengan `FutureProvider`.
- Memahami `AsyncValue`.

---

## 1. Kenapa Belajar Riverpod

Provider bagus untuk belajar state management pertama. Namun saat project semakin besar, biasanya muncul kebutuhan seperti:

- state lebih mudah dites
- tidak bergantung pada `BuildContext`
- async state lebih rapi
- dependency antar state lebih jelas
- logic aplikasi bisa dipisahkan lebih bersih

Riverpod membantu kebutuhan itu.

Perbandingan sederhana:

| Provider | Riverpod |
| --- | --- |
| Membaca state lewat `context` | Membaca state lewat `ref` |
| Butuh `BuildContext` | Tidak bergantung pada `BuildContext` |
| Umum memakai `ChangeNotifier` | Bisa memakai `StateProvider`, `NotifierProvider`, `FutureProvider`, dan lainnya |
| Async state sering dibuat manual | Async state didukung lewat `AsyncValue` |

Riverpod bukan wajib untuk semua aplikasi. Tapi jika ingin naik level dari Provider, Riverpod adalah pilihan yang bagus.

---

## 2. Install Riverpod

Tambahkan package:

```bash
flutter pub add flutter_riverpod
```

Lalu jalankan:

```bash
flutter pub get
```

Import:

```dart
import 'package:flutter_riverpod/flutter_riverpod.dart';
```

---

## 3. ProviderScope

Riverpod membutuhkan `ProviderScope` di root aplikasi.

Contoh `main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'pages/home_page.dart';

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
    return const MaterialApp(
      debugShowCheckedModeBanner: false,
      home: HomePage(),
    );
  }
}
```

Penjelasan:

- `ProviderScope` menyimpan container Riverpod.
- Semua provider hidup di dalam scope ini.
- Biasanya `ProviderScope` diletakkan paling atas di `runApp`.

Jika lupa menambahkan `ProviderScope`, provider tidak bisa dibaca oleh widget.

---

## 4. ConsumerWidget dan WidgetRef

Di Riverpod, widget yang membaca provider biasanya memakai `ConsumerWidget`.

Contoh:

```dart
class HomePage extends ConsumerWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    return const Scaffold(
      body: Center(
        child: Text('Hello Riverpod'),
      ),
    );
  }
}
```

Perhatikan perbedaannya:

```dart
Widget build(BuildContext context, WidgetRef ref)
```

`ref` dipakai untuk:

- membaca provider
- memanggil notifier
- mendengarkan perubahan state

Aturan sederhana:

```text
ref.watch -> membaca state dan rebuild saat berubah
ref.read -> membaca sekali atau memanggil action
```

---

## 5. StateProvider untuk State Sederhana

`StateProvider` cocok untuk state sederhana seperti:

- counter
- selected tab
- selected filter
- toggle dark mode sederhana
- search query

Contoh counter:

```dart
final counterProvider = StateProvider<int>((ref) {
  return 0;
});
```

Membaca state:

```dart
final counter = ref.watch(counterProvider);
```

Mengubah state:

```dart
ref.read(counterProvider.notifier).state++;
```

Contoh halaman lengkap:

```dart
final counterProvider = StateProvider<int>((ref) => 0);

class CounterPage extends ConsumerWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final counter = ref.watch(counterProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('Riverpod Counter'),
      ),
      body: Center(
        child: Text(
          '$counter',
          style: Theme.of(context).textTheme.displayLarge,
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          ref.read(counterProvider.notifier).state++;
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Penjelasan:

- `ref.watch(counterProvider)` membuat UI rebuild saat counter berubah.
- `ref.read(counterProvider.notifier).state++` mengubah nilai counter.

Gunakan `StateProvider` untuk state kecil. Jika logic mulai banyak, pindah ke `NotifierProvider`.

---

## 6. StateProvider untuk Filter

Contoh filter task:

```dart
enum TaskStatus {
  todo,
  progress,
  done,
}

final selectedStatusProvider = StateProvider<TaskStatus?>((ref) {
  return null;
});
```

Membaca filter:

```dart
final selectedStatus = ref.watch(selectedStatusProvider);
```

Mengubah filter:

```dart
ref.read(selectedStatusProvider.notifier).state = TaskStatus.done;
```

Menghapus filter:

```dart
ref.read(selectedStatusProvider.notifier).state = null;
```

Contoh UI:

```dart
ChoiceChip(
  label: const Text('Semua'),
  selected: selectedStatus == null,
  onSelected: (_) {
    ref.read(selectedStatusProvider.notifier).state = null;
  },
)
```

Ini cocok karena selected filter adalah state sederhana.

---

## 7. Provider untuk Computed State

Riverpod punya `Provider` untuk data turunan atau computed state.

Misalnya ada list task dan filter status.

```dart
final tasksProvider = StateProvider<List<Task>>((ref) {
  return [];
});

final selectedStatusProvider = StateProvider<TaskStatus?>((ref) {
  return null;
});

final filteredTasksProvider = Provider<List<Task>>((ref) {
  final tasks = ref.watch(tasksProvider);
  final selectedStatus = ref.watch(selectedStatusProvider);

  if (selectedStatus == null) {
    return tasks;
  }

  return tasks.where((task) => task.status == selectedStatus).toList();
});
```

Penjelasan:

- `tasksProvider` menyimpan data utama.
- `selectedStatusProvider` menyimpan filter.
- `filteredTasksProvider` menghitung hasil akhir.

Kelebihan pola ini:

- logic filter tidak ditulis di widget
- widget cukup membaca `filteredTasksProvider`
- jika task atau filter berubah, hasil ikut update

---

## 8. NotifierProvider untuk Logic Lebih Rapi

Jika state punya banyak action, gunakan `NotifierProvider`.

Contoh:

```dart
class CounterNotifier extends Notifier<int> {
  @override
  int build() {
    return 0;
  }

  void increment() {
    state++;
  }

  void decrement() {
    if (state == 0) return;
    state--;
  }

  void reset() {
    state = 0;
  }
}

final counterNotifierProvider =
    NotifierProvider<CounterNotifier, int>(CounterNotifier.new);
```

Membaca state:

```dart
final counter = ref.watch(counterNotifierProvider);
```

Memanggil action:

```dart
ref.read(counterNotifierProvider.notifier).increment();
```

Contoh UI:

```dart
class CounterPage extends ConsumerWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final counter = ref.watch(counterNotifierProvider);

    return Scaffold(
      appBar: AppBar(
        title: const Text('NotifierProvider Counter'),
      ),
      body: Center(
        child: Text('$counter'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          ref.read(counterNotifierProvider.notifier).increment();
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Kapan memakai `NotifierProvider`?

- saat state punya banyak function
- saat logic tidak cocok ditaruh di widget
- saat ingin state lebih mudah dites
- saat membuat fitur seperti task manager, cart, atau auth sederhana

---

## 9. Task Manager dengan NotifierProvider

Model:

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

Notifier:

```dart
class TaskNotifier extends Notifier<List<Task>> {
  @override
  List<Task> build() {
    return [];
  }

  void addTask({
    required String title,
    required String description,
  }) {
    final task = Task(
      id: DateTime.now().millisecondsSinceEpoch,
      title: title,
      description: description,
      status: TaskStatus.todo,
    );

    state = [...state, task];
  }

  void updateTask(Task updatedTask) {
    state = [
      for (final task in state)
        if (task.id == updatedTask.id) updatedTask else task,
    ];
  }

  void updateStatus(int id, TaskStatus status) {
    state = [
      for (final task in state)
        if (task.id == id) task.copyWith(status: status) else task,
    ];
  }

  void deleteTask(int id) {
    state = state.where((task) => task.id != id).toList();
  }
}

final taskNotifierProvider =
    NotifierProvider<TaskNotifier, List<Task>>(TaskNotifier.new);
```

Penjelasan:

- `state` adalah list task saat ini.
- Saat menambah data, kita membuat list baru dengan `state = [...state, task]`.
- Saat update, kita membuat list baru menggunakan `for`.
- Saat delete, kita membuat list baru dengan `.where()`.

Riverpod lebih cocok dengan pola immutable seperti ini.

---

## 10. Filter dan Search dengan Riverpod

Provider filter:

```dart
final selectedStatusProvider = StateProvider<TaskStatus?>((ref) => null);
final searchQueryProvider = StateProvider<String>((ref) => '');
```

Provider hasil akhir:

```dart
final visibleTasksProvider = Provider<List<Task>>((ref) {
  final tasks = ref.watch(taskNotifierProvider);
  final selectedStatus = ref.watch(selectedStatusProvider);
  final searchQuery = ref.watch(searchQueryProvider).toLowerCase();

  final filteredByStatus = selectedStatus == null
      ? tasks
      : tasks.where((task) => task.status == selectedStatus).toList();

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

Widget cukup membaca:

```dart
final visibleTasks = ref.watch(visibleTasksProvider);
```

Keuntungannya:

- UI tidak perlu tahu cara filter dan search dihitung.
- Jika task, filter, atau search berubah, `visibleTasksProvider` otomatis menghitung ulang.

---

## 11. FutureProvider untuk Data Async

`FutureProvider` cocok untuk data async seperti:

- request API
- membaca file
- mengambil data remote
- membaca data awal dari storage

Contoh:

```dart
final postsProvider = FutureProvider<List<String>>((ref) async {
  await Future.delayed(const Duration(seconds: 1));

  return [
    'Belajar Flutter',
    'Belajar Riverpod',
    'Belajar Firebase',
  ];
});
```

Membaca di UI:

```dart
class PostsPage extends ConsumerWidget {
  const PostsPage({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final postsAsync = ref.watch(postsProvider);

    return postsAsync.when(
      loading: () {
        return const Center(
          child: CircularProgressIndicator(),
        );
      },
      error: (error, stackTrace) {
        return Center(
          child: Text('Error: $error'),
        );
      },
      data: (posts) {
        return ListView.builder(
          itemCount: posts.length,
          itemBuilder: (context, index) {
            return ListTile(
              title: Text(posts[index]),
            );
          },
        );
      },
    );
  }
}
```

Penjelasan:

- `postsAsync` bertipe `AsyncValue<List<String>>`.
- `.when()` memisahkan UI loading, error, dan data.

Ini membuat async state lebih rapi daripada membuat banyak variable manual seperti `isLoading`, `errorMessage`, dan `data`.

---

## 12. Memahami AsyncValue

`AsyncValue` merepresentasikan tiga kondisi:

```text
loading
error
data
```

Contoh:

```dart
final userAsync = ref.watch(userProvider);
```

Lalu:

```dart
userAsync.when(
  loading: () => const CircularProgressIndicator(),
  error: (error, stackTrace) => Text('Error: $error'),
  data: (user) => Text(user.name),
)
```

Kelebihan `AsyncValue`:

- UI loading lebih jelas.
- Error lebih mudah ditangani.
- Data sukses punya jalur sendiri.
- Cocok untuk API dan Firebase.

Nanti saat belajar Firebase atau API CRUD, `AsyncValue` akan sangat berguna.

---

## 13. ref.watch vs ref.read

Aturan sederhana:

```text
ref.watch -> untuk UI yang harus rebuild saat state berubah
ref.read -> untuk action seperti tombol, submit form, delete data
```

Contoh `watch`:

```dart
final tasks = ref.watch(visibleTasksProvider);
```

Contoh `read`:

```dart
ref.read(taskNotifierProvider.notifier).deleteTask(task.id);
```

Kesalahan umum:

```dart
final notifier = ref.watch(taskNotifierProvider.notifier);
```

Untuk memanggil function, gunakan `read`:

```dart
final notifier = ref.read(taskNotifierProvider.notifier);
```

---

## 14. ConsumerStatefulWidget

Jika butuh lifecycle seperti `initState`, gunakan `ConsumerStatefulWidget`.

Contoh:

```dart
class SearchPage extends ConsumerStatefulWidget {
  const SearchPage({super.key});

  @override
  ConsumerState<SearchPage> createState() => _SearchPageState();
}

class _SearchPageState extends ConsumerState<SearchPage> {
  final controller = TextEditingController();

  @override
  void dispose() {
    controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final query = ref.watch(searchQueryProvider);

    return TextField(
      controller: controller,
      decoration: InputDecoration(
        labelText: 'Cari: $query',
      ),
      onChanged: (value) {
        ref.read(searchQueryProvider.notifier).state = value;
      },
    );
  }
}
```

Gunakan `ConsumerStatefulWidget` saat:

- butuh `TextEditingController`
- butuh `initState`
- butuh `dispose`
- butuh animation controller

Jika tidak butuh lifecycle, gunakan `ConsumerWidget`.

---

## 15. Kesalahan Umum Riverpod

### Lupa ProviderScope

Jika tidak ada `ProviderScope`, provider tidak bisa dipakai.

Solusi:

```dart
void main() {
  runApp(
    const ProviderScope(
      child: MyApp(),
    ),
  );
}
```

### Memakai read untuk UI yang harus update

Kurang tepat:

```dart
final count = ref.read(counterProvider);
```

Jika UI harus update, gunakan:

```dart
final count = ref.watch(counterProvider);
```

### Logic terlalu banyak di widget

Jika widget masih menyimpan semua logic, manfaat Riverpod jadi kecil.

Lebih baik:

```dart
ref.read(taskNotifierProvider.notifier).addTask(
  title: title,
  description: description,
);
```

### State mutable langsung diubah

Kurang aman:

```dart
state.add(task);
```

Lebih baik:

```dart
state = [...state, task];
```

Tujuannya agar Riverpod tahu state berubah dan UI bisa update dengan benar.

---

## 16. Kapan Memakai Riverpod

Riverpod cocok untuk:

- aplikasi menengah sampai besar
- state yang dipakai banyak halaman
- API dan Firebase
- auth state
- cart, task, profile, dan settings
- project yang butuh testing lebih rapi

Untuk pemula:

```text
setState -> Provider -> Riverpod
```

Jangan terburu-buru memakai semua fitur Riverpod. Mulai dari:

1. `ProviderScope`
2. `ConsumerWidget`
3. `StateProvider`
4. `NotifierProvider`
5. `FutureProvider`
6. `AsyncValue`

---

## 17. Checklist Riverpod

Pastikan sudah paham:

- [ ] Riverpod membaca state dengan `ref`, bukan `context`.
- [ ] `ProviderScope` wajib dipasang di root aplikasi.
- [ ] `ConsumerWidget` dipakai untuk membaca provider.
- [ ] `ref.watch` dipakai agar UI rebuild.
- [ ] `ref.read` dipakai untuk action.
- [ ] `StateProvider` cocok untuk state sederhana.
- [ ] `Provider` cocok untuk computed state.
- [ ] `NotifierProvider` cocok untuk state dengan banyak logic.
- [ ] `FutureProvider` cocok untuk data async.
- [ ] `AsyncValue` memisahkan loading, error, dan data.
- [ ] State list sebaiknya diubah dengan membuat list baru.

Jika checklist ini sudah aman, lanjutkan ke **Upgrade Project Task Manager dengan Riverpod** atau masuk ke **Cubit/Bloc Dasar**.

---

## Referensi Resmi

- [Riverpod providers concept](https://docs-v2.riverpod.dev/docs/concepts/providers)
- [Riverpod StateProvider](https://docs-v2.riverpod.dev/docs/providers/state_provider)
- [Riverpod NotifierProvider](https://riverpod.dev/docs/providers/notifier_provider)
- [flutter_riverpod package API](https://pub.dev/documentation/flutter_riverpod/latest/flutter_riverpod/)
- [FutureProvider API](https://pub.dev/documentation/flutter_riverpod/latest/flutter_riverpod/FutureProvider-class.html)
