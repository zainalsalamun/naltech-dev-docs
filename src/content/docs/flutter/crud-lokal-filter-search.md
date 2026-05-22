---
title: "CRUD Lokal, Filter, dan Search"
description: "Materi praktik untuk mengelola data lokal di Flutter: create, read, update, delete, filter, search, dan enum status task."
category: "Flutter"
level: "Foundation"
order: 36
tags: ["flutter", "crud", "filter", "search", "task"]
updated: "2026-05-20"
---

# CRUD Lokal, Filter, dan Search

Sebelum membuat Project 2: Task Manager, kita perlu memahami cara mengelola data lokal di memory. Materi ini membahas CRUD, edit berdasarkan id, filter status, search, dan penggunaan `enum`.

CRUD adalah singkatan dari:

- Create: menambah data
- Read: membaca atau menampilkan data
- Update: mengubah data
- Delete: menghapus data

Di project Flutter, CRUD bisa terjadi di memory, local storage, database, atau API. Untuk pemula, mulai dulu dari data lokal di memory.

Cara memahami materi ini:

```text
Data disimpan di List
-> user melakukan aksi
-> List berubah
-> setState dipanggil
-> UI membaca ulang List
-> tampilan berubah
```

Pada tahap ini, kita belum memakai database. Semua data hanya disimpan di memory aplikasi. Artinya, data akan hilang ketika aplikasi ditutup. Itu tidak masalah untuk belajar, karena fokus utama materi ini adalah memahami logika CRUD terlebih dahulu.

Bayangkan aplikasi Task Manager seperti papan tugas kecil:

- saat user menambah task, kita memasukkan kartu baru ke papan
- saat user melihat task, kita membaca semua kartu di papan
- saat user mengedit task, kita mengganti isi kartu tertentu
- saat user menghapus task, kita membuang kartu dari papan
- saat user filter/search, kita tidak menghapus data asli, hanya memilih kartu mana yang ingin ditampilkan

Hal yang harus dipahami setelah materi ini:

- dari mana data berasal
- bagaimana data ditambahkan
- bagaimana data dicari berdasarkan `id`
- kenapa update lebih aman memakai `copyWith`
- kenapa filter dan search sebaiknya tidak mengubah data asli
- kapan UI harus dipanggil ulang dengan `setState`

---

## Cara Berpikir CRUD Lokal

Sebelum masuk ke kode, pahami dulu peran setiap bagian.

| Bagian | Tugas |
| --- | --- |
| `Task` | Bentuk data task |
| `List<Task>` | Tempat menyimpan banyak task |
| `addTask` | Menambahkan task baru |
| `updateTask` | Mengubah task yang sudah ada |
| `deleteTask` | Menghapus task |
| `filteredTasks` | Menentukan task mana yang tampil |
| `searchQuery` | Kata kunci pencarian |
| `selectedStatus` | Filter status yang sedang aktif |

Contoh alur tambah data:

```text
User isi form
-> tekan tombol Simpan
-> aplikasi membuat object Task
-> Task dimasukkan ke List
-> setState dipanggil
-> ListView menampilkan data baru
```

Contoh alur filter data:

```text
Data asli tetap lengkap
-> user memilih status Done
-> aplikasi membuat hasil filter sementara
-> UI menampilkan hasil filter
-> data asli tidak berubah
```

Ini penting. Filter dan search sebaiknya hanya mengatur tampilan, bukan menghapus data asli.

---

## 1. Membuat Model Task

