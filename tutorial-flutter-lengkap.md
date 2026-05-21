# Tutorial Flutter Dasar untuk Pemula

Panduan ini dibuat untuk developer yang sedang belajar Flutter dari nol sampai bisa membuat aplikasi sederhana. Fokusnya bukan hanya "copy paste jalan", tetapi memahami pola pikir Flutter: UI dibangun dari widget, data berubah lewat state, dan aplikasi berkembang dari komponen kecil yang dirangkai.

## Daftar Isi

1. Apa itu Flutter
2. Persiapan alat
3. Membuat project pertama
4. Struktur folder Flutter
5. Dasar bahasa Dart
6. Konsep widget
7. Layout dasar
8. StatelessWidget dan StatefulWidget
9. State sederhana
10. Navigasi antar halaman
11. Input dan form
12. List dan data dinamis
13. Styling dan tema
14. Mengambil data dari API
15. Menyimpan data sederhana
16. Mini project: aplikasi catatan belajar
17. Debugging dan error umum
18. Roadmap belajar berikutnya

---

## 1. Apa itu Flutter

Flutter adalah framework dari Google untuk membuat aplikasi mobile, web, dan desktop dari satu codebase. Flutter memakai bahasa Dart.

Kelebihan Flutter:

- Bisa membuat aplikasi Android dan iOS dari satu project.
- UI cepat dibuat karena semuanya berbasis widget.
- Ada hot reload untuk melihat perubahan dengan cepat.
- Cocok untuk aplikasi sederhana sampai aplikasi produksi.
- Dokumentasi dan komunitasnya besar.

Hal penting yang perlu dipahami sejak awal:

- Di Flutter, hampir semua bagian UI adalah widget.
- Aplikasi dibuat dengan menyusun widget kecil menjadi tampilan besar.
- Ketika data berubah, Flutter menggambar ulang bagian UI yang perlu berubah.

---

## 2. Persiapan Alat

Alat yang dibutuhkan:

- Flutter SDK
- Android Studio atau Visual Studio Code
- Emulator Android, simulator iOS, atau device fisik
- Git

Setelah instalasi Flutter, cek dengan command:

```bash
flutter doctor
```

Jika ada tanda silang, baca pesan yang muncul. Biasanya masalah awal ada di:

- Android SDK belum terpasang.
- Lisensi Android belum diterima.
- Emulator belum dibuat.
- Path Flutter belum masuk environment variable.

Untuk menerima lisensi Android:

```bash
flutter doctor --android-licenses
```

Untuk melihat device yang tersedia:

```bash
flutter devices
```

---

## 3. Membuat Project Pertama

Buat project Flutter baru:

```bash
flutter create belajar_flutter
cd belajar_flutter
flutter run
```

Jika memakai VS Code:

1. Buka folder project.
2. Pilih device di pojok kanan bawah.
3. Tekan `F5` atau jalankan `flutter run` dari terminal.

Saat aplikasi berjalan, coba ubah teks di file `lib/main.dart`, lalu tekan save. Flutter akan melakukan hot reload.

---

## 4. Struktur Folder Flutter

Struktur dasar project Flutter:

```text
belajar_flutter/
  android/
  ios/
  lib/
    main.dart
  test/
  pubspec.yaml
```

Penjelasan:

- `lib/`: tempat utama menulis kode Dart.
- `lib/main.dart`: entry point aplikasi.
- `android/`: konfigurasi native Android.
- `ios/`: konfigurasi native iOS.
- `test/`: tempat menulis test.
- `pubspec.yaml`: konfigurasi project, dependency, asset, font, dan versi aplikasi.

Untuk pemula, paling sering bekerja di:

- `lib/main.dart`
- folder baru di dalam `lib/`, misalnya `pages/`, `widgets/`, `models/`, dan `services/`
- `pubspec.yaml`

---

## 5. Dasar Bahasa Dart

Flutter menggunakan Dart. Berikut dasar yang perlu dikuasai.

### Variable

```dart
void main() {
  String nama = 'Budi';
  int umur = 20;
  double tinggi = 170.5;
  bool sudahLogin = true;

  print(nama);
  print(umur);
  print(tinggi);
  print(sudahLogin);
}
```

### `var`, `final`, dan `const`

```dart
void main() {
  var kota = 'Jakarta';
  final tanggalLogin = DateTime.now();
  const appName = 'Belajar Flutter';
}
```

Bedanya:

