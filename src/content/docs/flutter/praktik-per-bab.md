---
title: "Praktik Flutter per Bab"
description: "Kumpulan latihan kecil, challenge, expected output, dan checklist setelah mempelajari materi Flutter dasar."
category: "Flutter"
level: "Practice"
order: 30
tags: ["flutter", "practice", "latihan", "challenge"]
updated: "2026-05-20"
---

# Praktik Flutter per Bab

Materi ini dibuat supaya belajar Flutter tidak berhenti di membaca teori. Setiap bagian berisi latihan kecil, challenge, expected output, dan checklist kemampuan.

Cara belajar yang disarankan:

1. Baca materi utama.
2. Ketik ulang contoh kode.
3. Ubah sedikit kode supaya paham alurnya.
4. Kerjakan challenge tanpa melihat jawaban.
5. Cocokkan hasil dengan expected output.

---

## 1. Praktik Dasar Bahasa Dart

Target:

- Bisa membuat variable.
- Bisa memakai `final` dan `const`.
- Bisa membuat function sederhana.
- Bisa memakai `List`, `Map`, `Class`, dan Null Safety.

### Latihan 1: Data Profil

Buat program Dart sederhana yang menyimpan data profil.

```dart
void main() {
  const appName = 'Belajar Flutter';
  final userName = 'Budi';
  final age = 21;
  final isActive = true;

  print(appName);
  print('Nama: $userName');
  print('Umur: $age');
  print('Aktif: $isActive');
}
```

Expected output:

```text
Belajar Flutter
Nama: Budi
Umur: 21
Aktif: true
```

Challenge:

- Tambahkan variable `email`.
- Tambahkan variable `city`.
- Tampilkan semua data dalam satu kalimat.

Checklist:

- [ ] Bisa membedakan `String`, `int`, dan `bool`.
- [ ] Bisa memakai string interpolation dengan `$variable`.
- [ ] Bisa memilih `final` untuk data yang tidak berubah.

---

## 2. Praktik Function

Target:

- Bisa membuat function dengan return value.
- Bisa membuat function dengan named parameter.
- Bisa memecah logika kecil menjadi function.

### Latihan 1: Format Harga

```dart
String formatRupiah(int price) {
  return 'Rp $price';
}

void main() {
  print(formatRupiah(25000));
  print(formatRupiah(150000));
}
```

Expected output:

```text
Rp 25000
Rp 150000
```

Challenge:

- Buat function `calculateTotal`.
- Parameter: `price` dan `quantity`.
- Return total harga.

Contoh:

```dart
int calculateTotal({
  required int price,
  required int quantity,
}) {
  return price * quantity;
}
```

Checklist:

- [ ] Bisa membuat function yang mengembalikan `String`.
- [ ] Bisa membuat function yang mengembalikan `int`.
- [ ] Bisa memakai named parameter dengan `required`.

---

## 3. Praktik List

Target:

- Bisa menyimpan banyak data.
- Bisa menampilkan semua item dengan loop.
- Bisa mengubah List menjadi widget.

### Latihan 1: Daftar Menu

```dart
void main() {
  final menus = ['Home', 'Profile', 'Settings'];

  for (final menu in menus) {
    print(menu);
  }
}
```

Expected output:

```text
Home
Profile
Settings
```

Contoh di Flutter:

```dart
final menus = ['Home', 'Profile', 'Settings'];

Column(
  children: menus.map((menu) {
    return Text(menu);
  }).toList(),
)
```

Challenge:

- Tambahkan menu `Help`.
- Tampilkan jumlah menu.
- Tampilkan menu pertama.

Checklist:

- [ ] Bisa membuat `List<String>`.
- [ ] Bisa membaca item berdasarkan index.
- [ ] Bisa melakukan loop dengan `for`.
- [ ] Bisa memakai `.map()` untuk membuat widget.

---

## 4. Praktik Map dan JSON

Target:

- Bisa membaca data key-value.
- Bisa memahami bentuk data dari API.
- Bisa mengubah Map menjadi object.

### Latihan 1: Data User

```dart
void main() {
  final Map<String, dynamic> user = {
    'id': 1,
    'name': 'Rina',
    'email': 'rina@example.com',
    'isActive': true,
  };

  print(user['name']);
  print(user['email']);
}
```

Expected output:

```text
Rina
rina@example.com
```

Challenge:

- Tambahkan key `phone`.
- Tampilkan `isActive`.
- Buat kalimat: `Rina aktif: true`.

Checklist:

- [ ] Bisa membuat `Map<String, dynamic>`.
- [ ] Bisa mengambil value dari key.
- [ ] Paham kenapa data API sering berbentuk Map.

---

## 5. Praktik Class Model

Target:

- Bisa membuat model data.
- Bisa memakai constructor.
- Bisa membuat object dari Map.