Kita akan memakai contoh data task.

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
}
```

Penjelasan:

- `TaskStatus` membatasi status yang boleh dipakai.
- `id` dipakai sebagai identitas unik.
- `title` adalah nama task.
- `description` adalah detail task.
- `status` menyimpan posisi task.

Kenapa memakai `enum`?

Karena status task hanya punya pilihan tertentu. Dengan `enum`, kita menghindari typo seperti `'progres'`, `'Progress'`, atau `'in progress'`.

---

## 2. Read: Menampilkan Data

Contoh data awal:

```dart
final List<Task> tasks = [
  const Task(
    id: 1,
    title: 'Belajar Dart',
    description: 'Pahami variable, function, List, dan Map.',
    status: TaskStatus.done,
  ),
  const Task(
    id: 2,
    title: 'Belajar Widget',
    description: 'Pahami Text, Container, Column, dan Row.',
    status: TaskStatus.progress,
  ),
];
```

Menampilkan data dengan `ListView.builder`:

```dart
ListView.builder(
  itemCount: tasks.length,
  itemBuilder: (context, index) {
    final task = tasks[index];

    return ListTile(
      title: Text(task.title),
      subtitle: Text(task.description),
      trailing: Text(task.status.name),
    );
  },
)
```

Penjelasan:

- `itemCount` menentukan jumlah item.
- `index` dipakai untuk mengambil task.
- `task.status.name` menampilkan nama enum sebagai teks.

---

## 3. Create: Menambah Data

Untuk menambah data, buat function khusus.

```dart
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

  setState(() {
    tasks.add(task);
  });
}
```

Penjelasan:

- `DateTime.now().millisecondsSinceEpoch` dipakai sebagai id sederhana.
- Task baru otomatis diberi status `todo`.
- `tasks.add(task)` menambahkan task ke List.
- `setState()` memperbarui UI.

Catatan:

Untuk aplikasi produksi, id biasanya berasal dari database atau backend. Untuk latihan lokal, id dari timestamp sudah cukup.

---

## 4. Update: Mengubah Data

Karena property `Task` dibuat `final`, kita tidak mengubah object lama secara langsung. Kita buat object baru dengan data yang diperbarui.

Tambahkan method `copyWith`:

```dart
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

Mengubah status task:

```dart
void updateTaskStatus(int id, TaskStatus status) {
  final index = tasks.indexWhere((task) => task.id == id);

  if (index == -1) return;

  setState(() {
    tasks[index] = tasks[index].copyWith(status: status);
  });
}
```

Penjelasan:

- `indexWhere` mencari posisi task berdasarkan id.
- Jika tidak ditemukan, hasilnya `-1`.
- `copyWith` membuat Task baru dengan status baru.
- Data lama di index tersebut diganti dengan data baru.

---

## 5. Delete: Menghapus Data

Menghapus berdasarkan id:

```dart
void deleteTask(int id) {
  setState(() {
    tasks.removeWhere((task) => task.id == id);
  });
}
```

Penjelasan:

- `removeWhere` menghapus semua item yang sesuai kondisi.
- Karena id unik, hanya satu task yang terhapus.

Contoh tombol hapus:

```dart
IconButton(
  icon: const Icon(Icons.delete_outline),
  onPressed: () => deleteTask(task.id),
)
```

Untuk UX yang lebih aman, tambahkan konfirmasi sebelum hapus:

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

  if (result == true) {
    deleteTask(task.id);
  }
}
```

---

## 6. Filter Berdasarkan Status

Filter dipakai untuk menampilkan data sesuai kondisi tertentu.

State filter:

```dart
TaskStatus? selectedStatus;
```

Jika `selectedStatus == null`, tampilkan semua task. Jika ada status, tampilkan task dengan status tersebut.

```dart
List<Task> get filteredTasks {
  if (selectedStatus == null) {
    return tasks;
  }

  return tasks
      .where((task) => task.status == selectedStatus)
      .toList();
}
```

Contoh tombol filter:

```dart
Wrap(
  spacing: 8,
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
    ChoiceChip(
      label: const Text('Todo'),
      selected: selectedStatus == TaskStatus.todo,
      onSelected: (_) {
        setState(() {
          selectedStatus = TaskStatus.todo;
        });
      },
    ),
  ],
)
```

Challenge:

- Tambahkan chip untuk `progress`.
- Tambahkan chip untuk `done`.
- Ubah warna chip aktif agar lebih jelas.

---

## 7. Search Task

Search dipakai untuk mencari task berdasarkan teks.

State search:

```dart
String searchQuery = '';
```

Input search:

```dart
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
)
```

Filter berdasarkan query:

```dart
List<Task> get searchedTasks {
  final query = searchQuery.toLowerCase();

  if (query.isEmpty) {
    return filteredTasks;
  }

  return filteredTasks.where((task) {
    final title = task.title.toLowerCase();
    final description = task.description.toLowerCase();

    return title.contains(query) || description.contains(query);
  }).toList();
}
```

Gunakan `searchedTasks` di `ListView.builder`:

```dart
final visibleTasks = searchedTasks;

