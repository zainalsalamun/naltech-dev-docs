---
title: "Cubit dan Bloc Dasar"
description: "Panduan belajar Cubit dan Bloc di Flutter: konsep event-state, Cubit, BlocProvider, BlocBuilder, BlocListener, BlocConsumer, MultiBlocProvider, dan contoh Task Manager."
category: "Flutter"
level: "State Management"
order: 39
tags: ["flutter", "bloc", "cubit", "state-management"]
updated: "2026-05-22"
---

# Cubit dan Bloc Dasar

Cubit dan Bloc adalah pola state management yang sering dipakai di aplikasi Flutter yang lebih besar, terutama ketika aplikasi punya flow yang jelas, banyak state, dan butuh pemisahan logic yang rapi.

Jika Provider dan Riverpod terasa seperti "state container", maka Cubit/Bloc lebih terasa seperti "mesin perubahan state". Kita membuat state, lalu UI bereaksi terhadap state tersebut.

Materi ini cocok dibaca setelah:

- `setState`
- Provider
- Riverpod
- CRUD lokal
- Task Manager

Target materi:

- Memahami perbedaan Cubit dan Bloc.
- Memahami state.
- Membuat Cubit sederhana.
- Membaca Cubit dengan `BlocBuilder`.
- Menjalankan side effect dengan `BlocListener`.
- Memakai `BlocConsumer`.
- Memakai `MultiBlocProvider`.
- Membuat contoh Task Manager dengan Cubit.
- Mengenal Bloc dengan event-state.

Cara belajar materi ini:

```text
Pahami state dulu
-> belajar Cubit
-> pahami emit
-> baca state dengan BlocBuilder
-> jalankan side effect dengan BlocListener
-> baru pahami Bloc event-state
```

Materi ini sengaja dimulai dari Cubit, karena Cubit lebih mudah dipahami daripada Bloc penuh. Cubit cukup memanggil function, lalu function itu mengirim state baru dengan `emit`.

Analogi sederhana:

```text
Cubit seperti remote control.
User menekan tombol function.
Cubit mengirim state baru.
UI menyesuaikan tampilan.
```

Sedangkan Bloc lebih formal:

```text
Bloc seperti loket proses.
User mengirim event.
Bloc membaca event.
Bloc menentukan state baru.
UI menyesuaikan tampilan.
```

Hal yang harus dipahami setelah materi ini:

- perbedaan Cubit dan Bloc
- kenapa state sebaiknya immutable
- apa fungsi `emit`
- kapan memakai `BlocBuilder`
- kapan memakai `BlocListener`
- kapan memakai `BlocConsumer`
- kenapa side effect tidak ditaruh di builder
- kapan Cubit cukup dan kapan Bloc lebih cocok

---

## Gambaran Alur Cubit/Bloc

Alur Cubit:

```text
User menekan tombol
-> UI memanggil function Cubit
-> Cubit memproses logic
-> Cubit emit state baru
-> BlocBuilder rebuild UI
```

Alur Bloc:

```text
User menekan tombol
-> UI mengirim event
-> Bloc menerima event
-> Bloc memproses logic
-> Bloc emit state baru
-> BlocBuilder rebuild UI
```

Perbandingan cepat:

| Bagian | Cubit | Bloc |
| --- | --- | --- |
| Cara mengubah state | Memanggil function | Mengirim event |
| Boilerplate | Lebih sedikit | Lebih banyak |
| Cocok untuk | Logic sederhana-menengah | Flow kompleks |
| Mudah dipelajari | Lebih mudah | Lebih formal |
| Contoh | `increment()` | `CounterIncrementPressed()` |

---

## 1. Apa Itu Cubit dan Bloc

Cubit dan Bloc berasal dari package `bloc` dan `flutter_bloc`.

Secara sederhana:

```text
Cubit -> function langsung mengubah state
Bloc -> event masuk, lalu event diproses menjadi state
```

Contoh Cubit:

```text
UI tekan tombol
-> panggil increment()
-> Cubit emit state baru
-> UI rebuild
```

Contoh Bloc:

```text
UI tekan tombol
-> kirim IncrementPressed event
-> Bloc memproses event
-> Bloc emit state baru
-> UI rebuild
```

