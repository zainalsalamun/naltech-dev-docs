---
title: "Repository Pattern Sederhana"
description: "Panduan belajar Repository Pattern di Flutter: bedanya service dan repository, alur UI-State-Repository-Service, TaskRepository, dan persiapan menuju API/Firebase."
category: "Flutter"
level: "Architecture"
order: 61
tags: ["flutter", "repository-pattern", "architecture", "service", "firebase"]
updated: "2026-05-23"
---

# Repository Pattern Sederhana

Repository Pattern adalah pola untuk memisahkan logic pengambilan data dari UI dan state management. Repository menjadi jembatan antara aplikasi dan sumber data seperti local storage, API, database, atau Firebase.

Materi ini penting setelah belajar:

- Task Manager
- Local Storage
- Provider/Riverpod/Cubit
- `TaskStorageService`

Kenapa? Karena sebelum masuk Firebase atau API, kita perlu membuat struktur data yang lebih rapi agar sumber data bisa diganti tanpa merombak seluruh aplikasi.

---

## 1. Masalah Tanpa Repository

Saat project masih kecil, state management bisa langsung memanggil service:

```text
TaskCubit
-> TaskStorageService
-> shared_preferences
```

Ini masih aman untuk belajar. Tapi ketika sumber data bertambah, struktur mulai terasa kurang rapi.

Contoh nanti aplikasi butuh:

- data lokal dari `shared_preferences`
- data online dari Firestore
- data dari REST API
- cache lokal
- sync offline-online

Jika semua logic ditulis langsung di Cubit/Provider, file state akan menjadi penuh.

Masalah yang muncul:

- UI/state tahu terlalu banyak detail teknis storage
- sulit mengganti storage ke Firestore/API
- sulit testing karena state langsung bergantung ke package tertentu
- logic cache/sync bercampur dengan logic UI

Repository membantu memisahkan masalah ini.

---

## 2. Apa Itu Repository

Repository adalah class yang bertanggung jawab menyediakan data untuk aplikasi.

Bayangkan repository sebagai loket data:

```text
UI tidak peduli data datang dari mana.
State management tidak perlu tahu detail storage/API.
Repository yang memutuskan ambil data dari mana.
```

Alur:

```text
UI
-> State Management
-> Repository
-> Service / Storage / API / Firebase
```

Contoh:

```text
TaskListPage
-> TaskCubit
-> TaskRepository
-> TaskStorageService
-> shared_preferences
```

Nanti saat pindah ke Firestore:

```text
TaskListPage
-> TaskCubit
-> TaskRepository
-> TaskFirestoreService
-> Firestore
```

UI dan Cubit tidak perlu berubah banyak karena tetap memanggil repository.

---

## 3. Service vs Repository

Ini bagian yang sering membingungkan.

| Layer | Tugas |
| --- | --- |
| Service | Detail teknis komunikasi dengan storage/API/Firebase |
| Repository | Aturan pengambilan data untuk aplikasi |

Contoh service:

```dart
class TaskStorageService {
  Future<List<Task>> loadTasks() async {
    // baca shared_preferences
  }

  Future<void> saveTasks(List<Task> tasks) async {
    // simpan shared_preferences
  }
}
```

Service tahu detail:

- package apa yang dipakai
- key storage apa
- cara encode/decode JSON
- cara request API
- cara query Firestore

Repository:

```dart
class TaskRepository {
  Future<List<Task>> getTasks() async {
    return storageService.loadTasks();
  }

  Future<void> saveTasks(List<Task> tasks) async {
    await storageService.saveTasks(tasks);
  }
}
```

Repository menyediakan API yang lebih dekat ke kebutuhan aplikasi:

- get tasks
- save tasks
- add task
- update task
- delete task

---

## 4. Kapan Repository Dibutuhkan

Repository mulai berguna ketika:

- aplikasi punya lebih dari satu sumber data
- state management mulai terlalu penuh
- ingin mudah pindah dari local storage ke API/Firebase
- ingin menambahkan cache
- ingin melakukan testing
- ingin struktur project lebih scalable

Untuk project sangat kecil, repository tidak wajib.

Untuk project belajar yang menuju production, repository sangat membantu.

Aturan sederhana:

```text
Project kecil -> Service langsung masih boleh
Project mulai besar -> pakai Repository
Project API/Firebase -> sangat disarankan pakai Repository
```

---

## 5. Struktur Folder

Struktur sederhana:

```text
lib/
  models/
    task.dart
  repositories/
    task_repository.dart
  services/
    task_storage_service.dart
  cubits/
    task_cubit.dart
  pages/
    task_list_page.dart
```

Jika memakai feature-based structure:

```text
lib/
  features/
    tasks/
      data/
        repositories/
          task_repository.dart
        services/
          task_storage_service.dart
      models/
        task.dart
      presentation/
        cubits/
        pages/
        widgets/
```

Untuk pemula, mulai dari struktur sederhana dulu.

---

## 6. Membuat TaskRepository

Buat file:

```text
lib/repositories/task_repository.dart
```

