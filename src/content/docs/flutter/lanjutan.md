---
title: "Tutorial Flutter Lanjutan"
description: "Materi lanjutan Flutter: struktur folder, repository, state management, CRUD, local storage, testing, build, dan publish."
category: "Flutter"
level: "Intermediate"
order: 20
tags: ["flutter", "architecture", "repository", "crud", "testing"]
updated: "2026-05-20"
---

# Tutorial Flutter Lanjutan untuk Pemula yang Naik Level

Materi ini adalah kelanjutan dari **Tutorial Flutter Dasar untuk Pemula**. Jika materi dasar fokus pada widget, layout, state sederhana, navigasi, form, list, API, dan mini project, maka materi lanjutan ini fokus pada cara membuat project Flutter yang lebih rapi, mudah dirawat, dan lebih dekat ke kebutuhan aplikasi nyata.

Target belajar:

- Memahami struktur folder yang lebih scalable.
- Memisahkan UI, model, service, repository, dan state.
- Mengelola loading, success, empty, dan error state.
- Memahami state management dasar dengan `ValueNotifier`, Provider, atau Riverpod secara konseptual.
- Membuat alur API yang lebih rapi.
- Menyimpan data lokal dengan pola yang aman.
- Menambahkan validasi form yang lebih baik.
- Mengenal testing, build, dan publish.

---

## Daftar Isi

1. Kapan Harus Naik dari Dasar ke Lanjutan
2. Mindset Aplikasi Flutter yang Rapi
3. Struktur Folder yang Lebih Scalable
4. Memisahkan Widget Menjadi Komponen Kecil
5. Model Data dan JSON Parsing yang Lebih Aman
6. Service dan Repository
7. Loading, Empty, Error, dan Success State
8. State Management: Dari setState ke Pola yang Lebih Rapi
9. Form Lanjutan dan Validasi
10. Navigasi dengan Named Routes
11. Local Storage dan Cache Sederhana
12. API CRUD Sederhana
13. Theme, Dark Mode, dan Design System Kecil
14. Error Handling yang Enak untuk User
15. Testing Dasar
16. Build dan Persiapan Publish
17. Mini Project Lanjutan: Task Manager
18. Roadmap Setelah Materi Ini

---

## 1. Kapan Harus Naik dari Dasar ke Lanjutan

Kamu siap masuk materi lanjutan jika sudah bisa:

- Membuat project Flutter baru.
- Membuat `StatelessWidget` dan `StatefulWidget`.
- Menggunakan `setState`.
- Membuat layout dengan `Column`, `Row`, `Container`, `Padding`, dan `Expanded`.
- Membaca input dari `TextField`.
- Menampilkan list dengan `ListView.builder`.
- Membuka halaman baru dengan `Navigator.push`.
- Mengambil data API sederhana dengan `FutureBuilder`.

Tanda kamu mulai butuh pola lanjutan:

- File `main.dart` sudah terlalu panjang.
- Banyak kode UI berulang.
- Bingung menaruh function API di mana.
- State mulai tersebar di banyak halaman.
- Error API tidak ditangani dengan konsisten.
- Sulit menambah fitur tanpa merusak fitur lama.

Tujuan materi lanjutan bukan membuat aplikasi menjadi rumit. Tujuannya adalah membuat aplikasi tetap mudah dipahami saat fitur bertambah.

---

## 2. Mindset Aplikasi Flutter yang Rapi

Aplikasi Flutter yang rapi biasanya punya pemisahan tanggung jawab:

- UI menampilkan data dan menerima interaksi user.
- State menyimpan kondisi layar.
- Model mendefinisikan bentuk data.
- Service berbicara dengan API, database, atau plugin.
- Repository menjadi jembatan antara UI/state dan sumber data.

Pola sederhana:

```text
Page -> State/Controller -> Repository -> Service/API
                  |
                Model
```

Penjelasan:

- `Page` fokus pada tampilan.
- `State/Controller` fokus pada perubahan kondisi.
- `Repository` fokus pada aturan ambil/simpan data.
- `Service/API` fokus pada detail teknis request.
- `Model` fokus pada bentuk data.

Saat baru belajar, kamu tidak harus memakai arsitektur besar. Cukup biasakan memisahkan kode sesuai tanggung jawab.

---

## 3. Struktur Folder yang Lebih Scalable

Struktur sederhana untuk project menengah:

```text
lib/
  main.dart
  app.dart
  core/
    constants/
    theme/
    utils/
  features/
    tasks/
      data/
        task_repository.dart
        task_service.dart
      models/
        task.dart
      pages/
        task_list_page.dart
        task_form_page.dart
      widgets/
        task_card.dart
  shared/
    widgets/
```

Kapan memakai folder `features`?

- Saat aplikasi punya beberapa fitur besar.
- Misalnya `auth`, `tasks`, `profile`, `settings`, `products`, `orders`.

Kapan memakai folder `shared`?

- Untuk komponen yang dipakai banyak fitur.
- Misalnya button, empty state, loading view, app text field.

Contoh pembagian sederhana:

- `models/`: class data.
- `pages/`: halaman penuh.
- `widgets/`: komponen kecil.
- `data/`: repository dan service.
- `core/`: konfigurasi umum.

Tips:

- Jangan terlalu cepat membuat banyak folder kosong.
- Tambahkan struktur saat mulai ada kebutuhan.
- Hindari semua kode menumpuk di `main.dart`.

---

## 4. Memisahkan Widget Menjadi Komponen Kecil

Jika satu halaman sudah terlalu panjang, pecah menjadi widget kecil.

Sebelum dipisah:

```dart
Card(
  child: ListTile(
    title: Text(task.title),
    subtitle: Text(task.description),
    trailing: IconButton(
      icon: const Icon(Icons.delete_outline),
      onPressed: onDelete,
    ),
  ),
)
```

Setelah dipisah:

```dart
class TaskCard extends StatelessWidget {
  final Task task;
  final VoidCallback onDelete;

  const TaskCard({
    super.key,
    required this.task,
    required this.onDelete,
  });

  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(task.title),
        subtitle: Text(task.description),
        trailing: IconButton(
          icon: const Icon(Icons.delete_outline),
          onPressed: onDelete,
        ),
      ),
    );
  }
}
```

Manfaat:

- Halaman lebih pendek.
- Komponen bisa dipakai ulang.
- Lebih mudah dites.
- Lebih mudah dibaca oleh developer lain.

Aturan praktis:

- Jika widget punya nama yang jelas, pisahkan.
- Jika widget dipakai lebih dari sekali, pisahkan.
- Jika method `build()` terlalu panjang, pisahkan.

---

## 5. Model Data dan JSON Parsing yang Lebih Aman

Model membantu aplikasi memahami bentuk data.

```dart
class Task {
  final int id;
  final String title;
  final String description;
  final bool isDone;

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.isDone,
  });

  factory Task.fromJson(Map<String, dynamic> json) {
    return Task(
      id: json['id'] as int,
      title: json['title'] as String? ?? '',
      description: json['description'] as String? ?? '',
      isDone: json['isDone'] as bool? ?? false,
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'title': title,
      'description': description,
      'isDone': isDone,
    };
  }
}
```

Kenapa `as String? ?? ''` lebih aman?

- API kadang mengirim nilai kosong.
- Field bisa hilang.
- Aplikasi tidak langsung crash saat data kurang lengkap.

Namun jangan diam-diam mengabaikan semua error. Untuk aplikasi produksi, tetap log error dan validasi data penting.

---

## 6. Service dan Repository

Service fokus pada detail teknis. Repository fokus pada kebutuhan aplikasi.

Contoh service:

```dart
class TaskService {
  Future<List<Map<String, dynamic>>> fetchTasks() async {
    // Request API dilakukan di sini.
    return [];
  }
}
```

Contoh repository:

```dart
class TaskRepository {
  final TaskService service;

  TaskRepository(this.service);

  Future<List<Task>> getTasks() async {
    final jsonList = await service.fetchTasks();
    return jsonList.map(Task.fromJson).toList();
  }
}
```

Manfaat repository:

- UI tidak perlu tahu detail API.
- Kalau sumber data berubah, UI tidak perlu banyak berubah.
- Lebih mudah membuat mock data untuk testing.

Pola pemanggilan:

```text
Page meminta data -> Repository mengambil data -> Service request API
```

---

## 7. Loading, Empty, Error, dan Success State

Aplikasi yang baik tidak hanya menampilkan data. Ia juga harus menjelaskan kondisi layar.

Empat state umum:

- Loading: data sedang diambil.
- Empty: data berhasil diambil, tetapi kosong.
- Error: data gagal diambil.
- Success: data berhasil ditampilkan.

Contoh enum:

```dart
enum ViewStatus {
  initial,
  loading,
  success,
  empty,
  error,
}
```

Contoh pemakaian:

```dart
Widget buildBody() {
  switch (status) {
    case ViewStatus.loading:
      return const Center(child: CircularProgressIndicator());
    case ViewStatus.empty:
      return const Center(child: Text('Belum ada data'));
    case ViewStatus.error:
      return Center(
        child: ElevatedButton(
          onPressed: fetchData,
          child: const Text('Coba Lagi'),
        ),
      );
    case ViewStatus.success:
      return TaskList(tasks: tasks);
    case ViewStatus.initial:
      return const SizedBox.shrink();
  }
}
```

Ini membuat UI lebih jelas dan mudah dirawat.

---

## 8. State Management: Dari setState ke Pola yang Lebih Rapi

`setState` cukup untuk:

- Counter.
- Form sederhana.
- Toggle kecil.
- Halaman dengan state lokal.

Namun saat state dipakai banyak widget atau halaman, gunakan pola yang lebih rapi.

Pilihan bertahap:

1. `setState`
2. `ValueNotifier`
3. Provider
4. Riverpod
5. Bloc/Cubit

### ValueNotifier

`ValueNotifier` cocok untuk state sederhana yang ingin dipisahkan dari widget.

```dart
final counter = ValueNotifier<int>(0);

ValueListenableBuilder<int>(
  valueListenable: counter,
  builder: (context, value, child) {
    return Text('Nilai: $value');
  },
)
```

Ubah nilai:

```dart
counter.value++;
```

### Provider atau Riverpod

Provider dan Riverpod membantu membagikan state ke banyak widget.

Contoh konsep:

```text
Widget membaca state -> Controller mengubah state -> UI otomatis update
```

Untuk pemula, pahami dulu:

- Apa data yang berubah?
- Siapa yang boleh mengubah data itu?
- Widget mana yang perlu membaca data?

Jangan memilih library hanya karena populer. Pilih saat masalahnya memang butuh.

---

## 9. Form Lanjutan dan Validasi

Untuk form yang lebih serius, gunakan `Form` dan `TextFormField`.

```dart
class TaskFormPage extends StatefulWidget {
  const TaskFormPage({super.key});

  @override
  State<TaskFormPage> createState() => _TaskFormPageState();
}

class _TaskFormPageState extends State<TaskFormPage> {
  final formKey = GlobalKey<FormState>();
  final titleController = TextEditingController();

  @override
  void dispose() {
    titleController.dispose();
    super.dispose();
  }

  void save() {
    if (!formKey.currentState!.validate()) return;

    final title = titleController.text.trim();
    Navigator.pop(context, title);
  }

  @override
  Widget build(BuildContext context) {
    return Form(
      key: formKey,
      child: Column(
        children: [
          TextFormField(
            controller: titleController,
            decoration: const InputDecoration(labelText: 'Judul'),
            validator: (value) {
              if (value == null || value.trim().isEmpty) {
                return 'Judul wajib diisi';
              }
              if (value.trim().length < 3) {
                return 'Judul minimal 3 karakter';
              }
              return null;
            },
          ),
          ElevatedButton(
            onPressed: save,
            child: const Text('Simpan'),
          ),
        ],
      ),
    );
  }
}
```

Form yang baik:

- Memberi pesan error yang jelas.
- Tidak membuat user menebak.
- Mencegah submit saat data belum valid.
- Membersihkan controller dengan `dispose`.

---

## 10. Navigasi dengan Named Routes

Untuk aplikasi kecil, `MaterialPageRoute` sudah cukup. Untuk aplikasi yang mulai punya banyak halaman, named routes bisa membantu.

```dart
class AppRoutes {
  static const home = '/';
  static const taskForm = '/task-form';
  static const settings = '/settings';
}
```

Di `MaterialApp`:

```dart
MaterialApp(
  initialRoute: AppRoutes.home,
  routes: {
    AppRoutes.home: (context) => const TaskListPage(),
    AppRoutes.taskForm: (context) => const TaskFormPage(),
    AppRoutes.settings: (context) => const SettingsPage(),
  },
)
```

Membuka halaman:

```dart
Navigator.pushNamed(context, AppRoutes.taskForm);
```

Kelebihan:

- Nama route lebih konsisten.
- Navigasi lebih mudah dilacak.
- Cocok untuk project yang mulai banyak halaman.

Untuk aplikasi besar, kamu bisa belajar router package seperti `go_router`.

---

## 11. Local Storage dan Cache Sederhana

Local storage dipakai untuk menyimpan data di device.

Contoh kebutuhan:

- Status login.
- Preferensi theme.
- Data cache kecil.
- Draft form.

Gunakan penyimpanan sesuai kebutuhan:

- `shared_preferences`: data kecil dan sederhana.
- secure storage: data sensitif seperti token.
- SQLite/Hive/Isar: data lokal yang lebih kompleks.

Contoh cache sederhana:

```dart
class SettingsRepository {
  Future<void> saveDarkMode(bool value) async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool('dark_mode', value);
  }

  Future<bool> getDarkMode() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool('dark_mode') ?? false;
  }
}
```

Catatan penting:

- Jangan simpan password langsung.
- Jangan menganggap cache selalu benar.
- Tetap siapkan fallback jika data lokal rusak atau kosong.

---

## 12. API CRUD Sederhana

CRUD adalah:

- Create: membuat data.
- Read: membaca data.
- Update: mengubah data.
- Delete: menghapus data.

Contoh kontrak repository:

```dart
abstract class TaskRepository {
  Future<List<Task>> getTasks();
  Future<Task> createTask(Task task);
  Future<Task> updateTask(Task task);
  Future<void> deleteTask(int id);
}
```

Kenapa membuat kontrak seperti ini?

- Lebih jelas fitur data yang tersedia.
- Mudah membuat versi fake untuk testing.
- UI tidak bergantung langsung pada API.

Contoh alur create:

```text
User isi form -> validasi -> repository.createTask -> API POST -> refresh list
```

Contoh alur delete:

```text
User tap delete -> konfirmasi -> repository.deleteTask -> API DELETE -> hapus dari list
```

Selalu tangani:

- Loading saat request berjalan.
- Error saat gagal.
- Empty state setelah data kosong.
- Feedback sukses seperti SnackBar.

---

## 13. Theme, Dark Mode, dan Design System Kecil

Design system kecil membantu UI tetap konsisten.

Contoh file warna:

```dart
class AppColors {
  static const primary = Color(0xFF02569B);
  static const success = Color(0xFF22C55E);
  static const danger = Color(0xFFEF4444);
}
```

Contoh theme:

```dart
ThemeData lightTheme() {
  return ThemeData(
    colorScheme: ColorScheme.fromSeed(
      seedColor: AppColors.primary,
    ),
    useMaterial3: true,
    inputDecorationTheme: const InputDecorationTheme(
      border: OutlineInputBorder(),
    ),
  );
}
```

Untuk dark mode:

```dart
MaterialApp(
  theme: lightTheme(),
  darkTheme: darkTheme(),
  themeMode: ThemeMode.system,
)
```

Tips:

- Simpan warna utama di satu tempat.
- Buat style button dan input konsisten.
- Hindari warna hardcode bertebaran di banyak widget.

---

## 14. Error Handling yang Enak untuk User

Error tidak boleh hanya muncul di console.

Contoh error buruk:

```text
Exception: failed request
```

Contoh error yang lebih ramah:

```text
Gagal mengambil data. Periksa koneksi internet lalu coba lagi.
```

Buat mapper error:

```dart
String mapErrorMessage(Object error) {
  final message = error.toString();

  if (message.contains('SocketException')) {
    return 'Tidak ada koneksi internet';
  }

  if (message.contains('timeout')) {
    return 'Request terlalu lama. Coba lagi nanti';
  }

  return 'Terjadi kesalahan. Silakan coba lagi';
}
```

UI error yang baik biasanya punya:

- Pesan singkat.
- Tombol coba lagi.
- Tidak menyalahkan user.
- Tidak menampilkan stack trace.

---

## 15. Testing Dasar

Testing membantu memastikan fitur tetap berjalan setelah kode berubah.

Jenis test:

- Unit test: mengetes function atau class kecil.
- Widget test: mengetes tampilan widget.
- Integration test: mengetes alur aplikasi.

Contoh unit test sederhana:

```dart
bool isValidTitle(String value) {
  return value.trim().length >= 3;
}
```

Test:

```dart
void main() {
  test('title minimal 3 karakter', () {
    expect(isValidTitle('ab'), false);
    expect(isValidTitle('abc'), true);
  });
}
```

Jalankan:

```bash
flutter test
```

Mulai dari test kecil:

- Validator form.
- JSON parsing model.
- Repository fake.
- Widget empty state.

---

## 16. Build dan Persiapan Publish

Sebelum publish, cek:

- App name.
- App icon.
- Splash screen.
- Version number.
- Permission Android/iOS.
- Internet permission jika memakai API.
- Build release.