Kapan memakai Cubit?

- logic masih cukup sederhana
- ingin state management rapi tanpa terlalu banyak boilerplate
- cocok untuk counter, form, filter, task lokal, auth sederhana

Kapan memakai Bloc?

- flow lebih kompleks
- butuh event yang eksplisit
- banyak aksi dari UI/API/background
- cocok untuk aplikasi besar atau tim besar

Rekomendasi belajar:

```text
Cubit dulu -> baru Bloc
```

---

## 2. Install flutter_bloc

Tambahkan package:

```bash
flutter pub add flutter_bloc
```

Lalu:

```bash
flutter pub get
```

Import:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';
```

Package `flutter_bloc` menyediakan widget seperti:

- `BlocProvider`
- `BlocBuilder`
- `BlocListener`
- `BlocConsumer`
- `MultiBlocProvider`

Widget tersebut bisa dipakai untuk Cubit maupun Bloc.

---

## 3. Konsep State

State adalah kondisi aplikasi saat ini.

Contoh counter:

```dart
int count = 0;
```

Contoh task manager:

```dart
class TaskState {
  final List<Task> tasks;
  final String searchQuery;
  final TaskStatus? selectedStatus;

  const TaskState({
    required this.tasks,
    required this.searchQuery,
    required this.selectedStatus,
  });
}
```

Di Cubit/Bloc, state biasanya dibuat immutable. Artinya, saat ada perubahan, kita membuat state baru, bukan mengubah state lama secara langsung.

Alasannya:

- perubahan lebih mudah dilacak
- UI lebih mudah rebuild
- data lebih aman
- testing lebih mudah

---

## 4. Cubit Counter

Buat file:

```text
lib/cubits/counter_cubit.dart
```

Isi:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class CounterCubit extends Cubit<int> {
  CounterCubit() : super(0);

  void increment() {
    emit(state + 1);
  }

  void decrement() {
    if (state == 0) return;

    emit(state - 1);
  }

  void reset() {
    emit(0);
  }
}
```

Penjelasan:

- `CounterCubit extends Cubit<int>` berarti state Cubit adalah `int`.
- `super(0)` adalah nilai awal state.
- `state` adalah nilai saat ini.
- `emit(...)` mengirim state baru.

Jika lupa `emit`, UI tidak akan menerima perubahan state.

---

## 5. BlocProvider

`BlocProvider` menyediakan Cubit/Bloc ke widget tree.

Contoh `main.dart`:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import 'cubits/counter_cubit.dart';
import 'pages/counter_page.dart';