Isi:

```dart
import '../models/task.dart';
import '../services/task_storage_service.dart';

class TaskRepository {
  final TaskStorageService _storageService;

  TaskRepository({
    TaskStorageService? storageService,
  }) : _storageService = storageService ?? TaskStorageService();

  Future<List<Task>> getTasks() async {
    return _storageService.loadTasks();
  }

  Future<void> saveTasks(List<Task> tasks) async {
    await _storageService.saveTasks(tasks);
  }

  Future<void> clearTasks() async {
    await _storageService.clearTasks();
  }
}
```

Penjelasan:

- Repository menerima `TaskStorageService`.
- Jika service tidak dikirim, repository membuat service sendiri.
- `getTasks()` membaca data.
- `saveTasks()` menyimpan data.
- `clearTasks()` menghapus semua data.

Ini masih sederhana, tapi sudah memisahkan Cubit/Provider dari detail storage.

---

## 7. Repository dengan CRUD Lebih Lengkap

Repository juga bisa menyimpan logic CRUD.

```dart
class TaskRepository {
  final TaskStorageService _storageService;

  TaskRepository({
    TaskStorageService? storageService,
  }) : _storageService = storageService ?? TaskStorageService();

  Future<List<Task>> getTasks() async {
    return _storageService.loadTasks();
  }

  Future<List<Task>> addTask({
    required List<Task> currentTasks,
    required Task task,
  }) async {
    final updatedTasks = [...currentTasks, task];
    await _storageService.saveTasks(updatedTasks);
    return updatedTasks;
  }

  Future<List<Task>> updateTask({
    required List<Task> currentTasks,
    required Task updatedTask,
  }) async {
    final updatedTasks = [
      for (final task in currentTasks)
        if (task.id == updatedTask.id) updatedTask else task,
    ];

    await _storageService.saveTasks(updatedTasks);
    return updatedTasks;
  }

  Future<List<Task>> deleteTask({
    required List<Task> currentTasks,
    required int id,
  }) async {
    final updatedTasks = currentTasks
        .where((task) => task.id != id)
        .toList();

    await _storageService.saveTasks(updatedTasks);
    return updatedTasks;
  }
}
```

Dengan pola ini, Cubit cukup meminta repository melakukan perubahan.

Alur:

```text
Cubit punya state.tasks
-> Cubit panggil repository.addTask
-> Repository membuat list baru dan simpan storage
-> Repository mengembalikan list terbaru
-> Cubit emit state baru
```

---

## 8. Menggunakan Repository di Cubit

Sebelumnya Cubit langsung memakai `TaskStorageService`.

Ubah menjadi memakai `TaskRepository`.

```dart
class TaskCubit extends Cubit<TaskState> {
  final TaskRepository _repository;

  TaskCubit({
    TaskRepository? repository,
  })  : _repository = repository ?? TaskRepository(),
        super(const TaskState(isLoading: true)) {
    loadTasks();
  }
}
```

Load tasks:

```dart
Future<void> loadTasks() async {
  emit(
    state.copyWith(
      isLoading: true,
      clearError: true,
    ),
  );

  try {
    final tasks = await _repository.getTasks();

    emit(
      state.copyWith(
        tasks: tasks,
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

Add task:

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

  try {
    final updatedTasks = await _repository.addTask(
      currentTasks: state.tasks,
      task: task,
    );

    emit(
      state.copyWith(
        tasks: updatedTasks,
        clearError: true,
      ),
    );
  } catch (error) {
    emit(
      state.copyWith(
        errorMessage: 'Gagal menambah task',
      ),
    );
  }
}
```

Cubit tidak lagi memanggil storage langsung.

---

## 9. Menggunakan Repository di Provider

Jika memakai Provider:

```dart
class TaskProvider extends ChangeNotifier {
  final TaskRepository _repository;

  TaskProvider({
    TaskRepository? repository,
  }) : _repository = repository ?? TaskRepository() {
    loadTasks();
  }

  final List<Task> _tasks = [];
}
```

Load:

```dart
Future<void> loadTasks() async {
  _isLoading = true;
  _errorMessage = null;
  notifyListeners();

  try {
    final savedTasks = await _repository.getTasks();

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

Add:

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

  try {
    final updatedTasks = await _repository.addTask(
      currentTasks: _tasks,
      task: task,
    );

    _tasks
      ..clear()
      ..addAll(updatedTasks);

    _errorMessage = null;
  } catch (error) {
    _errorMessage = 'Gagal menambah task';
  }

  notifyListeners();
}
```

Provider tetap mengelola state, repository mengelola pengambilan/penyimpanan data.

---

## 10. Menggunakan Repository di Riverpod

Riverpod bisa menyediakan repository sebagai provider.

```dart
final taskRepositoryProvider = Provider<TaskRepository>((ref) {
  return TaskRepository();
});
```

Lalu di notifier:

```dart
class TaskNotifier extends Notifier<TaskState> {
  late final TaskRepository _repository;

  @override
  TaskState build() {
    _repository = ref.read(taskRepositoryProvider);
    loadTasks();

    return const TaskState(isLoading: true);
  }
}
```