ListView.builder(
  itemCount: visibleTasks.length,
  itemBuilder: (context, index) {
    final task = visibleTasks[index];

    return ListTile(
      title: Text(task.title),
      subtitle: Text(task.description),
    );
  },
)
```

Penjelasan:

- Search dibuat case-insensitive dengan `toLowerCase()`.
- Pencarian dilakukan pada `title` dan `description`.
- Search diterapkan setelah filter status.

---

## 8. Empty State untuk Filter dan Search

Saat hasil filter atau search kosong, tampilkan pesan yang jelas.

```dart
if (visibleTasks.isEmpty) {
  return const Center(
    child: Text('Task tidak ditemukan'),
  );
}
```

Pesan kosong bisa dibedakan:

```dart
String get emptyMessage {
  if (searchQuery.isNotEmpty) {
    return 'Tidak ada task yang cocok dengan pencarian';
  }

  if (selectedStatus != null) {
    return 'Belum ada task dengan status ini';
  }

  return 'Belum ada task';
}
```

Lalu gunakan:

```dart
Center(
  child: Text(emptyMessage),
)
```

Ini membuat aplikasi terasa lebih jelas untuk user.

---

## 9. Alur CRUD Task Manager

Alur yang akan dipakai di project Task Manager:

```text
Create
-> user mengisi form
-> aplikasi membuat Task baru
-> Task masuk ke List

Read
-> aplikasi membaca List
-> data tampil di ListView

Update
-> user edit title, description, atau status
-> aplikasi mencari Task berdasarkan id
-> Task diganti dengan copy baru

Delete
-> user tekan hapus
-> aplikasi meminta konfirmasi
-> Task dihapus berdasarkan id

Filter dan Search
-> user memilih status atau mengetik keyword
-> aplikasi menghitung visibleTasks
-> ListView menampilkan hasil akhir
```

---

## Latihan Bertahap

Kerjakan latihan ini sebelum masuk Project Task Manager.

### Latihan 1: Tambah Data

Buat function `addTask`, lalu tambahkan minimal 3 task awal.

Target:

- task punya `id`
- task punya `title`
- task punya `description`
- task punya `status`

Pertanyaan untuk dicek:

- Apakah task baru muncul di UI?
- Apakah `setState` sudah dipanggil?
- Apakah task baru otomatis punya status `todo`?

### Latihan 2: Update Status

Buat function untuk mengubah status task dari `todo` menjadi `progress`, lalu dari `progress` menjadi `done`.

Target:

- cari task berdasarkan `id`
- gunakan `copyWith`
- jangan mengubah object lama secara langsung

Pertanyaan untuk dicek:

- Apa yang terjadi jika `id` tidak ditemukan?
- Kenapa perlu `indexWhere`?
- Kenapa tidak cukup memakai `tasks[index].status = status`?

### Latihan 3: Filter dan Search

Buat filter status dan search keyword.

Target:

- filter `todo`
- filter `progress`
- filter `done`
- search berdasarkan `title`
- search berdasarkan `description`

Pertanyaan untuk dicek:

- Apakah data asli tetap aman?
- Apakah search bekerja meskipun huruf besar/kecil berbeda?
- Apa pesan yang tampil jika hasil kosong?

---

## 10. Checklist CRUD Lokal

Pastikan kamu sudah paham:

- [ ] Bisa membuat model `Task`.
- [ ] Bisa memakai `enum` untuk status.
- [ ] Bisa menambah item ke `List`.
- [ ] Bisa menampilkan item dengan `ListView.builder`.
- [ ] Bisa mengubah item berdasarkan `id`.
- [ ] Bisa menghapus item berdasarkan `id`.
- [ ] Bisa memakai `copyWith`.
- [ ] Bisa filter data dengan `.where()`.
- [ ] Bisa search data dengan `.contains()`.
- [ ] Bisa menampilkan empty state yang sesuai kondisi.

Jika checklist ini sudah aman, kamu siap masuk **Project 2: Task Manager**.