- `var`: tipe data otomatis ditebak dari nilai awal.
- `final`: hanya bisa diisi sekali, nilainya bisa baru diketahui saat runtime.
- `const`: nilai tetap dan harus diketahui saat compile time.

Gunakan `final` untuk nilai yang tidak berubah setelah dibuat. Gunakan `const` untuk nilai yang benar-benar tetap.

### Function

```dart
int tambah(int a, int b) {
  return a + b;
}

void sapa(String nama) {
  print('Halo, $nama');
}
```

Jika function hanya satu baris:

```dart
int kali(int a, int b) => a * b;
```

### List

```dart
void main() {
  final buah = ['Apel', 'Jeruk', 'Mangga'];

  print(buah[0]);
  print(buah.length);

  for (final item in buah) {
    print(item);
  }
}
```

### Map

```dart
void main() {
  final user = {
    'nama': 'Sari',
    'email': 'sari@example.com',
  };

  print(user['nama']);
}
```

### Class

```dart
class User {
  final String nama;
  final String email;

  User({
    required this.nama,
    required this.email,
  });
}

void main() {
  final user = User(
    nama: 'Rina',
    email: 'rina@example.com',
  );

  print(user.nama);
}
```

### Null Safety

Dart mendukung null safety. Artinya, variable tidak boleh bernilai `null` kecuali kita izinkan.

```dart
String nama = 'Andi';
String? alamat;

print(nama);
print(alamat);
```

Tanda `?` berarti variable boleh `null`.

---

## 6. Konsep Widget

Widget adalah blok penyusun UI di Flutter. Contoh widget:

- `Text`
- `Container`
- `Column`
- `Row`
- `Image`
- `Scaffold`
- `AppBar`
- `ElevatedButton`
- `TextField`

Contoh aplikasi paling sederhana:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return const MaterialApp(
      home: Scaffold(
        body: Center(
          child: Text('Halo Flutter'),
        ),
      ),
    );
  }
}
```

Penjelasan:

- `main()` adalah function pertama yang dijalankan.
- `runApp()` menjalankan aplikasi Flutter.
- `MaterialApp` memberi struktur aplikasi Material Design.
- `Scaffold` memberi kerangka halaman seperti app bar, body, drawer, dan floating button.
- `Center` membuat child berada di tengah.
- `Text` menampilkan teks.

---

## 7. Layout Dasar

Layout Flutter dibuat dengan widget.

### Column

`Column` menyusun widget dari atas ke bawah.

```dart
Column(
  mainAxisAlignment: MainAxisAlignment.center,
  children: const [
    Text('Judul'),
    Text('Deskripsi'),
  ],
)
```

### Row

`Row` menyusun widget dari kiri ke kanan.

```dart
Row(
  mainAxisAlignment: MainAxisAlignment.spaceBetween,
  children: const [
    Text('Kiri'),
    Text('Kanan'),
  ],
)
```

### Container

`Container` sering dipakai untuk memberi ukuran, padding, margin, warna, dan border.

```dart
Container(
  padding: const EdgeInsets.all(16),
  margin: const EdgeInsets.all(12),
  decoration: BoxDecoration(
    color: Colors.blue,
    borderRadius: BorderRadius.circular(8),
  ),
  child: const Text(
    'Kotak biru',
    style: TextStyle(color: Colors.white),
  ),
)
```

### Padding

```dart
const Padding(
  padding: EdgeInsets.all(16),
  child: Text('Teks dengan jarak'),
)
```

### Expanded

`Expanded` membuat widget mengisi ruang kosong yang tersedia.

```dart
Row(
  children: [
    Expanded(
      child: Container(height: 80, color: Colors.red),
    ),
    Expanded(
      child: Container(height: 80, color: Colors.green),
    ),
  ],
)
```

---

## 8. StatelessWidget dan StatefulWidget

### StatelessWidget

Gunakan `StatelessWidget` jika UI tidak punya data yang berubah dari dalam widget itu sendiri.

```dart
class ProfileCard extends StatelessWidget {
  const ProfileCard({super.key});

  @override
  Widget build(BuildContext context) {
    return const Card(
      child: Padding(
        padding: EdgeInsets.all(16),
        child: Text('Nama: Dinda'),
      ),
    );
  }
}
```

### StatefulWidget

Gunakan `StatefulWidget` jika UI perlu berubah, misalnya counter, checkbox, form, tab, loading, atau data API.

```dart
class CounterPage extends StatefulWidget {
  const CounterPage({super.key});