void main() {
  runApp(
    BlocProvider(
      create: (context) => CounterCubit(),
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

- `BlocProvider` membuat `CounterCubit`.
- Widget di bawah `MyApp` bisa membaca `CounterCubit`.
- `BlocProvider` juga mengurus lifecycle Cubit.

---

## 6. BlocBuilder

`BlocBuilder` digunakan untuk membangun UI berdasarkan state.

Buat file:

```text
lib/pages/counter_page.dart
```

Isi:

```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';

import '../cubits/counter_cubit.dart';

class CounterPage extends StatelessWidget {
  const CounterPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Cubit Counter'),
      ),
      body: Center(
        child: BlocBuilder<CounterCubit, int>(
          builder: (context, count) {
            return Text(
              '$count',
              style: Theme.of(context).textTheme.displayLarge,
            );
          },
        ),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: () {
          context.read<CounterCubit>().increment();
        },
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

Penjelasan:

- `BlocBuilder<CounterCubit, int>` membaca state dari `CounterCubit`.
- `builder` dipanggil saat state berubah.
- `context.read<CounterCubit>().increment()` memanggil function Cubit.

Aturan sederhana:

```text
BlocBuilder -> untuk membangun UI
context.read -> untuk memanggil function/action
```

---

## 7. BlocListener

`BlocListener` dipakai untuk side effect, bukan untuk membangun UI.

Contoh side effect:

- menampilkan `SnackBar`
- membuka halaman baru
- menampilkan dialog
- menutup halaman

Contoh:

```dart
BlocListener<CounterCubit, int>(
  listener: (context, count) {
    if (count == 10) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Counter sudah mencapai 10'),
        ),
      );
    }
  },
  child: BlocBuilder<CounterCubit, int>(
    builder: (context, count) {
      return Text('$count');
    },
  ),
)
```

Penjelasan:

- `BlocBuilder` mengurus tampilan.
- `BlocListener` mengurus aksi tambahan saat state berubah.

Jangan menampilkan `SnackBar` dari dalam `BlocBuilder`. Pakai `BlocListener`.

---

## 8. BlocConsumer

`BlocConsumer` menggabungkan `BlocBuilder` dan `BlocListener`.

Contoh:

```dart
BlocConsumer<CounterCubit, int>(
  listener: (context, count) {
    if (count == 10) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(
          content: Text('Counter mencapai 10'),
        ),
      );
    }
  },
  builder: (context, count) {
    return Text('$count');
  },
)
```

Gunakan `BlocConsumer` jika satu widget butuh:

- rebuild UI
- side effect

Jika hanya butuh rebuild, pakai `BlocBuilder`.

Jika hanya butuh side effect, pakai `BlocListener`.

---

## 9. MultiBlocProvider

Jika aplikasi punya beberapa Cubit/Bloc, gunakan `MultiBlocProvider`.

Contoh:

```dart
void main() {
  runApp(
    MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (context) => CounterCubit(),
        ),
        BlocProvider(
          create: (context) => ThemeCubit(),
        ),
      ],
      child: const MyApp(),
    ),
  );
}
```

Kapan dipakai?

- saat ada Cubit untuk auth
- Cubit untuk theme
- Cubit untuk task
- Cubit untuk profile

Dengan `MultiBlocProvider`, struktur root aplikasi lebih rapi.

---

## 10. Membuat Task State

Untuk Task Manager, kita butuh state yang lebih lengkap.

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

  const TaskState({
    this.tasks = const [],
    this.selectedStatus,
    this.searchQuery = '',
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
  }) {
    return TaskState(
      tasks: tasks ?? this.tasks,
      selectedStatus: clearSelectedStatus
          ? null
          : selectedStatus ?? this.selectedStatus,
      searchQuery: searchQuery ?? this.searchQuery,
    );
  }
}
```

Penjelasan:

- `tasks` menyimpan semua task.
- `selectedStatus` menyimpan filter.
- `searchQuery` menyimpan keyword search.
- `visibleTasks` menghitung hasil yang tampil.
- `copyWith` membuat state baru dari state lama.

---

## 11. Membuat TaskCubit

Buat file:

```text
lib/cubits/task_cubit.dart
```

Isi:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

import '../models/task.dart';
import 'task_state.dart';

class TaskCubit extends Cubit<TaskState> {
  TaskCubit() : super(const TaskState());

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