Build Android APK:

```bash
flutter build apk --release
```

Build Android App Bundle:

```bash
flutter build appbundle --release
```

Build iOS:

```bash
flutter build ios --release
```

Checklist sebelum rilis:

- Tidak ada debug banner.
- Tidak ada print sensitif.
- Error state sudah ramah.
- Loading state jelas.
- Aplikasi dites di device fisik.
- Form tidak bisa submit data kosong.
- App icon dan nama sudah benar.

---

## 17. Mini Project Lanjutan: Task Manager

Setelah aplikasi catatan belajar, buat project lanjutan: **Task Manager**.

Fitur utama:

- Menampilkan daftar task.
- Menambahkan task.
- Mengedit task.
- Menghapus task.
- Menandai task selesai.
- Filter task: semua, aktif, selesai.
- Simpan data lokal.
- Empty state.
- Error state.
- Theme sederhana.

Struktur fitur:

```text
features/tasks/
  models/task.dart
  data/task_repository.dart
  pages/task_list_page.dart
  pages/task_form_page.dart
  widgets/task_card.dart
  widgets/task_filter_bar.dart
```

Tahap pengerjaan:

1. Buat model `Task`.
2. Buat halaman list task.
3. Buat form tambah task.
4. Tambahkan edit task.
5. Tambahkan delete dengan dialog konfirmasi.
6. Tambahkan toggle selesai.
7. Tambahkan filter.
8. Simpan data lokal.
9. Rapikan theme.
10. Tambahkan test kecil.

Contoh model:

```dart
class Task {
  final String id;
  final String title;
  final String description;
  final bool isDone;

  const Task({
    required this.id,
    required this.title,
    required this.description,
    required this.isDone,
  });

  Task copyWith({
    String? title,
    String? description,
    bool? isDone,
  }) {
    return Task(
      id: id,
      title: title ?? this.title,
      description: description ?? this.description,
      isDone: isDone ?? this.isDone,
    );
  }
}
```

Kenapa `copyWith` penting?

- Membuat object baru tanpa mengubah object lama.
- Cocok untuk state management.
- Lebih aman untuk data immutable.

---

## 18. Roadmap Setelah Materi Ini

Setelah memahami materi lanjutan, lanjutkan ke:

1. State management pilihan
   - Riverpod
   - Bloc/Cubit
   - Provider lebih dalam

2. Arsitektur
   - Repository pattern
   - Clean architecture dasar
   - Dependency injection
   - Feature-first folder structure

3. Networking lebih kuat
   - Interceptor
   - Token refresh
   - Timeout
   - Retry
   - Pagination

4. Database lokal
   - SQLite
   - Hive
   - Isar
   - Offline-first app

5. UI lanjutan
   - Animation
   - CustomPaint
   - Responsive layout
   - Adaptive UI Android/iOS

6. Testing dan CI
   - Unit test
   - Widget test
   - Integration test
   - GitHub Actions

7. Production readiness
   - Crash reporting
   - Analytics
   - Logging
   - Performance profiling
   - App signing

---

## Checklist Penguasaan Lanjutan

- [ ] Bisa memisahkan page, widget, model, repository, dan service.
- [ ] Bisa membuat model dengan `fromJson` dan `toJson`.
- [ ] Bisa menangani loading, empty, error, dan success state.
- [ ] Bisa membuat form dengan `Form` dan `TextFormField`.
- [ ] Bisa memakai named routes.
- [ ] Bisa menyimpan preferensi sederhana.
- [ ] Bisa membuat alur CRUD sederhana.
- [ ] Bisa membuat theme kecil yang konsisten.
- [ ] Bisa menampilkan pesan error yang ramah.
- [ ] Bisa menulis unit test sederhana.
- [ ] Bisa menjalankan `flutter test`.
- [ ] Bisa build APK atau App Bundle release.
- [ ] Bisa membuat mini project Task Manager.

Jika checklist ini sudah banyak terpenuhi, kamu sudah siap masuk ke topik Flutter intermediate yang lebih serius.

---

## Penutup

Belajar Flutter lanjutan bukan berarti langsung memakai arsitektur yang rumit. Mulailah dari kebiasaan kecil: pecah widget, rapikan folder, pisahkan data layer, tangani semua state layar, dan buat error message yang manusiawi.

Jika materi dasar membuat kamu bisa membangun layar, materi lanjutan ini membuat kamu bisa membangun aplikasi yang lebih tahan tumbuh.