  @override
  State<CounterPage> createState() => _CounterPageState();
}

class _CounterPageState extends State<CounterPage> {
  int count = 0;

  void increment() {
    setState(() {
      count++;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Counter')),
      body: Center(
        child: Text('Nilai: $count'),
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: increment,
        child: const Icon(Icons.add),
      ),
    );
  }
}
```

`setState()` memberi tahu Flutter bahwa data berubah dan UI perlu digambar ulang.

---

## 9. State Sederhana

Contoh mengganti teks saat tombol ditekan:

```dart
class GreetingPage extends StatefulWidget {
  const GreetingPage({super.key});

  @override
  State<GreetingPage> createState() => _GreetingPageState();
}

class _GreetingPageState extends State<GreetingPage> {
  String message = 'Selamat datang';

  void changeMessage() {
    setState(() {
      message = 'Kamu berhasil menekan tombol';
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('State Sederhana')),
      body: Center(
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Text(message),
            const SizedBox(height: 16),
            ElevatedButton(
              onPressed: changeMessage,
              child: const Text('Ubah Teks'),
            ),
          ],
        ),
      ),
    );
  }
}
```

Pola penting:

1. Simpan data sebagai variable di class `State`.
2. Ubah data di dalam `setState()`.
3. Tampilkan data di method `build()`.

---

## 10. Navigasi Antar Halaman

Buat halaman pertama:

```dart
class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Home')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.push(
              context,
              MaterialPageRoute(
                builder: (context) => const DetailPage(),
              ),
            );
          },
          child: const Text('Buka Detail'),
        ),
      ),
    );
  }
}
```

Buat halaman kedua:

```dart
class DetailPage extends StatelessWidget {
  const DetailPage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Detail')),
      body: Center(
        child: ElevatedButton(
          onPressed: () {
            Navigator.pop(context);
          },
          child: const Text('Kembali'),
        ),
      ),
    );
  }
}
```

Konsep:

- `Navigator.push()` membuka halaman baru.
- `Navigator.pop()` kembali ke halaman sebelumnya.

---

## 11. Input dan Form

Untuk membaca input teks, gunakan `TextEditingController`.

```dart
class LoginPage extends StatefulWidget {
  const LoginPage({super.key});

  @override
  State<LoginPage> createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final emailController = TextEditingController();
  final passwordController = TextEditingController();

  @override
  void dispose() {
    emailController.dispose();
    passwordController.dispose();
    super.dispose();
  }