    emit(
      state.copyWith(
        tasks: [...state.tasks, task],
      ),
    );
  }

  void updateTask(Task updatedTask) {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == updatedTask.id) updatedTask else task,
    ];

    emit(
      state.copyWith(tasks: updatedTasks),
    );
  }

  void updateStatus(int id, TaskStatus status) {
    final updatedTasks = [
      for (final task in state.tasks)
        if (task.id == id) task.copyWith(status: status) else task,
    ];

    emit(
      state.copyWith(tasks: updatedTasks),
    );
  }

  void deleteTask(int id) {
    final updatedTasks = state.tasks
        .where((task) => task.id != id)
        .toList();

    emit(
      state.copyWith(tasks: updatedTasks),
    );
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

Penjelasan:

- `TaskCubit` menyimpan seluruh logic Task Manager.
- UI tidak perlu tahu cara list difilter atau diubah.
- Setiap perubahan memakai `emit(state.copyWith(...))`.
- Data list dibuat baru agar perubahan state lebih jelas.

---

## 12. Menggunakan TaskCubit di UI

Daftarkan provider:

```dart
BlocProvider(
  create: (context) => TaskCubit(),
  child: const TaskListPage(),
)
```

Atau di root:

```dart
MultiBlocProvider(
  providers: [
    BlocProvider(
      create: (context) => TaskCubit(),
    ),
  ],
  child: const MyApp(),
)
```

Contoh halaman:

```dart
class TaskListPage extends StatelessWidget {
  const TaskListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Task Manager Cubit'),
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
                context.read<TaskCubit>().setSearchQuery(value);
              },
            ),
          ),
          Expanded(
            child: BlocBuilder<TaskCubit, TaskState>(
              builder: (context, state) {
                final visibleTasks = state.visibleTasks;

                if (visibleTasks.isEmpty) {
                  return Center(
                    child: Text(state.emptyMessage),
                  );
                }

                return ListView.builder(
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
                          context.read<TaskCubit>().deleteTask(task.id);
                        },
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

Penjelasan:

- `BlocBuilder` membaca `TaskState`.
- `state.visibleTasks` dipakai untuk menampilkan data akhir.
- Tombol hapus memanggil `TaskCubit`.

---

## 13. Filter Status dengan Cubit

Tambahkan di UI:

```dart
BlocBuilder<TaskCubit, TaskState>(
  builder: (context, state) {
    return SingleChildScrollView(
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
                label: Text(status.name),
                selected: state.selectedStatus == status,
                onSelected: (_) {
                  context.read<TaskCubit>().setStatusFilter(status);
                },
              ),
            );
          }),
        ],
      ),
    );
  },
)
```

Jika label status ingin lebih bagus, buat extension:

```dart
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
```

Lalu gunakan:

```dart
Text(status.label)
```

---

## 14. Mengenal Bloc dengan Event-State

Cubit memanggil function langsung:

```dart
context.read<CounterCubit>().increment();
```

Bloc memakai event:

```dart
context.read<CounterBloc>().add(CounterIncrementPressed());
```

Alur Bloc:

```text
UI mengirim event
-> Bloc menerima event
-> Bloc memproses event
-> Bloc emit state baru
-> UI rebuild
```

Contoh event:

```dart
sealed class CounterEvent {}

class CounterIncrementPressed extends CounterEvent {}

class CounterDecrementPressed extends CounterEvent {}

class CounterResetPressed extends CounterEvent {}
```

Contoh Bloc:

```dart
import 'package:flutter_bloc/flutter_bloc.dart';

