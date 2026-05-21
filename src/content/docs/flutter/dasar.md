---
title: "Tutorial Flutter Dasar untuk Pemula"
description: "Materi fondasi Flutter: setup, Dart dasar, widget, layout, state, navigasi, form, API, storage, dan mini project catatan belajar."
category: "Flutter"
level: "Beginner"
order: 10
tags: ["flutter", "dart", "widget", "state", "pemula"]
updated: "2026-05-20"
---

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

Flutter menggunakan Dart. Sebelum masuk terlalu jauh ke widget, layout, dan state, pahami dulu cara Dart menyimpan data, membuat fungsi, mengelola kumpulan data, membuat object, dan menangani nilai kosong.

Bayangkan Dart sebagai bahasa yang dipakai untuk menulis logika aplikasi. Flutter adalah alat untuk menggambar UI, sedangkan Dart adalah bahasa untuk menentukan data apa yang ditampilkan, apa yang terjadi ketika tombol ditekan, dan bagaimana aplikasi mengambil keputusan.

### Variable

Variable adalah tempat menyimpan data. Data bisa berupa teks, angka, benar atau salah, daftar, object, dan nilai lain.

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

Penjelasan tipe data:

- `String`: menyimpan teks, misalnya nama, email, alamat, atau judul.
- `int`: menyimpan angka bulat, misalnya umur, jumlah item, atau nomor halaman.
- `double`: menyimpan angka desimal, misalnya harga, tinggi badan, atau rating.
- `bool`: menyimpan nilai `true` atau `false`, misalnya status login.

Contoh penggunaan di Flutter:

```dart
final String title = 'Profil User';
final int totalNotification = 3;
final bool isLoggedIn = true;
```

Data seperti ini biasanya dipakai untuk menentukan tampilan:

```dart
Text(title)
```

Atau menentukan kondisi:

```dart
if (isLoggedIn) {
  print('Tampilkan halaman dashboard');
} else {
  print('Tampilkan halaman login');
}
```

Hal yang perlu diingat:

- Nama variable sebaiknya jelas, misalnya `userName`, bukan `x`.
- Gunakan gaya `camelCase`, misalnya `totalPrice`, `isLoading`, dan `selectedIndex`.
- Jangan menyimpan semua data sebagai `String`. Jika data berupa angka, gunakan `int` atau `double`.

### `var`, `final`, dan `const`

Di Dart, ada beberapa cara membuat variable. Yang paling sering dipakai adalah `var`, `final`, dan `const`.

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

Contoh yang sering dipakai di Flutter:

```dart
class ProfilePage extends StatelessWidget {
  const ProfilePage({super.key});

  @override
  Widget build(BuildContext context) {
    final userName = 'Budi';

    return Scaffold(
      appBar: AppBar(
        title: const Text('Profil'),
      ),
      body: Text('Halo, $userName'),
    );
  }
}
```

Penjelasan:

- `const ProfilePage`: constructor bisa dibuat `const` karena tidak ada data runtime yang berubah.
- `final userName`: nilai dibuat saat `build()` berjalan dan tidak diubah lagi.
- `const Text('Profil')`: teksnya tetap, jadi aman dibuat `const`.

Kesalahan umum pemula:

```dart
final name = 'Budi';
name = 'Andi'; // error
```

`final` hanya boleh diisi sekali. Jika ingin nilainya bisa berubah, gunakan variable biasa:

```dart
var name = 'Budi';
name = 'Andi';
```

Namun di Flutter, biasakan memakai `final` jika data tidak perlu diubah. Kode jadi lebih aman dan mudah dibaca.

### Function

Function adalah blok kode yang bisa dipanggil ulang. Function membuat kode lebih rapi karena logika yang sering dipakai tidak perlu ditulis berkali-kali.

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

Penjelasan:

- `int tambah(int a, int b)`: function bernama `tambah`, menerima dua angka, dan mengembalikan `int`.
- `void sapa(String nama)`: function tidak mengembalikan nilai, hanya menjalankan perintah.
- `=>`: arrow function, cocok untuk function pendek satu baris.

Contoh function untuk format harga:

```dart
String formatRupiah(int harga) {
  return 'Rp $harga';
}

void main() {
  final result = formatRupiah(50000);
  print(result); // Rp 50000
}
```