  void login() {
    final email = emailController.text;
    final password = passwordController.text;

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('Login sebagai $email')),
    );

    print('Email: $email');
    print('Password: $password');
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Login')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          children: [
            TextField(
              controller: emailController,
              decoration: const InputDecoration(
                labelText: 'Email',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 12),
            TextField(
              controller: passwordController,
              obscureText: true,
              decoration: const InputDecoration(
                labelText: 'Password',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: ElevatedButton(
                onPressed: login,
                child: const Text('Login'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

Jangan lupa `dispose()` controller agar resource dibersihkan saat widget tidak dipakai lagi.

---

## 12. List dan Data Dinamis

Jika data sedikit, bisa pakai `Column`. Jika data banyak, gunakan `ListView.builder`.

```dart
class ProductListPage extends StatelessWidget {
  const ProductListPage({super.key});

  @override
  Widget build(BuildContext context) {
    final products = [
      'Laptop',
      'Keyboard',
      'Mouse',
      'Monitor',
      'Headset',
    ];

    return Scaffold(
      appBar: AppBar(title: const Text('Produk')),
      body: ListView.builder(
        itemCount: products.length,
        itemBuilder: (context, index) {
          final product = products[index];

          return ListTile(
            leading: CircleAvatar(
              child: Text('${index + 1}'),
            ),
            title: Text(product),
            subtitle: const Text('Stok tersedia'),
            trailing: const Icon(Icons.chevron_right),
            onTap: () {
              ScaffoldMessenger.of(context).showSnackBar(
                SnackBar(content: Text('Pilih $product')),
              );
            },
          );
        },
      ),
    );
  }
}
```

Gunakan `ListView.builder` karena item dibuat sesuai kebutuhan, sehingga lebih efisien untuk data panjang.

---

## 13. Styling dan Tema

Daripada mengatur warna satu per satu di banyak tempat, gunakan theme.

```dart
class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Belajar Flutter',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
        appBarTheme: const AppBarTheme(
          centerTitle: true,
        ),
        inputDecorationTheme: const InputDecorationTheme(
          border: OutlineInputBorder(),
        ),
      ),
      home: const HomePage(),
    );
  }
}
```

Contoh styling teks:

```dart
Text(
  'Belajar Flutter',
  style: Theme.of(context).textTheme.headlineMedium?.copyWith(
        fontWeight: FontWeight.bold,
      ),
)
```

Tips:

- Gunakan `Theme.of(context)` agar style konsisten.
- Hindari hardcode warna terlalu banyak.
- Pakai `SizedBox` untuk jarak sederhana.
- Pakai `Padding` untuk memberi ruang di sekitar konten.

---

## 14. Mengambil Data dari API

Tambahkan dependency `http` di `pubspec.yaml`:

```yaml
dependencies:
  flutter:
    sdk: flutter
  http: ^1.2.0
```

Lalu jalankan:

```bash
flutter pub get
```

Contoh model:

```dart
class Post {
  final int id;
  final String title;
  final String body;

  Post({
    required this.id,
    required this.title,
    required this.body,
  });

  factory Post.fromJson(Map<String, dynamic> json) {
    return Post(
      id: json['id'] as int,
      title: json['title'] as String,
      body: json['body'] as String,
    );
  }
}
```

Contoh fetch API:

```dart
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

class PostPage extends StatefulWidget {
  const PostPage({super.key});

  @override
  State<PostPage> createState() => _PostPageState();
}

class _PostPageState extends State<PostPage> {
  late Future<List<Post>> postsFuture;

  @override
  void initState() {
    super.initState();
    postsFuture = fetchPosts();
  }

  Future<List<Post>> fetchPosts() async {
    final response = await http.get(
      Uri.parse('https://jsonplaceholder.typicode.com/posts'),
    );

    if (response.statusCode != 200) {
      throw Exception('Gagal mengambil data');
    }

    final List<dynamic> jsonList = jsonDecode(response.body) as List<dynamic>;

    return jsonList
        .map((item) => Post.fromJson(item as Map<String, dynamic>))
        .toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Post')),
      body: FutureBuilder<List<Post>>(
        future: postsFuture,
        builder: (context, snapshot) {
          if (snapshot.connectionState == ConnectionState.waiting) {
            return const Center(child: CircularProgressIndicator());
          }

          if (snapshot.hasError) {
            return Center(child: Text('Error: ${snapshot.error}'));
          }

          final posts = snapshot.data ?? [];

          return ListView.builder(
            itemCount: posts.length,
            itemBuilder: (context, index) {
              final post = posts[index];

              return ListTile(
                title: Text(post.title),
                subtitle: Text(post.body),
              );
            },
          );
        },
      ),
    );
  }
}
```

Konsep penting:

- `Future` mewakili data yang datang nanti.
- `async` dan `await` dipakai untuk operasi asynchronous.
- `FutureBuilder` membantu menampilkan UI berdasarkan status data.

---

## 15. Menyimpan Data Sederhana

Untuk menyimpan data kecil seperti token, theme, atau preference user, gunakan package `shared_preferences`.

Tambahkan dependency:

```yaml
dependencies:
  flutter:
    sdk: flutter
  shared_preferences: ^2.2.0
```

Simpan data:

```dart
import 'package:shared_preferences/shared_preferences.dart';

Future<void> saveName(String name) async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.setString('name', name);
}
```

Ambil data:

```dart
import 'package:shared_preferences/shared_preferences.dart';

Future<String?> getName() async {
  final prefs = await SharedPreferences.getInstance();
  return prefs.getString('name');
}
```

Hapus data:

```dart
import 'package:shared_preferences/shared_preferences.dart';

Future<void> removeName() async {
  final prefs = await SharedPreferences.getInstance();
  await prefs.remove('name');
}
```

Catatan:

- `shared_preferences` cocok untuk data kecil.
- Jangan simpan password langsung di `shared_preferences`.
- Untuk data sensitif, pelajari secure storage.
- Untuk data kompleks, pelajari SQLite, Hive, Isar, atau database lain.

---

## 16. Mini Project: Aplikasi Catatan Belajar

Di bagian ini kita membuat aplikasi catatan sederhana. Fitur:

- Menampilkan daftar catatan.
- Menambahkan catatan.
- Menghapus catatan.
- State masih disimpan di memory, jadi data hilang saat aplikasi ditutup.

Ganti isi `lib/main.dart` dengan kode berikut:

```dart
import 'package:flutter/material.dart';

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Catatan Belajar',
      theme: ThemeData(
        colorScheme: ColorScheme.fromSeed(seedColor: Colors.teal),
        useMaterial3: true,
      ),
      home: const NotePage(),
    );
  }
}

class Note {
  final String title;
  final String description;

  Note({
    required this.title,
    required this.description,
  });
}

class NotePage extends StatefulWidget {
  const NotePage({super.key});

  @override
  State<NotePage> createState() => _NotePageState();
}

class _NotePageState extends State<NotePage> {
  final notes = <Note>[
    Note(
      title: 'Belajar Widget',
      description: 'Pahami Text, Container, Row, dan Column.',
    ),
    Note(
      title: 'Belajar State',
      description: 'Latihan setState dengan counter sederhana.',
    ),
  ];

  void openAddNotePage() async {
    final result = await Navigator.push<Note>(
      context,
      MaterialPageRoute(
        builder: (context) => const AddNotePage(),
      ),
    );

    if (result == null) return;

    setState(() {
      notes.add(result);
    });
  }

  void deleteNote(int index) {
    final deletedNote = notes[index];

    setState(() {
      notes.removeAt(index);
    });

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(content: Text('${deletedNote.title} dihapus')),
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Catatan Belajar'),
      ),
      body: notes.isEmpty
          ? const Center(
              child: Text('Belum ada catatan'),
            )
          : ListView.separated(
              padding: const EdgeInsets.all(16),
              itemCount: notes.length,
              separatorBuilder: (context, index) => const SizedBox(height: 8),
              itemBuilder: (context, index) {
                final note = notes[index];

                return Card(
                  child: ListTile(
                    title: Text(note.title),
                    subtitle: Text(note.description),
                    trailing: IconButton(
                      icon: const Icon(Icons.delete_outline),
                      onPressed: () => deleteNote(index),
                    ),
                  ),
                );
              },
            ),
      floatingActionButton: FloatingActionButton(
        onPressed: openAddNotePage,
        child: const Icon(Icons.add),
      ),
    );
  }
}

class AddNotePage extends StatefulWidget {
  const AddNotePage({super.key});

  @override
  State<AddNotePage> createState() => _AddNotePageState();
}

class _AddNotePageState extends State<AddNotePage> {
  final titleController = TextEditingController();
  final descriptionController = TextEditingController();

  @override
  void dispose() {
    titleController.dispose();
    descriptionController.dispose();
    super.dispose();
  }

  void saveNote() {
    final title = titleController.text.trim();
    final description = descriptionController.text.trim();

    if (title.isEmpty || description.isEmpty) {
      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Judul dan deskripsi wajib diisi')),
      );
      return;
    }

    final note = Note(
      title: title,
      description: description,
    );

    Navigator.pop(context, note);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Tambah Catatan'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
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
              minLines: 3,
              maxLines: 5,
              decoration: const InputDecoration(
                labelText: 'Deskripsi',
                border: OutlineInputBorder(),
              ),
            ),
            const SizedBox(height: 16),
            SizedBox(
              width: double.infinity,
              child: FilledButton(
                onPressed: saveNote,
                child: const Text('Simpan'),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

Yang dipelajari dari mini project ini:

- Membuat model sederhana dengan class `Note`.
- Menampilkan list dengan `ListView.separated`.
- Menambah data dari halaman lain.
- Mengirim data balik dengan `Navigator.pop(context, data)`.
- Menghapus item dari list.
- Validasi input sederhana.
- Membersihkan controller dengan `dispose()`.

Latihan lanjutan:

1. Tambahkan fitur edit catatan.
2. Tambahkan konfirmasi sebelum menghapus catatan.
3. Simpan catatan memakai `shared_preferences`.
4. Pisahkan file menjadi `main.dart`, `note.dart`, `note_page.dart`, dan `add_note_page.dart`.
5. Tambahkan pencarian catatan.

---

## 17. Debugging dan Error Umum

### Error: `No connected devices`

Solusi:

- Jalankan emulator.
- Sambungkan device fisik.
- Aktifkan USB debugging di Android.
- Cek dengan `flutter devices`.

### Error: dependency belum terinstall

Solusi:

```bash
flutter pub get
```

### UI overflow kuning hitam

Biasanya karena widget terlalu besar untuk layar.

Solusi yang sering dipakai:

- Bungkus konten dengan `SingleChildScrollView`.
- Gunakan `Expanded` di dalam `Column` atau `Row`.
- Kurangi ukuran widget.
- Pastikan layout responsif.

Contoh:

```dart
SingleChildScrollView(
  child: Column(
    children: [
      Text('Konten panjang'),
    ],
  ),
)
```

### `setState() called after dispose()`

Biasanya terjadi ketika async process selesai setelah halaman ditutup.

Solusi:

```dart
if (!mounted) return;

setState(() {
  // ubah state
});
```

### Lupa dispose controller

Jika memakai `TextEditingController`, biasakan:

```dart
@override
void dispose() {
  controller.dispose();
  super.dispose();
}
```

### Hot reload tidak mengubah state awal

Hot reload mempertahankan state. Jika ingin reset total, gunakan hot restart.

---

## 18. Roadmap Belajar Berikutnya

Setelah menguasai dasar di tutorial ini, lanjutkan ke topik berikut:

1. Dart lebih dalam
   - null safety
   - async await
   - class dan inheritance
   - extension
   - collection method seperti `map`, `where`, dan `fold`

2. Flutter UI
   - layout responsif
   - custom widget
   - theme
   - dark mode
   - animation dasar

3. State management
   - `setState`
   - `ValueNotifier`
   - Provider
   - Riverpod
   - Bloc atau Cubit

4. Networking
   - REST API
   - JSON parsing
   - error handling
   - loading state
   - retry dan timeout

5. Local storage
   - shared preferences
   - secure storage
   - SQLite
   - Hive atau Isar

6. Arsitektur aplikasi
   - pemisahan folder
   - repository pattern
   - service layer
   - dependency injection
   - clean architecture dasar

7. Testing
   - unit test
   - widget test
   - integration test

8. Publish aplikasi
   - build APK
   - build App Bundle
   - konfigurasi icon
   - konfigurasi splash screen
   - upload ke Play Store

---

## Rekomendasi Cara Belajar

Belajar Flutter akan lebih cepat jika dilakukan bertahap:

1. Ketik ulang kode, jangan hanya membaca.
2. Jalankan setiap contoh kecil.
3. Ubah teks, warna, layout, dan data supaya paham efeknya.
4. Buat project mini setelah belajar satu konsep.
5. Biasakan membaca error dari atas ke bawah.
6. Jangan langsung lompat ke state management kompleks sebelum nyaman dengan `setState`.

Urutan latihan yang disarankan:

1. Counter sederhana.
2. Form login tanpa backend.
3. List produk statis.
4. Catatan sederhana.
5. Fetch data dari API.
6. Simpan data lokal.
7. Aplikasi CRUD sederhana.

---

## Checklist Penguasaan Dasar

Gunakan checklist ini untuk menilai progress:

- [ ] Bisa membuat project Flutter baru.
- [ ] Bisa menjalankan aplikasi di emulator atau device.
- [ ] Paham struktur folder dasar.
- [ ] Bisa membuat `StatelessWidget`.
- [ ] Bisa membuat `StatefulWidget`.
- [ ] Bisa memakai `setState`.
- [ ] Bisa membuat layout dengan `Column`, `Row`, `Container`, dan `Padding`.
- [ ] Bisa memakai `ListView.builder`.
- [ ] Bisa membaca input dari `TextField`.
- [ ] Bisa membuat navigasi antar halaman.
- [ ] Bisa membuat model class sederhana.
- [ ] Bisa mengambil data API dengan `http`.
- [ ] Bisa memakai `FutureBuilder`.
- [ ] Bisa menyimpan data sederhana.
- [ ] Bisa membaca dan memperbaiki error umum.

Jika sebagian besar checklist sudah terpenuhi, kamu sudah punya fondasi yang cukup kuat untuk lanjut ke project nyata.

---

## Penutup

Flutter terasa besar di awal karena banyak widget dan konsep baru. Namun pola dasarnya sederhana: buat widget, susun layout, simpan data sebagai state, ubah state saat user berinteraksi, lalu tampilkan hasilnya.

Mulailah dari aplikasi kecil. Setelah nyaman, tingkatkan perlahan dengan API, local storage, state management, dan arsitektur yang lebih rapi. Yang paling penting adalah sering membuat sesuatu, karena skill Flutter tumbuh dari latihan langsung.

---

# Bagian 2: Materi Flutter Lanjutan

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