class CounterBloc extends Bloc<CounterEvent, int> {
  CounterBloc() : super(0) {
    on<CounterIncrementPressed>((event, emit) {
      emit(state + 1);
    });

    on<CounterDecrementPressed>((event, emit) {
      if (state == 0) return;
      emit(state - 1);
    });

    on<CounterResetPressed>((event, emit) {
      emit(0);
    });
  }
}
```

Memakai di UI:

```dart
context.read<CounterBloc>().add(CounterIncrementPressed());
```

Kapan pakai Bloc dibanding Cubit?

- saat aksi user perlu direpresentasikan sebagai event
- saat flow lebih kompleks
- saat perlu logging event
- saat aplikasi besar dan tim butuh aturan lebih eksplisit

Untuk pemula, Cubit biasanya cukup untuk mulai.

---

## 15. BlocBuilder vs BlocListener vs BlocConsumer

Ringkasan:

| Widget | Fungsi |
| --- | --- |
| `BlocBuilder` | Membuat UI berdasarkan state |
| `BlocListener` | Menjalankan side effect saat state berubah |
| `BlocConsumer` | Gabungan builder dan listener |

Contoh penggunaan:

```text
Menampilkan list data -> BlocBuilder
Menampilkan SnackBar -> BlocListener
Menampilkan UI dan SnackBar -> BlocConsumer
```

Jangan gunakan `BlocBuilder` untuk navigasi atau dialog. Gunakan `BlocListener`.

---

## 16. Kesalahan Umum Cubit/Bloc

### Lupa emit

Kurang tepat:

```dart
void increment() {
  state + 1;
}
```

Benar:

```dart
void increment() {
  emit(state + 1);
}
```

### Mengubah list lama secara langsung

Kurang aman:

```dart
state.tasks.add(task);
emit(state);
```

Lebih baik:

```dart
emit(
  state.copyWith(
    tasks: [...state.tasks, task],
  ),
);
```

### BlocProvider tidak berada di atas widget

Jika muncul error Cubit/Bloc tidak ditemukan, biasanya `BlocProvider` belum membungkus widget yang membaca Cubit/Bloc.

### Side effect di BlocBuilder

Kurang tepat:

```dart
BlocBuilder<AuthCubit, AuthState>(
  builder: (context, state) {
    if (state is AuthSuccess) {
      Navigator.push(...);
    }

    return Container();
  },
)
```

Lebih baik gunakan `BlocListener`.

---

## 17. Kapan Memakai Cubit/Bloc

Cubit cocok untuk:

- counter
- form sederhana
- filter/search
- CRUD lokal
- task manager
- auth sederhana

Bloc cocok untuk:

- flow kompleks
- banyak event
- aplikasi besar
- project tim
- fitur yang butuh audit event
- logic yang perlu sangat eksplisit

Urutan belajar:

```text
setState
-> Provider
-> Riverpod
-> Cubit
-> Bloc
```

Atau jika ingin fokus enterprise:

```text
setState
-> Cubit
-> Bloc
```

---

## Latihan Cubit dan Bloc

Kerjakan dari Cubit dulu. Bloc penuh bisa dipelajari setelah Cubit terasa jelas.

### Latihan 1: CounterCubit

Buat `CounterCubit` dengan:

- `increment`
- `decrement`
- `reset`
- tidak boleh kurang dari 0

Pertanyaan untuk dicek:

- Apakah state awal dari `super(0)`?
- Apakah setiap perubahan memakai `emit`?
- Apakah UI memakai `BlocBuilder`?
- Apakah tombol memakai `context.read<CounterCubit>()`?

### Latihan 2: TaskCubit

Buat `TaskCubit` dengan state khusus bernama `TaskState`.

Target:

- `tasks`
- `selectedStatus`
- `searchQuery`
- `visibleTasks`
- `emptyMessage`

Action:

- `addTask`
- `updateTask`
- `updateStatus`
- `deleteTask`
- `setStatusFilter`
- `setSearchQuery`

Pertanyaan untuk dicek:

- Apakah state dibuat immutable?
- Apakah update list membuat list baru?
- Apakah `copyWith` sudah dipakai?

### Latihan 3: BlocListener

Tambahkan listener untuk menampilkan `SnackBar` setelah task berhasil dihapus.

Tujuannya:

- pahami bahwa `BlocBuilder` untuk UI
- pahami bahwa `BlocListener` untuk side effect

### Latihan 4: CounterBloc

Setelah Cubit aman, buat versi Bloc:

- `CounterIncrementPressed`
- `CounterDecrementPressed`
- `CounterResetPressed`

Bandingkan dengan Cubit:

- mana yang lebih mudah ditulis?
- mana yang lebih eksplisit?
- kapan event terasa berguna?

---

## 18. Checklist Cubit dan Bloc

Pastikan sudah paham:

- [ ] Cubit mengubah state lewat function.
- [ ] Bloc mengubah state lewat event.
- [ ] `emit` dipakai untuk mengirim state baru.
- [ ] `BlocProvider` menyediakan Cubit/Bloc.
- [ ] `BlocBuilder` membangun UI.
- [ ] `BlocListener` menjalankan side effect.
- [ ] `BlocConsumer` menggabungkan builder dan listener.
- [ ] `MultiBlocProvider` dipakai untuk banyak Cubit/Bloc.
- [ ] State sebaiknya immutable.
- [ ] List sebaiknya diperbarui dengan membuat list baru.
- [ ] Cubit cocok sebelum masuk Bloc penuh.

Jika checklist ini aman, langkah berikutnya bisa **Upgrade Project Task Manager dengan Cubit**, atau lanjut ke **Local Storage** agar data tidak hilang saat aplikasi ditutup.

---

## Referensi Resmi

- [flutter_bloc package - pub.dev](https://pub.dev/packages/flutter_bloc)
- [flutter_bloc API docs](https://pub.dev/documentation/flutter_bloc/latest/flutter_bloc/)
- [Flutter Bloc Concepts](https://bloclibrary.dev/flutter-bloc-concepts/)