Contoh function dengan parameter opsional:

```dart
String buatSapaan(String nama, {String waktu = 'pagi'}) {
  return 'Selamat $waktu, $nama';
}

void main() {
  print(buatSapaan('Rina'));
  print(buatSapaan('Budi', waktu: 'malam'));
}
```

Parameter di dalam `{}` disebut named parameter. Di Flutter, named parameter sangat sering dipakai:

```dart
Text(
  'Halo',
  style: TextStyle(
    fontSize: 20,
    fontWeight: FontWeight.bold,
  ),
)
```

Tips:

- Function sebaiknya melakukan satu tugas yang jelas.
- Nama function biasanya memakai kata kerja, misalnya `getUser`, `saveNote`, `formatDate`, atau `calculateTotal`.
- Jika function menghasilkan nilai, tentukan tipe return-nya agar kode mudah dipahami.

### List

`List` adalah kumpulan data berurutan. List cocok untuk data yang jumlahnya lebih dari satu, misalnya daftar produk, daftar user, daftar catatan, atau daftar menu.

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

Penjelasan:

- Index List dimulai dari `0`.
- `buah[0]` mengambil item pertama.
- `buah.length` menghitung jumlah item.
- `for (final item in buah)` digunakan untuk membaca semua item.

Contoh List dengan tipe data jelas:

```dart
final List<String> menu = [
  'Home',
  'Profile',
  'Settings',
];
```

Menambah dan menghapus data:

```dart
void main() {
  final notes = <String>[];

  notes.add('Belajar Dart');
  notes.add('Belajar Flutter');
  notes.remove('Belajar Dart');

  print(notes);
}
```

Mengubah List menjadi widget di Flutter:

```dart
final menus = ['Home', 'Profile', 'Settings'];

Column(
  children: menus.map((menu) {
    return Text(menu);
  }).toList(),
)
```

Untuk data yang banyak, gunakan `ListView.builder`:

```dart
final products = ['Laptop', 'Mouse', 'Keyboard'];

ListView.builder(
  itemCount: products.length,
  itemBuilder: (context, index) {
    final product = products[index];

    return ListTile(
      title: Text(product),
    );
  },
)
```

Kapan memakai List:

- Saat menampilkan data lebih dari satu.
- Saat data punya urutan.
- Saat data akan ditampilkan sebagai daftar di UI.

### Map

`Map` adalah kumpulan data berbentuk key dan value. Map cocok untuk data yang punya label, misalnya data user dari API.

```dart
void main() {
  final user = {
    'nama': 'Sari',
    'email': 'sari@example.com',
  };

  print(user['nama']);
}
```

Penjelasan:

- `'nama'` adalah key.
- `'Sari'` adalah value.
- `user['nama']` mengambil value dari key `nama`.

Contoh Map dengan tipe data:

```dart
final Map<String, dynamic> user = {
  'id': 1,
  'name': 'Sari',
  'email': 'sari@example.com',
  'isActive': true,
};
```

Kenapa memakai `dynamic`? Karena value di dalam Map bisa berbeda tipe: ada `int`, `String`, dan `bool`.

Mengambil data dari Map:

```dart
final name = user['name'];
final email = user['email'];

print(name);
print(email);
```

Contoh data seperti response API:

```dart
final Map<String, dynamic> response = {
  'status': 'success',
  'data': {
    'id': 7,
    'name': 'Rina',
  },
};

final data = response['data'] as Map<String, dynamic>;
print(data['name']);
```

Di Flutter, Map sering muncul saat membaca JSON:

```dart
factory User.fromJson(Map<String, dynamic> json) {
  return User(
    name: json['name'] as String,
    email: json['email'] as String,
  );
}
```

Kapan memakai Map:

- Saat data punya pasangan key dan value.
- Saat membaca response JSON.
- Saat membuat object dari data API.

### Class

Class adalah cetakan untuk membuat object. Jika Map menyimpan data secara bebas, Class membuat struktur data menjadi lebih jelas dan aman.

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

Penjelasan:

- `class User`: membuat tipe data baru bernama `User`.
- `final String nama`: property yang dimiliki User.
- `required this.nama`: saat membuat User, nilai `nama` wajib diisi.
- `user.nama`: mengambil nilai property dari object.