### Latihan 1: Model Note

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
    title: 'Belajar Flutter',
    description: 'Membuat UI dari widget kecil.',
  );

  print(note.title);
  print(note.description);
}
```

Expected output:

```text
Belajar Flutter
Membuat UI dari widget kecil.
```

Challenge:

- Tambahkan property `createdAt`.
- Buat 3 object `Note`.
- Simpan semua note ke dalam `List<Note>`.

Checklist:

- [ ] Bisa membuat class.
- [ ] Bisa membuat property `final`.
- [ ] Bisa memakai `required`.
- [ ] Bisa membuat object dari class.

---

## 6. Praktik Widget Dasar

Target:

- Bisa memakai `Text`, `Container`, `Column`, dan `Row`.
- Bisa memahami parent-child widget.
- Bisa membuat UI sederhana.

### Latihan 1: Kartu Profil

Buat tampilan profil sederhana.

```dart
Container(
  padding: const EdgeInsets.all(16),
  child: const Column(
    crossAxisAlignment: CrossAxisAlignment.start,
    children: [
      Text('Budi Santoso'),
      Text('Flutter Developer'),
      Text('Jakarta'),
    ],
  ),
)
```

Expected output:

- Nama tampil di baris pertama.
- Role tampil di baris kedua.
- Kota tampil di baris ketiga.

Challenge:

- Tambahkan warna background.
- Tambahkan jarak antar teks dengan `SizedBox`.
- Buat nama lebih besar dan tebal.

Checklist:

- [ ] Bisa menyusun widget secara vertikal dengan `Column`.
- [ ] Bisa memberi padding.
- [ ] Bisa styling teks.

---

## 7. Praktik State Sederhana

Target:

- Bisa memakai `StatefulWidget`.
- Bisa mengubah data dengan `setState`.
- Bisa memahami kenapa UI berubah saat state berubah.

### Latihan 1: Counter Manual

```dart
int counter = 0;

ElevatedButton(
  onPressed: () {
    setState(() {
      counter++;
    });
  },
  child: const Text('Tambah'),
)
```

Expected output:

- Saat tombol ditekan, angka bertambah.
- UI menampilkan nilai terbaru.

Challenge:

- Tambahkan tombol kurang.
- Tambahkan tombol reset.
- Jika angka `0`, tombol kurang tidak boleh mengurangi lagi.

Checklist:

- [ ] Bisa membuat variable state.
- [ ] Bisa memakai `setState`.
- [ ] Paham bahwa state adalah data yang memengaruhi tampilan.

---

## 8. Praktik Navigasi

Target:

- Bisa pindah halaman.
- Bisa membuat halaman detail.
- Bisa mengirim data sederhana ke halaman berikutnya.

### Latihan 1: Pindah ke Halaman Detail

```dart
Navigator.push(
  context,
  MaterialPageRoute(
    builder: (context) => const DetailPage(),
  ),
);
```

Challenge:

- Buat halaman `HomePage`.
- Buat halaman `DetailPage`.
- Dari `HomePage`, kirim judul ke `DetailPage`.

Checklist:

- [ ] Bisa memakai `Navigator.push`.
- [ ] Bisa memakai `Navigator.pop`.
- [ ] Bisa mengirim data lewat constructor halaman.

---

## 9. Praktik Form

Target:

- Bisa membaca input user.
- Bisa memakai `TextEditingController`.
- Bisa melakukan validasi sederhana.

### Latihan 1: Input Nama

```dart
final nameController = TextEditingController();

TextField(
  controller: nameController,
  decoration: const InputDecoration(
    labelText: 'Nama',
  ),
)
```

Challenge:

- Tambahkan input email.
- Jika nama kosong, tampilkan pesan error.
- Jika email kosong, tampilkan pesan error.

Checklist:

- [ ] Bisa membuat controller.
- [ ] Bisa membaca nilai input.
- [ ] Bisa mengecek input kosong.

---

## 10. Praktik API Sederhana

Target:

- Bisa memahami alur request API.
- Bisa membaca loading, success, dan error state.
- Bisa menampilkan data dari response.

Alur dasar:

```text
User membuka halaman
-> aplikasi request API
-> tampilkan loading
-> jika berhasil tampilkan data
-> jika gagal tampilkan pesan error
```

Challenge:

- Ambil data dari API dummy.
- Tampilkan title post.
- Tambahkan tampilan loading.
- Tambahkan tampilan error.

Checklist:

- [ ] Bisa membuat function async.
- [ ] Bisa memakai `FutureBuilder`.
- [ ] Bisa parsing JSON sederhana.

---

## Checklist Akhir Praktik Dasar

Setelah menyelesaikan materi praktik ini, pastikan kamu sudah bisa:

- [ ] Membuat variable dan function dasar.
- [ ] Memakai `List`, `Map`, dan `Class`.
- [ ] Memahami Null Safety.
- [ ] Membuat UI sederhana dari widget.
- [ ] Mengubah tampilan dengan state.
- [ ] Membuat navigasi antar halaman.
- [ ] Membaca input dari form.
- [ ] Memahami alur dasar API.

Kalau semua checklist sudah aman, lanjut ke project pertama: **Aplikasi Catatan Belajar**.