Load:

```dart
Future<void> loadTasks() async {
  state = state.copyWith(
    isLoading: true,
    clearError: true,
  );

  try {
    final tasks = await _repository.getTasks();

    state = state.copyWith(
      tasks: tasks,
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

Keuntungan Riverpod:

- repository mudah di-override saat testing
- dependency lebih eksplisit
- state tidak bergantung pada `BuildContext`

---

## 11. Kenapa Repository Memudahkan Firebase

Saat masih local storage:

```dart
class TaskRepository {
  final TaskStorageService _storageService;

  Future<List<Task>> getTasks() {
    return _storageService.loadTasks();
  }
}
```

Saat pindah ke Firestore, repository bisa berubah:

```dart
class TaskRepository {
  final TaskFirestoreService _firestoreService;

  Future<List<Task>> getTasks() {
    return _firestoreService.getTasks();
  }
}
```

UI dan state management tetap memanggil:

```dart
repository.getTasks();
```

Itulah manfaat repository: sumber data bisa berubah, API untuk aplikasi tetap mirip.

---

## 12. Repository dengan Banyak Sumber Data

Nanti repository bisa mengambil data dari dua sumber:

```text
local storage
Firestore/API
```

Contoh konsep:

```dart
class TaskRepository {
  final TaskStorageService _localService;
  final TaskFirestoreService _remoteService;

  Future<List<Task>> getTasks() async {
    final localTasks = await _localService.loadTasks();

    if (localTasks.isNotEmpty) {
      return localTasks;
    }

    final remoteTasks = await _remoteService.getTasks();
    await _localService.saveTasks(remoteTasks);
    return remoteTasks;
  }
}
```

Alur:

```text
Coba baca local
-> jika ada, tampilkan cepat
-> jika kosong, ambil remote
-> simpan remote ke local
-> tampilkan data
```

Ini adalah dasar dari konsep cache.

---

## 13. Repository dan Testing

Repository membuat testing lebih mudah karena kita bisa mengganti implementasi asli dengan fake.

Contoh fake repository:

```dart
class FakeTaskRepository extends TaskRepository {
  final List<Task> fakeTasks;

  FakeTaskRepository(this.fakeTasks);

  @override
  Future<List<Task>> getTasks() async {
    return fakeTasks;
  }
}
```

Saat test:

```dart
final cubit = TaskCubit(
  repository: FakeTaskRepository([
    Task(
      id: 1,
      title: 'Test Task',
      description: 'From fake repository',
      status: TaskStatus.todo,
      createdAt: DateTime.now(),
    ),
  ]),
);
```

Dengan fake repository, test tidak perlu benar-benar membaca shared preferences atau Firestore.

---

## 14. Kapan Repository Terasa Berlebihan

Repository bisa terasa terlalu banyak jika:

- project hanya satu halaman
- data sangat sederhana
- tidak ada rencana API/Firebase
- hanya latihan kecil

Untuk latihan kecil, service langsung dari provider/cubit masih bisa diterima.

Untuk project belajar yang ingin berkembang, repository mulai masuk akal.

Aturan praktis:

```text
Jika mulai bertanya "data ini nanti dari local atau API ya?"
-> saatnya pakai repository.
```

---

## 15. Alur Final yang Direkomendasikan

Untuk Task Manager:

```text
TaskListPage
-> TaskCubit / TaskProvider / TaskNotifier
-> TaskRepository
-> TaskStorageService
-> shared_preferences
```

Untuk Firebase nanti:

```text
TaskListPage
-> State Management
-> TaskRepository
-> TaskFirestoreService
-> Firestore
```

Untuk offline-first:

```text
TaskListPage
-> State Management
-> TaskRepository
-> Local Service + Remote Service
-> Local Storage + Firestore
```

---

## 16. Checklist Repository Pattern

Pastikan sudah paham:

- [ ] Repository menjadi jembatan antara state dan sumber data.
- [ ] Service mengurus detail teknis storage/API.
- [ ] Repository mengurus aturan data untuk aplikasi.
- [ ] UI tidak memanggil service langsung.
- [ ] State management memanggil repository.
- [ ] Repository bisa memakai local storage.
- [ ] Repository bisa diganti ke Firestore/API.
- [ ] Repository memudahkan testing.
- [ ] Repository tidak wajib untuk project kecil.
- [ ] Repository berguna saat aplikasi mulai berkembang.

Jika checklist ini aman, kamu siap masuk materi Firebase Auth atau Firestore CRUD.

---

## 17. Lanjutan Setelah Ini

Materi berikutnya yang cocok:

1. Firebase Authentication.
2. Cloud Firestore CRUD.
3. Task Manager sync ke Firestore.
4. Repository dengan local + remote source.
5. Clean Architecture sederhana.

Urutan yang disarankan:

```text
Repository Pattern
-> Firebase Auth
-> Firestore CRUD
-> Task Manager online
-> Clean Architecture
```