Contoh class untuk produk:

```dart
class Product {
  final int id;
  final String name;
  final int price;
  final bool isAvailable;

  const Product({
    required this.id,
    required this.name,
    required this.price,
    required this.isAvailable,
  });
}
```

Membuat object dari class:

```dart
void main() {
  const product = Product(
    id: 1,
    name: 'Keyboard',
    price: 250000,
    isAvailable: true,
  );

  print(product.name);
  print(product.price);
}
```

Class juga bisa punya function di dalamnya. Function di dalam class disebut method.

```dart
class Product {
  final String name;
  final int price;

  const Product({
    required this.name,
    required this.price,
  });

  String formattedPrice() {
    return 'Rp $price';
  }
}

void main() {
  const product = Product(
    name: 'Mouse',
    price: 150000,
  );

  print(product.formattedPrice());
}
```

Contoh class untuk data dari API:

```dart
class User {
  final int id;
  final String name;
  final String email;

  const User({
    required this.id,
    required this.name,
    required this.email,
  });

  factory User.fromJson(Map<String, dynamic> json) {
    return User(
      id: json['id'] as int,
      name: json['name'] as String,
      email: json['email'] as String,
    );
  }
}
```

Kapan memakai Class:

- Saat data punya struktur tetap.
- Saat ingin kode lebih aman daripada memakai Map langsung.
- Saat membuat model seperti `User`, `Product`, `Note`, `Post`, atau `Task`.

### Null Safety

Dart mendukung null safety. Artinya, variable tidak boleh bernilai `null` kecuali kita izinkan. Fitur ini membantu mengurangi error yang sering terjadi karena data kosong.

```dart
String nama = 'Andi';
String? alamat;

print(nama);
print(alamat);
```

Tanda `?` berarti variable boleh `null`.

Contoh:

```dart
String name = 'Budi';
String? phone;
```

Penjelasan:

- `name` wajib punya nilai `String`.
- `phone` boleh punya nilai `String` atau `null`.

Mengakses nilai nullable harus hati-hati:

```dart
void main() {
  String? phone;

  print(phone?.length);
}
```

Tanda `?.` berarti akses property hanya jika nilainya tidak `null`. Jika `phone` masih `null`, hasilnya juga `null`, bukan error.

Memberi nilai default dengan `??`:

```dart
void main() {
  String? name;

  final displayName = name ?? 'Guest';
  print(displayName);
}
```

Jika `name` null, maka `displayName` berisi `'Guest'`.

Memastikan nilai tidak null dengan `!`:

```dart
void main() {
  String? email = 'rina@example.com';

  print(email!.length);
}
```

Tanda `!` berarti kita yakin nilainya tidak null. Gunakan dengan hati-hati. Jika ternyata nilainya `null`, aplikasi bisa error.

Contoh di Flutter:

```dart
class ProfilePage extends StatelessWidget {
  final String? userName;

  const ProfilePage({
    super.key,
    this.userName,
  });

  @override
  Widget build(BuildContext context) {
    return Text(userName ?? 'User belum login');
  }
}
```

Kapan memakai nullable:

- Data belum tentu ada, misalnya foto profil user.
- Data masih menunggu dari API.
- Input boleh dikosongkan.

Ringkasan operator null safety:

| Operator | Fungsi | Contoh |
| --- | --- | --- |
| `?` | Mengizinkan nilai null | `String? name` |
| `?.` | Akses aman jika tidak null | `user?.name` |
| `??` | Nilai cadangan jika null | `name ?? 'Guest'` |
| `!` | Paksa dianggap tidak null | `name!` |

Latihan kecil:

```dart
class Note {
  final String title;
  final String? description;

  const Note({
    required this.title,
    this.description,
  });
}

void main() {
  const note = Note(
    title: 'Belajar Dart',
  );

  print(note.title);
  print(note.description ?? 'Tidak ada deskripsi');
}
```

Jika sudah paham variable, function, List, Map, Class, dan Null Safety, materi Flutter berikutnya akan jauh lebih mudah karena widget Flutter juga dibangun dengan pola yang sama: property, function, object, dan data yang bisa berubah.

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
